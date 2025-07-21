from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="FYP Age Prediction API")

app.include_router(router)
