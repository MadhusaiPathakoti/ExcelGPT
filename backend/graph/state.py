from typing import TypedDict


class AgentState(
    TypedDict
):

    question: str

    schema: str

    table_name: str

    intent: str

    sql: str

    result: list

    answer: str

    chart: dict