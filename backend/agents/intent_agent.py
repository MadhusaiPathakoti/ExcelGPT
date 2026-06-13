class IntentAgent:

    @staticmethod
    def detect(question):

        q = question.lower()

        if any(
            word in q
            for word in [
                "chart",
                "graph",
                "plot",
                "pie",
                "bar",
                "line"
            ]
        ):

            return "chart"

        if any(
            word in q
            for word in [
                "insight",
                "summary",
                "overview",
                "top product",
                "best region"
            ]
        ):

            return "insight"

        return "sql"