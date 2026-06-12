from fastapi import APIRouter
from pydantic import BaseModel

from services.session_store import SESSIONS

from agents.sql_agent import SQLAgent
from agents.explain_agent import ExplainAgent

from services.sql_executor import SQLExecutor
from services.sql_validator import SQLValidator

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    question: str


def detect_chart(question, result_df):

    question = question.lower()

    if result_df.empty:
        return None

    columns = result_df.columns.tolist()

    # Need at least 2 columns for charting
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
def chat(request: ChatRequest):

    if request.session_id not in SESSIONS:

        return {
            "answer": "Invalid session.",
            "sql": "",
            "result": [],
            "chart": None
        }

    table_name = SESSIONS[
        request.session_id
    ]

    db = SQLExecutor()

    schema_df = db.execute(
        f"DESCRIBE {table_name}"
    )

    schema = schema_df.to_string()

    try:

        sql = SQLAgent.generate_sql(
            request.question,
            schema,
            table_name
        )

    except Exception as e:

        return {
            "answer": f"SQL Generation Error: {str(e)}",
            "sql": "",
            "result": [],
            "chart": None
        }

    if not SQLValidator.validate(sql):

        return {
            "answer": "Invalid SQL generated.",
            "sql": sql,
            "result": [],
            "chart": None
        }

    try:

        result_df = SQLExecutor.execute(
            sql
        )

    except Exception as e:

        return {
            "answer": f"SQL Error: {str(e)}",
            "sql": sql,
            "result": [],
            "chart": None
        }

    try:

        explanation = (
            ExplainAgent.explain(
                request.question,
                result_df
            )
        )

    except Exception:

        explanation = (
            "Analysis completed successfully."
        )

    chart = detect_chart(
        request.question,
        result_df
    )

    print("\n========== DEBUG ==========")
    print("QUESTION:")
    print(request.question)

    print("\nSQL:")
    print(sql)

    print("\nRESULT COLUMNS:")
    print(result_df.columns.tolist())

    print("\nCHART:")
    print(chart)

    print("===========================\n")

    return {

        "sql": sql,

        "answer": explanation,

        "result":
            result_df
            .fillna("")
            .to_dict(
                orient="records"
            ),

        "chart": chart
    }