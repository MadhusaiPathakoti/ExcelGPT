from fastapi import APIRouter
from pydantic import BaseModel
from agents.dashboard_agent import (
    DashboardAgent
)

from agents.sql_agent import (
    SQLAgent
)

from agents.chart_agent import (
    ChartAgent
)
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

    question = question.lower()

    if not result:
        return None

    columns = list(
        result[0].keys()
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

    if request.session_id not in SESSIONS:

        return {

            "answer":
                "Invalid session.",

            "sql":
                "",

            "result":
                [],

            "chart":
                None,

            "dashboard":
                {}
        }

    session_data = (
        SESSIONS[
            request.session_id
        ]
    )

    tables = (
        session_data.get(
            "tables",
            []
        )
    )

    relationships = (
        session_data.get(
            "relationships",
            []
        )
    )

    if not tables:

        return {

            "answer":
                "No tables found in session.",

            "sql":
                "",

            "result":
                [],

            "chart":
                None
        }

    db = SQLExecutor()

    schema_text = ""

    try:

        for table in tables:

            table_name = (
                table[
                    "table_name"
                ]
            )

            schema_df = (
                db.execute(
                    f"""
                    DESCRIBE
                    {table_name}
                    """
                )
            )

            schema_text += f"""

TABLE:
{table_name}

SCHEMA:

{schema_df.to_string()}

==================================================
"""

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
                schema_text,

            "tables":
                tables,

            "relationships":
                relationships,

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
        # =====================================
        # Dashboard Mode
        # =====================================

        if result.get(
            "intent"
        ) == "dashboard":

            dashboard = (
                result.get(
                    "dashboard",
                    {}
                )
            )

            widgets = []

            for widget in dashboard.get(
                "widgets",
                []
            ):

                try:

                    sql = SQLAgent.generate_sql(

                        widget[
                            "question"
                        ],

                        schema_text,

                        tables,

                        relationships
                    )

                    df = (
                        SQLExecutor.execute(
                            sql
                        )
                    )

                    records = (
                        df.fillna("")
                        .to_dict(
                            orient="records"
                        )
                    )

                    chart = (
                        ChartAgent.recommend(
                            records,
                            widget[
                                "question"
                            ]
                        )
                    )

                    widgets.append(

                        {

                            "title":
                                widget[
                                    "title"
                                ],

                            "question":
                                widget[
                                    "question"
                                ],

                            "sql":
                                sql,

                            "result":
                                records,

                            "chart":
                                chart
                        }
                    )

                except Exception as e:

                    widgets.append(

                        {

                            "title":
                                widget[
                                    "title"
                                ],

                            "error":
                                str(e)
                        }
                    )

            return {

                "intent":
                    "dashboard",

                "dashboard_type":
                    dashboard.get(
                        "dashboard_type"
                    ),

                "widgets":
                    widgets
            }
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

    print(
        "\n========== MULTI TABLE QUERY =========="
    )

    print(
        "QUESTION:"
    )

    print(
        request.question
    )

    print(
        "\nTABLES:"
    )

    for table in tables:

        print(
            table[
                "table_name"
            ]
        )

    print(
        "\nRELATIONSHIPS:"
    )

    for rel in relationships:

        print(
            f"{rel['left_table']}.{rel['left_column']} "
            f"= "
            f"{rel['right_table']}.{rel['right_column']}"
        )

    print(
        "\nINTENT:"
    )

    print(
        result.get(
            "intent"
        )
    )

    print(
        "\nSQL:"
    )

    print(
        result.get(
            "sql"
        )
    )

    print(
        "\nCHART:"
    )

    print(
        chart
    )

    print(
        "\n=======================================\n"
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
            ),

        "tables":
            tables,

        "relationships":
            relationships
    }