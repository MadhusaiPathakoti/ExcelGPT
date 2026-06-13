class SchemaDiscovery:

    @staticmethod
    def classify_table(
        table_name,
        columns,
        row_count
    ):

        cols = [
            c.lower()
            for c in columns
        ]

        # ==================
        # FACT TABLE
        # ==================

        fact_score = 0

        for keyword in [

            "quantity",
            "qty",
            "sales",
            "revenue",
            "amount",
            "order"
        ]:

            if keyword in " ".join(cols):

                fact_score += 10

        # ==================
        # CUSTOMER
        # ==================

        customer_score = 0

        for keyword in [

            "customer",
            "customer_id",
            "customer_name"
        ]:

            if keyword in " ".join(cols):

                customer_score += 10

        # ==================
        # PRODUCT
        # ==================

        product_score = 0

        for keyword in [

            "product",
            "sku",
            "item",
            "price",
            "category"
        ]:

            if keyword in " ".join(cols):

                product_score += 10

        # ==================
        # REGION
        # ==================

        region_score = 0

        for keyword in [

            "region",
            "state",
            "territory",
            "country"
        ]:

            if keyword in " ".join(cols):

                region_score += 10

        scores = {

            "fact":
                fact_score,

            "customer":
                customer_score,

            "product":
                product_score,

            "region":
                region_score
        }

        role = max(
            scores,
            key=scores.get
        )

        return role 