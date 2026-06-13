from agents.intent_agent import (
    IntentAgent
)

from agents.sql_agent import (
    SQLAgent
)

from agents.explain_agent import (
    ExplainAgent
)

from agents.insight_agent import (
    InsightAgent
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
        state["table_name"]
    )

    result = (
        SQLExecutor.execute(sql)
    )

    state["sql"] = sql

    state["result"] = (
        result
        .to_dict(
            orient="records"
        )
    )

    return state

def run_insight(state):

    state["answer"] = (
        InsightAgent.execute(
            state["table_name"]
        )
    )

    return state

def explain(state):

    state["answer"] = (
        ExplainAgent.explain(
            state["question"],
            state["result"]
        )
    )

    return state