import pandas as pd


class DatasetProfiler:

    @staticmethod
    def generate_profile(df):

        profile = {}

        profile["rows"] = len(df)

        profile["columns"] = len(df.columns)

        profile["duplicates"] = int(
            df.duplicated().sum()
        )

        profile["missing_values"] = (
            df.isnull()
            .sum()
            .to_dict()
        )

        profile["missing_percentage"] = (
            (
                df.isnull().sum()
                / len(df)
            ) * 100
        ).round(2).to_dict()

        profile["numeric_summary"] = (
            df.describe(
                include="number"
            )
            .fillna("")
            .to_dict()
        )

        profile["categorical_summary"] = {}

        categorical_cols = (
            df.select_dtypes(
                include=["object"]
            ).columns
        )

        for col in categorical_cols:

            profile[
                "categorical_summary"
            ][col] = {

                "unique_values":
                    int(
                        df[col]
                        .nunique()
                    ),

                "top_value":
                    (
                        df[col]
                        .mode()[0]
                        if not df[col]
                        .mode()
                        .empty
                        else None
                    )
            }

        return profile
    
    @staticmethod
    def quality_score(df):

        total_cells = (
            len(df)
            * len(df.columns)
        )

        missing_cells = (
            df.isnull()
            .sum()
            .sum()
        )

        duplicate_rows = (
            df.duplicated()
            .sum()
        )

        missing_penalty = (
            missing_cells
            / total_cells
        ) * 50

        duplicate_penalty = (
            duplicate_rows
            / len(df)
        ) * 50

        score = (
            100
            - missing_penalty
            - duplicate_penalty
        )

        return round(
            max(score, 0),
            2
        )
    @staticmethod
    def suggested_questions(df):

        questions = []

        numeric_cols = (
            df.select_dtypes(
                include=["number"]
            ).columns
        )

        categorical_cols = (
            df.select_dtypes(
                include=["object"]
            ).columns
        )

        for col in numeric_cols[:3]:

            questions.append(
                f"What is average {col}?"
            )

        for col in categorical_cols[:3]:

            questions.append(
                f"Show distribution of {col}"
            )

        return questions