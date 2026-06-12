import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import uuid

from utils.api_client import upload_file

BACKEND_URL = "https://excelgpt-2zrp.onrender.com"

def render_chart(chart_info, result_table):

    if not chart_info:
        return

    if not result_table:
        return

    df = pd.DataFrame(result_table)

    chart_type = chart_info.get(
        "chart_type",
        "bar"
    )

    x = chart_info.get("x")
    y = chart_info.get("y")

    if x not in df.columns:
        st.warning(
            f"Column '{x}' not found."
        )
        return

    if y not in df.columns:
        st.warning(
            f"Column '{y}' not found."
        )
        return

    # KPI Cards

    try:

        if pd.api.types.is_numeric_dtype(
            df[y]
        ):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Total",
                    round(
                        df[y].sum(),
                        2
                    )
                )

            with col2:
                st.metric(
                    "Average",
                    round(
                        df[y].mean(),
                        2
                    )
                )

            with col3:
                st.metric(
                    "Maximum",
                    round(
                        df[y].max(),
                        2
                    )
                )

    except Exception:
        pass

    try:

        if chart_type != "line":

            if y in df.columns:
                df = df.sort_values(
                    by=y,
                    ascending=False
                )

        if chart_type == "bar":

            if len(df) >= 6:

                fig = px.bar(
                    df,
                    x=y,
                    y=x,
                    orientation="h",
                    text_auto=".2s"
                )

            else:

                fig = px.bar(
                    df,
                    x=x,
                    y=y,
                    text_auto=".2s"
                )

            fig.update_traces(
                textposition="outside"
            )

        elif chart_type == "line":

            fig = px.line(
                df,
                x=x,
                y=y,
                markers=True
            )

            fig.update_traces(
                line_width=4,
                marker_size=10
            )

        elif chart_type == "pie":

            fig = px.pie(
                df,
                names=x,
                values=y,
                hole=0.5
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

        elif chart_type == "scatter":

            fig = px.scatter(
                df,
                x=x,
                y=y,
                size=y
            )

        else:

            fig = px.bar(
                df,
                x=x,
                y=y,
                text_auto=".2s"
            )

        fig.update_layout(
            template="plotly_white",
            height=600,
            font=dict(
                size=14
            ),
            title=dict(
                x=0.5
            ),
            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            ),
            hovermode="closest",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Download Button

        csv = df.to_csv(
            index=False
        )

        st.download_button(
                label="📥 Download Results",
                data=csv,
                file_name="results.csv",
                mime="text/csv",
                key=f"download_{uuid.uuid4()}"
            )

    except Exception as e:

        st.error(
            f"Chart Error: {str(e)}"
        )

st.set_page_config(
    page_title="ExcelGPT",
    layout="wide"
)

st.title("ExcelGPT")
st.caption(
    """
    AI-Powered Business Intelligence Assistant
    Upload Excel files,
    analyze business data,
    generate charts,
    and ask questions in natural language.
    """
)

# =====================================
# Session State Initialization
# =====================================

if "dataset_uploaded" not in st.session_state:
    st.session_state.dataset_uploaded = False

if "upload_result" not in st.session_state:
    st.session_state.upload_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

# =====================================
# File Upload
# =====================================

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"]
)

# Upload only once

if (
    uploaded_file is not None
    and not st.session_state.dataset_uploaded
):

    with st.spinner("Analyzing dataset..."):

        result = upload_file(uploaded_file)
        st.write(result)
        st.stop()

        st.session_state.upload_result = result

        st.session_state.session_id = result.get(
            "session_id"
        )

        st.session_state.dataset_uploaded = True

# =====================================
# Show Dataset Information
# =====================================

if st.session_state.upload_result:

    result = st.session_state.upload_result

    profile = result.get(
        "profile",
        {}
    )

    st.success(
        "Dataset uploaded successfully"
    )

    # ---------------------------------

    with st.expander(
        "Dataset Overview",
        expanded=True
    ):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Rows",
                profile.get("rows", 0)
            )

        with col2:
            st.metric(
                "Columns",
                profile.get("columns", 0)
            )

        with col3:
            st.metric(
                "Quality Score",
                result.get(
                    "quality_score",
                    0
                )
            )

    # ---------------------------------

    with st.expander(
        "Missing Values"
    ):

        st.json(
            profile.get(
                "missing_values",
                {}
            )
        )

    # ---------------------------------

    with st.expander(
        "Duplicate Rows"
    ):

        st.write(
            profile.get(
                "duplicates",
                0
            )
        )

    # ---------------------------------

    if "numeric_summary" in profile:

        with st.expander(
            "Numeric Statistics"
        ):

            st.json(
                profile[
                    "numeric_summary"
                ]
            )

    # ---------------------------------

    if "categorical_summary" in profile:

        with st.expander(
            "Categorical Summary"
        ):

            st.json(
                profile[
                    "categorical_summary"
                ]
            )

    # ---------------------------------

    if "suggested_questions" in result:

        st.subheader(
            "Suggested Questions"
        )

        for question in result[
            "suggested_questions"
        ]:

            st.info(question)

    # ---------------------------------

    if "preview" in result:

        with st.expander(
            "Dataset Preview"
        ):

            st.dataframe(
                result["preview"],
                use_container_width=True
            )

    st.divider()

    # =====================================
    # Chat Section
    # =====================================

    st.header(
        "Chat With Your Data"
    )

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            if message["role"] == "assistant":

                if message.get("sql"):

                    st.code(
                        message["sql"],
                        language="sql"
                    )

                if message.get("result"):

                    st.dataframe(
                        message["result"],
                        use_container_width=True
                    )

                if message.get("chart"):

                    render_chart(
                        message["chart"],
                        message["result"]
                    )

    question = st.chat_input(
        "Ask a question about your data..."
    )

    if question:

        # User message

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # AI response

        with st.spinner(
            "Thinking..."
        ):

            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={
                    "session_id":
                        st.session_state.session_id,
                    "question":
                        question
                }
            )

            try:

                response_data = response.json()

            except Exception:

                st.error(
                    response.text
                )

                st.stop()

        answer = response_data.get(
            "answer",
            "No response generated."
        )

        sql = response_data.get(
            "sql",
            ""
        )

        result_table = response_data.get(
            "result",
            []
        )
        chart_info = response_data.get(
            "chart"
        )
        with st.chat_message(
            "assistant"
        ):

            st.markdown(answer)

            if sql:

                st.subheader(
                    "Generated SQL"
                )

                st.code(
                    sql,
                    language="sql"
                )

            if result_table:

                st.subheader(
                    "Results"
                )

                st.dataframe(
                    result_table,
                    use_container_width=True
                )

            if chart_info:

                st.subheader(
                    "Visualization"
                )

                render_chart(
                    chart_info,
                    result_table
                )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
                "sql": sql,
                "result": result_table,
                "chart": chart_info
            }
        )