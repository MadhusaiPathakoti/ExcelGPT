from typing import TypedDict
from typing import List
from typing import Dict


class AgentState(
    TypedDict
):

    question: str

    schema: str

    tables: List[Dict]

    intent: str

    sql: str

    result: list

    answer: str

    chart: dict
    
    dashboard: dict
    
    relationships: list