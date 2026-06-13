from services.sql_executor import (
    SQLExecutor
)


class MultiTableInsightGenerator:

    @staticmethod
    def generate(session_data):

        insights = {}

        tables = {

            table["table_name"].lower():

                table["table_name"]

            for table in session_data[
                "tables"
            ]
        }

        try:

            # ==========================
            # Top Product
            # ==========================

            if (
                "orders" in tables
                and
                "products" in tables
            ):

                sql = f"""
                SELECT
                    p."Product Name",
                    SUM(
                        o."Quantity"
                    ) qty
                FROM {tables['orders']} o
                JOIN {tables['products']} p
                ON o."Product Code" =
                   p."Product Code"
                GROUP BY 1
                ORDER BY qty DESC
                LIMIT 1
                """

                df = SQLExecutor.execute(
                    sql
                )

                if not df.empty:

                    insights[
                        "top_product"
                    ] = (
                        df.iloc[0][
                            "Product Name"
                        ]
                    )

            # ==========================
            # Best Region
            # ==========================

            if (
                "orders" in tables
                and
                "regions" in tables
            ):

                sql = f"""
                SELECT
                    r."Region Name",
                    SUM(
                        o."Quantity"
                    ) qty
                FROM {tables['orders']} o
                JOIN {tables['regions']} r
                ON o."Region Code" =
                   r."Region Code"
                GROUP BY 1
                ORDER BY qty DESC
                LIMIT 1
                """

                df = SQLExecutor.execute(
                    sql
                )

                if not df.empty:

                    insights[
                        "best_region"
                    ] = (
                        df.iloc[0][
                            "Region Name"
                        ]
                    )

            # ==========================
            # Revenue
            # ==========================

            if (
                "orders" in tables
                and
                "products" in tables
            ):

                sql = f"""
                SELECT
                    SUM(
                        p.Price *
                        o.Quantity
                    ) total_revenue
                FROM {tables['orders']} o
                JOIN {tables['products']} p
                ON o."Product Code" =
                   p."Product Code"
                """

                df = SQLExecutor.execute(
                    sql
                )

                if not df.empty:

                    insights[
                        "total_revenue"
                    ] = round(
                        float(
                            df.iloc[0][
                                "total_revenue"
                            ]
                        ),
                        2
                    )

            # ==========================
            # Top Customer
            # ==========================

            if (
                "orders" in tables
                and
                "customers" in tables
            ):

                sql = f"""
                SELECT
                    c."Customer Name",
                    SUM(
                        o.Quantity
                    ) qty
                FROM {tables['orders']} o
                JOIN {tables['customers']} c
                ON o."Customer ID" =
                   c."Customer ID"
                GROUP BY 1
                ORDER BY qty DESC
                LIMIT 1
                """

                df = SQLExecutor.execute(
                    sql
                )

                if not df.empty:

                    insights[
                        "top_customer"
                    ] = (
                        df.iloc[0][
                            "Customer Name"
                        ]
                    )

            # ==========================
            # Total Orders
            # ==========================

            if "orders" in tables:

                sql = f"""
                SELECT COUNT(*)
                AS total_orders
                FROM {tables['orders']}
                """

                df = SQLExecutor.execute(
                    sql
                )

                if not df.empty:

                    insights[
                        "total_orders"
                    ] = int(
                        df.iloc[0][
                            "total_orders"
                        ]
                    )

        except Exception as e:

            insights[
                "error"
            ] = str(e)

        return insights