from pathlib import Path
import uuid

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from services.excel_loader import ExcelLoader
from database.duckdb_manager import (
    DuckDBManager
)

from services.dataset_profiler import (
    DatasetProfiler
)
from services.session_store import (
    SESSIONS
)
router = APIRouter()

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(
    exist_ok=True
)


@router.post("/upload")
async def upload_excel(
        file: UploadFile = File(...)
):

    unique_name = (
        f"{uuid.uuid4()}_{file.filename}"
    )

    file_path = (
        UPLOAD_DIR / unique_name
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        content = await file.read()

        buffer.write(content)

    df = ExcelLoader.load_excel(
        str(file_path)
    )
    session_id = str(uuid.uuid4())

    safe_session_id = (
        session_id.replace("-", "_")
    )

    table_name = (
        f"dataset_{safe_session_id}"
    )
    SESSIONS[
        session_id
    ] = table_name  
    db = DuckDBManager()

    db.register_dataframe(
        table_name,
        df
    )
    profile = (
    DatasetProfiler
    .generate_profile(df)
    )

    quality_score = (
        DatasetProfiler
        .quality_score(df)
    )
    
    questions = (
    DatasetProfiler
    .suggested_questions(df)
    )
    

    return {

    "session_id":
        session_id,

    "table_name":
        table_name,

    "profile":
        profile,

    "quality_score":
        quality_score,

    "suggested_questions":
        questions,

    "preview":
        df.head(10)
        .fillna("")
        .to_dict(
            orient="records"
        )
}