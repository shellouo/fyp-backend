# app/routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import List, Tuple

from app.model_prediction import predict_and_display

ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

DATA_TEST_DIR = (Path(__file__).resolve().parent / ".." / "data_test").resolve()
DATA_TEST_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

# ---------------- Utility Functions ----------------
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
    If the number of images in the directory is >= 2 → immediately delete all images and raise an error,
    requiring the user to re-upload.
    """
    imgs = _list_images()
    if len(imgs) >= 2:
        _delete_all_images()
        raise HTTPException(
            status_code=400,
            detail="Two or more images were found in the data_test directory and have been deleted. Please re-upload (the system only allows one image at a time)."
        )

def _call_predict(image_path: Path) -> Tuple[int, str, float, str, float]:
    """
    Compatible with two types of return values:
      - (age, gender, gender_conf, race, race_conf)
      - (age, gender_conf, race_conf)  -> set gender/race as 'Unknown'
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

# ---------------- Request Body  ----------------
class FilenameRequest(BaseModel):
    filename: str

# ---------------- Routes ----------------
@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    1) Save the uploaded file to ../data_test
    2) If the directory contains >= 2 images: clear it and raise an error, asking the user to re-upload (only 1 image is allowed at a time)
    3) Call predict_and_display(image_path)
    4) Return JSON
    """
    if not _is_allowed(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    # Save uploaded file
    try:
        content = await file.read()
        save_path = (DATA_TEST_DIR / Path(file.filename).name).resolve()
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Save failed: {e}")

    # Check file count limit
    _enforce_single_after_change()

    # Call the model
    age, gender, gender_conf, race, race_conf = _call_predict(save_path)

    return JSONResponse(content={
        "age": age,
        "gender": gender,
        "gender_confidence": gender_conf,
        "race": race,
        "race_confidence": race_conf,
    })
