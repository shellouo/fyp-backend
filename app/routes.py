# app/routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import List, Tuple

# ✅ 修正导入路径：从 app.model_prediction 引入你的推理函数
from app.model_prediction import predict_and_display

ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# data_test 目录位于 fyp_backend/data_test
DATA_TEST_DIR = (Path(__file__).resolve().parent / ".." / "data_test").resolve()
DATA_TEST_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

# ---------------- 工具函数 ----------------
def _is_allowed(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTS

def _list_images() -> List[Path]:
    return [p for p in DATA_TEST_DIR.iterdir() if p.is_file() and _is_allowed(p.name)]

def _delete_all_images():
    for p in _list_images():
        try:
            p.unlink(missing_ok=True)
        except Exception:
            pass

def _enforce_single_after_change():
    """
    当目录内图片数量 >= 2 ——> 立即清空所有图片并抛错，要求用户重新上传。
    """
    imgs = _list_images()
    if len(imgs) >= 2:
        _delete_all_images()
        raise HTTPException(
            status_code=400,
            detail="data_test 中存在两张或以上图片，已全部删除。请重新上传（系统只允许同时存在一张图片）。"
        )

def _call_predict(image_path: Path) -> Tuple[int, str, float, str, float]:
    """
    兼容两种返回：
      - (age, gender, gender_conf, race, race_conf)
      - (age, gender_conf, race_conf)  -> gender/race 置为 'Unknown'
    """
    try:
        res = predict_and_display(str(image_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    if isinstance(res, (list, tuple)):
        if len(res) == 5:
            age, gender, gender_conf, race, race_conf = res
        elif len(res) == 3:
            age, gender_conf, race_conf = res
            gender, race = "Unknown", "Unknown"
        else:
            raise HTTPException(status_code=500, detail=f"Unexpected return format: len={len(res)}")
    else:
        raise HTTPException(status_code=500, detail="Unexpected return type from model.")

    return int(age), str(gender), float(gender_conf), str(race), float(race_conf)

# ---------------- 请求体（可选） ----------------
class FilenameRequest(BaseModel):
    filename: str

# ---------------- 路由 ----------------
@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    1) 保存上传文件到 ../data_test
    2) 若该目录出现 >=2 张图：清空并报错，提醒用户重传（系统只允许同时存在 1 张）
    3) 调用 predict_and_display(image_path)
    4) 返回 JSON
    """
    if not _is_allowed(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    # 保存上传文件
    try:
        content = await file.read()
        save_path = (DATA_TEST_DIR / Path(file.filename).name).resolve()
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Save failed: {e}")

    # 检查数量限制
    _enforce_single_after_change()

    # 调用模型
    age, gender, gender_conf, race, race_conf = _call_predict(save_path)

    return JSONResponse(content={
        "age": age,
        "gender": gender,
        "gender_confidence": gender_conf,
        "race": race,
        "race_confidence": race_conf,
    })
