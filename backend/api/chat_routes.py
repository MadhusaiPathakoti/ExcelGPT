from fastapi import APIRouter
from pydantic import BaseModel

from graph.workflow import graph

from services.session_store import (
    SESSIONS
)

from services.sql_executor import (
    SQLExecutor
)

router = APIRouter()


class ChatRequest(BaseModel):

    session_id: str

    question: str


def detect_chart(
    question,
    result
):

    question = (
        question.lower()
    )

    if not result:
        return None

    columns = (
        list(
            result[0].keys()
        )
    )

    if len(columns) < 2:
        return None

    x_column = columns[0]
    y_column = columns[1]

    if (
        "pie" in question
        or "contribution" in question
        or "share" in question
        or "percentage" in question
    ):

        return {
            "chart_type": "pie",
            "x": x_column,
            "y": y_column
        }

    if (
        "line" in question
        or "trend" in question
        or "over time" in question
    ):

        return {
            "chart_type": "line",
            "x": x_column,
            "y": y_column
        }

    if "scatter" in question:

        return {
            "chart_type": "scatter",
            "x": x_column,
            "y": y_column
        }

    if (
        "bar" in question
        or "chart" in question
        or "graph" in question
        or "plot" in question
        or "visualize" in question
        or "visualise" in question
    ):

        return {
            "chart_type": "bar",
            "x": x_column,
            "y": y_column
        }

    return None


@router.post("/chat")
def chat(
    request: ChatRequest
):

    if (
        request.session_id
        not in SESSIONS
    ):

        return {

            "answer":
                "Invalid session.",

            "sql":
                "",

            "result":
                [],

            "chart":
                None
        }

    table_name = (
        SESSIONS[
            request.session_id
        ]
    )

    db = SQLExecutor()

    try:

        schema_df = (
            db.execute(
                f"""
                DESCRIBE
                {table_name}
                """
            )
        )

        schema = (
            schema_df
            .to_string()
        )

    except Exception as e:

        return {

            "answer":
                f"Schema Error: {str(e)}",

            "sql":
                "",

            "result":
                [],

            "chart":
                None
        }

    try:

        state = {

            "question":
                request.question,

            "schema":
                schema,

            "table_name":
                table_name,

            "intent":
                "",

            "sql":
                "",

            "result":
                [],

            "answer":
                "",

            "chart":
                None
        }

        result = (
            graph.invoke(
                state
            )
        )

    except Exception as e:

        return {

            "answer":
                f"Workflow Error: {str(e)}",

            "sql":
                "",

            "result":
                [],

            "chart":
                None
        }

    chart = (
        result.get(
            "chart"
        )
    )

    if not chart:

        chart = detect_chart(
            request.question,
            result.get(
                "result",
                []
            )
        )

    print(
        "\n========== LANGGRAPH =========="
    )

    print(
        "QUESTION:",
        request.question
    )

    print(
        "INTENT:",
        result.get(
            "intent"
        )
    )

    print(
        "SQL:",
        result.get(
            "sql"
        )
    )

    print(
        "CHART:",
        chart
    )

    print(
        "===============================\n"
    )

    return {

        "answer":
            result.get(
                "answer",
                ""
            ),

        "sql":
            result.get(
                "sql",
                ""
            ),

        "result":
            result.get(
                "result",
                []
            ),

        "chart":
            chart,

        "intent":
            result.get(
                "intent",
                ""
            )
    }