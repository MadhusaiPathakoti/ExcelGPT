import pandas as pd


class ChartAgent:

    @staticmethod
    def recommend(
        result,
        question=""
    ):

        if not result:
            return None

        df = pd.DataFrame(result)

        if df.empty:
            return None

        question = question.lower()

        numeric_cols = list(
            df.select_dtypes(
                include="number"
            ).columns
        )

        categorical_cols = list(
            df.select_dtypes(
                exclude="number"
            ).columns
        )

        # =================================
        # USER EXPLICITLY ASKED PIE
        # =================================

        if (
            "pie" in question
            and len(categorical_cols) == 1
            and len(numeric_cols) == 1
            and len(df) <= 10
        ):

            return {

                "chart_type": "pie",

                "x": categorical_cols[0],

                "y": numeric_cols[0]
            }

        # =================================
        # USER EXPLICITLY ASKED BAR
        # =================================

        if (
            "bar" in question
            or "bar graph" in question
        ):

            return {

                "chart_type": "bar",

                "x": categorical_cols[0],

                "y": numeric_cols[0]
            }

        # =================================
        # USER EXPLICITLY ASKED LINE
        # =================================

        if (
            "line" in question
            or "trend" in question
        ):

            return {

                "chart_type": "line",

                "x": categorical_cols[0],

                "y": numeric_cols[0]
            }

        # =================================
        # AUTO DECISION
        # =================================

        if (
            len(categorical_cols) == 1
            and len(numeric_cols) == 1
        ):

            if len(df) <= 8:

                return {

                    "chart_type": "pie",

                    "x": categorical_cols[0],

                    "y": numeric_cols[0]
                }

            return {

                "chart_type": "bar",

                "x": categorical_cols[0],

                "y": numeric_cols[0]
            }

        if (
            len(categorical_cols) >= 2
            and len(numeric_cols) == 1
        ):

            return {

                "chart_type": "grouped_bar",

                "x": categorical_cols[0],

                "y": numeric_cols[0],

                "color": categorical_cols[1]
            }

        if len(numeric_cols) >= 2:

            return {

                "chart_type": "scatter",

                "x": numeric_cols[0],

                "y": numeric_cols[1]
            }

        return None