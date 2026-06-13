from agents.intent_agent import (
    IntentAgent
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


def detect_intent(state):

    state["intent"] = (
        IntentAgent.detect(
            state["question"]
        )
    )

    return state


def run_sql(state):

    sql = SQLAgent.generate_sql(

    state["question"],

    state["schema"],

    state["tables"],

    state["relationships"]
    )

    result = (
        SQLExecutor.execute(
            sql
        )
    )

    state["sql"] = sql

    state["result"] = (
        result
        .fillna("")
        .to_dict(
            orient="records"
        )
    )

    return state


def run_insight(state):

    tables = state[
        "tables"
    ]

    state["answer"] = {

        "tables_available":

            [
                table[
                    "table_name"
                ]
                for table in tables
            ],

        "message":

            f"""
Uploaded
{len(tables)}
table(s).

You can now ask
questions across
multiple datasets.
"""
    }

    return state


def explain(state):

    state["answer"] = (
        ExplainAgent.explain(

            state["question"],

            state["result"]
        )
    )

    return state