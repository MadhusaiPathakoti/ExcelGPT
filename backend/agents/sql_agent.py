from llm.prompts import (
    SQL_PROMPT
)

from llm.openrouter_client import (
    OpenRouterClient
)

from services.sql_cleaner import (
    SQLCleaner
)


class SQLAgent:

    @staticmethod
    def generate_sql(

        question,

        schema,

        tables,

        relationships
    ):

        table_names = [

            table[
                "table_name"
            ]

            for table in tables
        ]

        tables_text = "\n".join(
            table_names
        )

        relationship_text = ""

        for rel in relationships:

            relationship_text += f"""
{rel['left_table']}.{rel['left_column']}
=
{rel['right_table']}.{rel['right_column']}

"""

        prompt = SQL_PROMPT.format(

            question=question,

            schema=schema,

            tables=tables_text,

            relationships=relationship_text
        )

        print(
            "\n========== SQL PROMPT =========="
        )

        print(prompt)

        print(
            "\n===============================\n"
        )

        response = (
            OpenRouterClient
            .chat(
                [
                    {
                        "role":
                            "user",

                        "content":
                            prompt
                    }
                ]
            )
        )

        sql = (
            SQLCleaner
            .clean(
                response
            )
        )

        print(
            "\nGenerated SQL:"
        )

        print(sql)

        return sql