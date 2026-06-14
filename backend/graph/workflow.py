from langgraph.graph import (
    StateGraph,
    END
)

from graph.state import (
    AgentState
)

from graph.nodes import (

    detect_intent,

    run_sql,

    run_insight,

    explain,
    generate_chart
)


builder = StateGraph(
    AgentState
)

builder.add_node(
    "intent",
    detect_intent
)

builder.add_node(
    "chart",
    generate_chart
)

builder.add_node(
    "sql",
    run_sql
)

builder.add_node(
    "insight",
    run_insight
)

builder.add_node(
    "explain",
    explain
)


def router(state):

    return state[
        "intent"
    ]


builder.set_entry_point(
    "intent"
)

builder.add_conditional_edges(

    "intent",

    router,

    {

        "sql":
            "sql",

        "chart":
            "sql",

        "insight":
            "insight"
    }
)

builder.add_edge(
    "sql",
    "chart"
)

builder.add_edge(
    "chart",
    "explain"
)
builder.add_edge(
    "insight",
    END
)

builder.add_edge(
    "explain",
    END
)

graph = (
    builder.compile()
)