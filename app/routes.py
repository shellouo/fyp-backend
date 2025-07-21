from fastapi import APIRouter, UploadFile, File
from app.preprocess import preprocess_image
import numpy as np

router = APIRouter()

@router.post("/preprocess")
async def preprocess(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img_array = preprocess_image(image_bytes)
    return {"shape": list(img_array.shape)}