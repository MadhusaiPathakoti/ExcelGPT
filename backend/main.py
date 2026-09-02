import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.voice_routes import router as voice_router
from api.upload_routes import router as upload_router
from api.chat_routes import (
    router as chat_router
)
app = FastAPI(
    title="ExcelGPT"
)

frontend_origin = os.getenv("FRONTEND_ORIGIN")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin] if frontend_origin else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    upload_router,
    prefix="/api"
)
app.include_router(
    chat_router,
    prefix="/api"
)
app.include_router(
    voice_router,
    prefix="/api"
)

@app.get("/")
def health():

    return {
        "status": "running"
    }