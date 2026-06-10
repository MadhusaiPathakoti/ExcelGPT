from llm.prompts import SQL_PROMPT
from llm.openrouter_client import OpenRouterClient

from services.sql_cleaner import SQLCleaner


class SQLAgent:

    @staticmethod
    def generate_sql(
        question,
        schema,
        table_name
    ):

        prompt = SQL_PROMPT.format(
            question=question,
            schema=schema,
            table_name=table_name
        )

        response = OpenRouterClient.chat([
            {
                "role": "user",
                "content": prompt
            }
        ])

        sql = SQLCleaner.clean(
            response
        )

        print("\nGenerated SQL:")
        print(sql)

        return sql