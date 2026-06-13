import pandas as pd


class InsightGenerator:

    @staticmethod
    def generate(df):

        insights = {}

        # ==================================
        # Total Revenue
        # ==================================

        if "revenue" in df.columns:

            insights[
                "total_revenue"
            ] = round(
                float(
                    df["revenue"]
                    .sum()
                ),
                2
            )

        # ==================================
        # Top Product
        # ==================================

        if (
            "Product Name"
            in df.columns
            and
            "revenue"
            in df.columns
        ):

            top_product = (
                df.groupby(
                    "Product Name"
                )["revenue"]
                .sum()
                .idxmax()
            )

            insights[
                "top_product"
            ] = top_product

        # ==================================
        # Most Ordered Product
        # ==================================

        if (
            "Product Name"
            in df.columns
            and
            "Quantity"
            in df.columns
        ):

            most_ordered = (
                df.groupby(
                    "Product Name"
                )["Quantity"]
                .sum()
                .idxmax()
            )

            insights[
                "most_ordered_product"
            ] = most_ordered

        # ==================================
        # Best Region
        # ==================================

        if (
            "Region"
            in df.columns
            and
            "revenue"
            in df.columns
        ):

            best_region = (
                df.groupby(
                    "Region"
                )["revenue"]
                .sum()
                .idxmax()
            )

            insights[
                "best_region"
            ] = best_region

        # ==================================
        # Missing Data
        # ==================================

        missing = (
            df.isnull()
            .sum()
            .sum()
        )

        insights[
            "missing_cells"
        ] = int(missing)

        # ==================================
        # Outliers (IQR Method)
        # ==================================

        outlier_count = 0

        numeric_cols = (
            df.select_dtypes(
                include="number"
            ).columns
        )

        for col in numeric_cols:

            q1 = (
                df[col]
                .quantile(0.25)
            )

            q3 = (
                df[col]
                .quantile(0.75)
            )

            iqr = q3 - q1

            lower = (
                q1 - 1.5 * iqr
            )

            upper = (
                q3 + 1.5 * iqr
            )

            outlier_count += len(
                df[
                    (df[col] < lower)
                    |
                    (df[col] > upper)
                ]
            )

        insights[
            "outliers"
        ] = int(outlier_count)

        # ==================================
        # AI Summary
        # ==================================

        summary = []

        if (
            "top_product"
            in insights
        ):

            summary.append(
                f"Top revenue product is {insights['top_product']}"
            )

        if (
            "best_region"
            in insights
        ):

            summary.append(
                f"Best performing region is {insights['best_region']}"
            )

        if (
            "most_ordered_product"
            in insights
        ):

            summary.append(
                f"Most ordered product is {insights['most_ordered_product']}"
            )

        if insights[
            "missing_cells"
        ] == 0:

            summary.append(
                "Dataset contains no missing values"
            )

        insights[
            "summary"
        ] = summary

        return insights