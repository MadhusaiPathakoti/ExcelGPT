import streamlit as st
import requests

from utils.api_client import upload_file

BACKEND_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="ExcelGPT",
    layout="wide"
)

st.title("ExcelGPT")
st.caption(
    "AI-Powered Business Intelligence Assistant"
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

            if (
                message["role"]
                == "assistant"
            ):

                if "sql" in message:

                    st.code(
                        message["sql"],
                        language="sql"
                    )

                if "result" in message:

                    st.dataframe(
                        message["result"],
                        use_container_width=True
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

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
                "sql": sql,
                "result": result_table
            }
        )