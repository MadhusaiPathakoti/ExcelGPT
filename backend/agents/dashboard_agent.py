class DashboardAgent:

    @staticmethod
    def generate_dashboard(question):

        q = question.lower()

        if (
            "sales" in q
            or "revenue" in q
            or "executive" in q
        ):

            return {

                "dashboard_type":
                    "executive",

                "widgets": [

                    {
                        "title":
                            "Revenue By Region",

                        "question":
                            "Show revenue by region"
                    },

                    {
                        "title":
                            "Revenue By Category",

                        "question":
                            "Show revenue by product category"
                    },

                    {
                        "title":
                            "Top Products",

                        "question":
                            "Top 10 products by revenue"
                    },

                    {
                        "title":
                            "Revenue Trend",

                        "question":
                            "Show monthly revenue trend"
                    }
                ]
            }

        return {

            "dashboard_type":
                "generic",

            "widgets": [

                {
                    "title":
                        "Top Records",

                    "question":
                        "Show top records"
                }
            ]
        }