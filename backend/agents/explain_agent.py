from llm.openrouter_client import (
    OpenRouterClient
)


class ExplainAgent:

    @staticmethod
    def explain(
        question,
        result
    ):

        prompt = f"""
Question:
{question}

Result:

{result}

Explain in simple business language.
"""

        return (
            OpenRouterClient
            .chat([
                {
                    "role":"user",
                    "content":prompt
                }
            ])
        )