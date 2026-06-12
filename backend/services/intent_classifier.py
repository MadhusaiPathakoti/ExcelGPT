class IntentClassifier:

    CHART_KEYWORDS = [
        "chart",
        "graph",
        "plot",
        "visualize",
        "visualise",
        "pie",
        "bar",
        "line",
        "scatter",
        "trend",
        "distribution"
    ]

    @staticmethod
    def is_chart_request(question):

        question = question.lower()

        return any(
            keyword in question
            for keyword in IntentClassifier.CHART_KEYWORDS
        )