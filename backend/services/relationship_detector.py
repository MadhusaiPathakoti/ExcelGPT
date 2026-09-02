import re


class RelationshipDetector:

    COLUMN_ALIASES = {

        "customer_id": [

            "customer_id",
            "cust_id",
            "client_id",
            "customerkey",
            "customer_key"
        ],

        "product_id": [

            "product_id",
            "product_code",
            "sku",
            "item_id",
            "item_code"
        ],

        "region_id": [

            "region_id",
            "region_code",
            "territory_id",
            "state_code"
        ],

        "order_id": [

            "order_id",
            "order_number",
            "transaction_id"
        ]
    }

    @staticmethod
    def normalize_column(
        column_name
    ):

        column_name = (
            column_name
            .lower()
            .strip()
        )

        column_name = re.sub(
            r"[\s\-_]",
            "",
            column_name
        )

        return column_name

    @classmethod
    def semantic_name(
        cls,
        column_name
    ):

        normalized = (
            cls.normalize_column(
                column_name
            )
        )

        for canonical_name, aliases in (
            cls.COLUMN_ALIASES.items()
        ):

            normalized_aliases = [

                cls.normalize_column(
                    alias
                )

                for alias in aliases
            ]

            if normalized in normalized_aliases:

                return canonical_name

        return normalized

    @classmethod
    def detect_relationships(
        cls,
        tables_metadata
    ):

        relationships = []

        for i in range(
            len(tables_metadata)
        ):

            for j in range(
                i + 1,
                len(tables_metadata)
            ):

                table1 = (
                    tables_metadata[i]
                )

                table2 = (
                    tables_metadata[j]
                )

                for col1 in table1["columns"]:

                    semantic_col1 = (
                        cls.semantic_name(
                            col1
                        )
                    )

                    for col2 in table2["columns"]:

                        semantic_col2 = (
                            cls.semantic_name(
                                col2
                            )
                        )

                        if (
                            semantic_col1
                            ==
                            semantic_col2
                        ):

                            relationships.append(

                                {

                                    "left_table":
                                        table1[
                                            "table_name"
                                        ],

                                    "left_column":
                                        col1,

                                    "right_table":
                                        table2[
                                            "table_name"
                                        ],

                                    "right_column":
                                        col2,

                                    "relationship":
                                        semantic_col1
                                }
                            )

        return relationships