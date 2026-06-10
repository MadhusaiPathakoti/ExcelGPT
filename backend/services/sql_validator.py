class SQLValidator:

    ALLOWED = (
        "SELECT",
        "WITH",
        "DESCRIBE"
    )

    @staticmethod
    def validate(sql):

        sql = sql.strip().upper()

        return sql.startswith(
            SQLValidator.ALLOWED
        )