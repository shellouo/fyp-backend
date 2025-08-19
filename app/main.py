# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(title="FYP Age Prediction API", version="1.0.0")

# Allow frontend Vue local URL access (e.g. http://localhost:5173) when running: python -m uvicorn main:app --reload
# (Port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the route only once

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
