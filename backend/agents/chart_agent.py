import json

from llm.openrouter_client import (
    OpenRouterClient
)


class ChartAgent:

    @staticmethod
    def generate_chart_metadata(
        question,
        schema
    ):

        prompt = f"""
You are a data visualization expert.

Based on the user question and dataset schema,
identify the chart to generate.

Return ONLY JSON.

Schema:
{schema}

Question:
{question}

Example:

{{
    "chart_type":"pie",
    "x":"Region",
    "y":"Revenue"
}}
"""

        try:

            response = (
                OpenRouterClient.chat(
                    [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            )

            response = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(
                response
            )

        except Exception as e:

            print(
                "Chart Agent Error:",
                e
            )

            return {
                "chart_type": "bar"
            }