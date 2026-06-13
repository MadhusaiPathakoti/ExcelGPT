from pathlib import Path
import uuid
from typing import List

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from services.insight_generator import (
    InsightGenerator
)

from services.relationship_detector import (
    RelationshipDetector
)

from services.excel_loader import (
    ExcelLoader
)

from services.multi_table_insight_generator import (
    MultiTableInsightGenerator
)

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
    files: List[UploadFile] = File(...)
):

    session_id = str(
        uuid.uuid4()
    )

    db = DuckDBManager()

    uploaded_tables = []

    tables_metadata = []

    fact_df = None

    fact_score = -1

    for file in files:

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

            buffer.write(
                content
            )

        df = (
            ExcelLoader
            .load_excel(
                str(file_path)
            )
        )

        table_name = (
            Path(
                file.filename
            )
            .stem
            .lower()
            .replace(
                " ",
                "_"
            )
        )

        db.register_dataframe(
            table_name,
            df
        )

        uploaded_tables.append(
            {
                "table_name":
                    table_name,

                "rows":
                    len(df),

                "columns":
                    len(df.columns)
            }
        )

        tables_metadata.append(
            {
                "table_name":
                    table_name,

                "columns":
                    list(
                        df.columns
                    )
            }
        )

        # ==========================
        # Fact Table Detection
        # ==========================

        score = 0

        cols = [
            c.lower()
            for c in df.columns
        ]

        if "revenue" in cols:
            score += 100

        if "sales" in cols:
            score += 100

        if "quantity" in cols:
            score += 50

        if "price" in cols:
            score += 50

        score += len(df)

        if score > fact_score:

            fact_score = score

            fact_df = df

    relationships = (
        RelationshipDetector
        .detect_relationships(
            tables_metadata
        )
    )

    SESSIONS[
        session_id
    ] = {

        "tables":
            uploaded_tables,

        "relationships":
            relationships
    }

    if fact_df is None:

        return {

            "session_id":
                session_id,

            "tables":
                uploaded_tables,

            "relationships":
                relationships,

            "profile":
                {},

            "quality_score":
                0,

            "suggested_questions":
                [],

            "insights":
                {},

            "preview":
                []
        }

    profile = (
        DatasetProfiler
        .generate_profile(
            fact_df
        )
    )

    quality_score = (
        DatasetProfiler
        .quality_score(
            fact_df
        )
    )

    questions = (
        DatasetProfiler
        .suggested_questions(
            fact_df
        )
    )
    print("\n========== FACT TABLE ==========")

    print(
        fact_df.columns.tolist()
    )

    print(
        fact_df.head(5)
    )

    print("\n===============================\n")

    insights = (
        MultiTableInsightGenerator
        .generate(
            SESSIONS[
                session_id
            ]
            )
        )

    print(
        "\n========== FACT TABLE =========="
    )

    print(
        fact_df.columns.tolist()
    )

    print(
        "================================\n"
    )

    return {

        "session_id":
            session_id,

        "tables":
            uploaded_tables,

        "relationships":
            relationships,

        "profile":
            profile,

        "quality_score":
            quality_score,

        "suggested_questions":
            questions,

        "insights":
            insights,

        "preview":
            fact_df
            .head(10)
            .fillna("")
            .to_dict(
                orient="records"
            )
    }