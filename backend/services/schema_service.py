class SchemaService:

    @staticmethod
    def generate_schema_context(df):

        schema = []

        for col, dtype in df.dtypes.items():

            schema.append(
                f"{col}: {dtype}"
            )

        return "\n".join(schema)