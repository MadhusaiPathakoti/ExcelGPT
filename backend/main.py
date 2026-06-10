from fastapi import FastAPI

from api.upload_routes import router as upload_router
from api.chat_routes import (
    router as chat_router
)
app = FastAPI(
    title="ExcelGPT"
)

app.include_router(
    upload_router,
    prefix="/api"
)
app.include_router(
    chat_router,
    prefix="/api"
)

@app.get("/")
def health():

    return {
        "status": "running"
    }