import os
from dotenv import load_dotenv
load_dotenv()
import requests


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

MODEL_NAME = "deepseek/deepseek-chat"


class OpenRouterClient:

    @staticmethod
    def chat(messages):

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization":
                    f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type":
                    "application/json"
            },
            json={
                "model": MODEL_NAME,
                "messages": messages
            }
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        data = response.json()

        if "choices" not in data:
            raise Exception(
                f"OpenRouter Error: {data}"
            )

        return (
            data["choices"][0]
            ["message"]["content"]
        )