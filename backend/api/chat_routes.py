from fastapi import APIRouter

from pydantic import BaseModel

from services.session_store import (
    SESSIONS
)

from agents.sql_agent import (
    SQLAgent
)

from agents.explain_agent import (
    ExplainAgent
)

from services.sql_executor import (
    SQLExecutor
)

from services.sql_validator import (
    SQLValidator
)

router = APIRouter()

class ChatRequest(
    BaseModel
):
    session_id: str
    question: str
    
@router.post("/chat")
def chat(
    request: ChatRequest
):

    table_name = (
        SESSIONS[
            request.session_id
        ]
    )

    db = SQLExecutor()

    schema_df = (
        db.execute(
            f"DESCRIBE {table_name}"
        )
    )

    schema = (
        schema_df.to_string()
    )

    sql = (
        SQLAgent.generate_sql(
            request.question,
            schema,
            table_name
        )
    )
    if not SQLValidator.validate(sql):

        return {
            "answer":
                "Invalid SQL generated.",
            "sql":
                sql,
            "result":[]
        }

    try:

        result_df = SQLExecutor.execute(
            sql
        )

    except Exception as e:

        return {

            "answer":
                f"SQL Error: {str(e)}",

            "sql":
                sql,

            "result":[]
        }

    explanation = (
        ExplainAgent.explain(
            request.question,
            result_df
        )
    )

    return {

        "sql": sql,

        "answer":
            explanation,

        "result":
            result_df
            .fillna("")
            .to_dict(
                orient="records"
            )
    }