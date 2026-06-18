from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from pathlib import Path
import uuid

from services.speech_service import (
    SpeechService
)

router = APIRouter()


@router.post(
    "/voice"
)
async def voice_to_text(

    file: UploadFile = File(...)
):

    temp_path = (
        f"temp_{uuid.uuid4()}.wav"
    )

    with open(
        temp_path,
        "wb"
    ) as f:

        f.write(
            await file.read()
        )

    text = (
        SpeechService.transcribe(
            temp_path
        )
    )

    return {

        "question":
            text
    }