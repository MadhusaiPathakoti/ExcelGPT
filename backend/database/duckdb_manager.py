import duckdb


class DuckDBManager:

    def __init__(self):

        self.conn = duckdb.connect(
            "excelgpt.db"
        )

    def register_dataframe(
        self,
        table_name,
        dataframe
    ):

        self.conn.register(
            "temp_df",
            dataframe
        )

        self.conn.execute(
            f"""
            CREATE OR REPLACE TABLE
            {table_name}
            AS
            SELECT *
            FROM temp_df
            """
        )

    def execute_query(
        self,
        query
    ):

        return (
            self.conn
            .execute(query)
            .fetchdf()
        )

    def get_schema(
        self,
        table_name
    ):

        return (
            self.conn
            .execute(
                f"""
                DESCRIBE {table_name}
                """
            )
            .fetchdf()
        )

    def get_columns(
        self,
        table_name
    ):

        schema = (
            self.get_schema(
                table_name
            )
        )

        return (
            schema[
                "column_name"
            ]
            .tolist()
        )

    def get_all_tables(self):

        tables = (
            self.conn
            .execute(
                """
                SHOW TABLES
                """
            )
            .fetchall()
        )

        return [
            t[0]
            for t in tables
        ]