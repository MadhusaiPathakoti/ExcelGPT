import plotly.express as px


class ChartService:

    @staticmethod
    def create_chart(
        dataframe,
        chart_type,
        x,
        y
    ):

        if dataframe is None or dataframe.empty:
            raise ValueError(
                "Cannot create chart from empty dataframe."
            )

        if x not in dataframe.columns:
            raise ValueError(
                f"Column '{x}' not found in dataframe."
            )

        if y and y not in dataframe.columns:
            raise ValueError(
                f"Column '{y}' not found in dataframe."
            )

        chart_type = (
            chart_type
            .lower()
            .strip()
        )

        try:

            if chart_type == "bar":

                fig = px.bar(
                    dataframe,
                    x=x,
                    y=y,
                    title=f"{y} by {x}"
                )

            elif chart_type == "line":

                fig = px.line(
                    dataframe,
                    x=x,
                    y=y,
                    title=f"{y} Trend"
                )

            elif chart_type == "pie":

                fig = px.pie(
                    dataframe,
                    names=x,
                    values=y,
                    title=f"{y} Distribution"
                )

            elif chart_type == "scatter":

                fig = px.scatter(
                    dataframe,
                    x=x,
                    y=y,
                    title=f"{x} vs {y}"
                )

            else:

                # fallback
                fig = px.bar(
                    dataframe,
                    x=x,
                    y=y,
                    title=f"{y} by {x}"
                )

            fig.update_layout(
                height=500
            )

            return fig

        except Exception as e:

            raise Exception(
                f"Chart generation failed: {str(e)}"
            )