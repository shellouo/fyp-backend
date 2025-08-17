from pathlib import Path
import os

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "gif"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_save_path(filename: str) -> Path:
    outdir = Path.cwd() / "data_test"
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir / filename

def remove_file(filename: str) -> Path:
    outdir = Path.cwd() / "data_test"
    if os.path.exists(outdir / filename):
        os.remove(outdir / filename)