from services.insight_generator import (
    InsightGenerator
)

from database.duckdb_manager import (
    DuckDBManager
)


class InsightAgent:

    @staticmethod
    def execute(table_name):

        db = DuckDBManager()

        df = db.execute_query(
            f"""
            SELECT *
            FROM {table_name}
            """
        )

        return (
            InsightGenerator
            .generate(df)
        )