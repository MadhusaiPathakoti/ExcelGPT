import re


class SQLCleaner:

    @staticmethod
    def clean(text: str):

        text = text.strip()

        text = text.replace(
            "```sql",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        # Find first SELECT/WITH

        match = re.search(
            r"(SELECT|WITH|DESCRIBE).*",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if match:

            return match.group(0).strip()

        return text