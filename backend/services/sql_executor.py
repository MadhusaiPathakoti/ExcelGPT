from database.duckdb_manager import (
    DuckDBManager
)


class SQLExecutor:

    @staticmethod
    def execute(sql):

        db = DuckDBManager()

        return db.execute_query(
            sql
        )