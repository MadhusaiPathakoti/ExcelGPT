import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import uuid

from utils.api_client import upload_file

BACKEND_URL = "https://excelgpt-2zrp.onrender.com/api"

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
    color = chart_info.get(
        "color"
    )
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

        if (
            chart_type
            not in [
                "line",
                "grouped_bar"
            ]
        ):

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

            pie_df = (
                df.nlargest(
                    10,
                    y
                )
            )

            fig = px.pie(
                pie_df,
                names=x,
                values=y,
                hole=0.5
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )
        elif chart_type == "grouped_bar":

            color_column = chart_info.get(
                "color"
            )

            fig = px.bar(
                df,
                x=x,
                y=y,
                color=color_column,
                barmode="group",
                text_auto=".2s"
            )

            fig.update_traces(
                textposition="outside"
            )
        elif chart_type == "stacked_bar":

            fig = px.bar(
                df,
                x=x,
                y=y,
                color=chart_info.get(
                    "color"
                ),
                barmode="stack",
                text_auto=".2s"
            )
        elif chart_type == "treemap":

            fig = px.treemap(
                df,
                path=[
                    x,
                    chart_info.get(
                        "color"
                    )
                ],
                values=y
            )
        elif chart_type == "heatmap":

            pivot_df = df.pivot_table(
                index=x,
                columns=chart_info.get(
                    "color"
                ),
                values=y,
                aggfunc="sum"
            )

            fig = px.imshow(
                pivot_df,
                text_auto=True
            )
        elif chart_type == "scatter":

            fig = px.scatter(
                df,
                x=x,
                y=y,
                size=y
            )

        else:

            numeric_cols = list(
                df.select_dtypes(
                    include="number"
                ).columns
            )

            categorical_cols = [

                col

                for col in df.columns

                if col not in numeric_cols
            ]

            if (
                len(categorical_cols) >= 2
                and
                len(numeric_cols) >= 1
            ):

                fig = px.bar(
                    df,
                    x=categorical_cols[0],
                    y=numeric_cols[0],
                    color=categorical_cols[1],
                    barmode="group",
                    text_auto=".2s"
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

        import uuid

        st.plotly_chart(
            fig,
            use_container_width=True,
            key=f"chart_{uuid.uuid4()}"
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
if "editing_index" not in st.session_state:
    st.session_state.editing_index = None
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# =====================================
# File Upload
# =====================================

uploaded_files = st.file_uploader(
    "Upload Excel Files",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)
# Upload only once

if (
    uploaded_files
    and len(uploaded_files) > 0
    and not st.session_state.dataset_uploaded
):

    with st.spinner("Analyzing dataset..."):

        result = upload_file(uploaded_files)

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
    insights = result.get(
    "insights",
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

    # =====================================
    # Uploaded Datasets
    # =====================================

    if "previews" in result:

        st.header(
            "📂 Uploaded Datasets"
        )

        previews = result.get(
            "previews",
            {}
        )

        tables = result.get(
            "tables",
            []
        )

        for table in tables:

            table_name = table[
                "table_name"
            ]

            rows = table[
                "rows"
            ]

            cols = table[
                "columns"
            ]

            with st.expander(
                f"📄 {table_name} | {rows} rows | {cols} columns"
            ):

                preview_data = (
                    previews.get(
                        table_name,
                        []
                    )
                )

                if preview_data:

                    st.dataframe(
                        pd.DataFrame(
                            preview_data
                        ),
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No preview available"
                    )

    # =====================================
    # Relationship Explorer
    # =====================================

    relationships = result.get(
        "relationships",
        []
    )

    if relationships:

        st.header(
            "🔗 Relationship Explorer"g
        )

        st.success(
            f"Detected {len(relationships)} relationship(s)"
        )

        for rel in relationships:

            left_table = rel[
                "left_table"
            ]

            left_column = rel[
                "left_column"
            ]

            right_table = rel[
                "right_table"
            ]

            right_column = rel[
                "right_column"
            ]

            relation_name = rel.get(
                "relationship",
                ""
            )

            st.markdown(
                f"""
    **{left_table}.{left_column}**
    &nbsp;&nbsp;➡️
    **{right_table}.{right_column}**

    Relationship Type:
    `{relation_name}`
    """
            )

            st.divider()

    # =====================================
    # Data Model Summary
    # =====================================

    if tables:

        st.header(
            "📊 Data Model Summary"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Tables",
                len(tables)
            )

        with col2:

            st.metric(
                "Relationships",
                len(relationships)
            )

        with col3:

            total_rows = sum(
                table["rows"]
                for table in tables
            )

            st.metric(
                "Total Rows",
                total_rows
            )

        st.subheader(
            "Available Tables"
        )

        for table in tables:

            st.info(
                f"""
    {table['table_name']}
    ({table['rows']} rows,
    {table['columns']} columns)
    """
            )
    
    st.header(
                "📊 AI Generated Insights"
            )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Top Product",
            insights.get(
                "top_product",
                "N/A"
            )
        )

    with c2:

        st.metric(
            "Best Region",
            insights.get(
                "best_region",
                "N/A"
            )
        )

    with c3:

        st.metric(
            "Most Ordered Product",
            insights.get(
                "most_ordered_product",
                "N/A"
            )
        )

    c4, c5, c6 = st.columns(3)

    with c4:

        st.metric(
            "Revenue",
            insights.get(
                "total_revenue",
                0
            )
        )

    with c5:

        st.metric(
            "Missing Cells",
            insights.get(
                "missing_cells",
                0
            )
        )

    with c6:

        st.metric(
            "Outliers",
            insights.get(
                "outliers",
                0
            )
        )

    for item in insights.get(
        "summary",
        []
    ):

        st.success(item)

    st.divider()
        # ---------------------------------

    if "suggested_questions" in result:

        st.subheader(
            "Suggested Questions"
        )

        for question in result[
            "suggested_questions"
        ]:

            st.info(question)

    # =====================================
    # Chat Section
    # =====================================

    st.header(
        "Chat With Your Data"
    )
    
    for idx, message in enumerate(
    st.session_state.chat_history
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            # ==========================
            # USER MESSAGE
            # ==========================

            if (
                message["role"] == "user"
            ):

                col1, col2 = st.columns(
                    [1, 8]
                )

                with col1:

                    edit_clicked = st.button(
                        "✏️",
                        key=f"edit_{idx}"
                    )

                    if edit_clicked:

                        st.session_state[
                            "editing_index"
                        ] = idx

                        st.session_state[
                            "editing_index"
                        ] = idx

                    if (
                        st.session_state[
                            "editing_index"
                        ]
                        == idx
                    ):

                        edited_question = (
                            st.text_area(
                                "Edit Question",
                                value=message[
                                    "content"
                                ],
                                key=f"edit_box_{idx}"
                            )
                        )

                    if st.button(
                        "🔄 Regenerate",
                        key=f"regen_{idx}"
                    ):

                        with st.spinner(
                            "Regenerating..."
                        ):

                            response = requests.post(
                                f"{BACKEND_URL}/chat",
                                json={
                                    "session_id":
                                        st.session_state.session_id,
                                    "question":
                                        edited_question
                                }
                            )

                            response_data = (
                                response.json()
                            )

                        # update user question

                        st.session_state.chat_history[
                            idx
                        ]["content"] = (
                            edited_question
                        )

                        # update assistant answer

                        new_assistant_message = {

                            "role":
                                "assistant",

                            "content":
                                response_data.get(
                                    "answer",
                                    ""
                                ),

                            "sql":
                                response_data.get(
                                    "sql",
                                    ""
                                ),

                            "result":
                                response_data.get(
                                    "result",
                                    []
                                ),

                            "chart":
                                response_data.get(
                                    "chart"
                                )
                        }

                        st.session_state.chat_history = (

                            st.session_state.chat_history[
                                :idx
                            ]

                            +

                            [
                                {
                                    "role": "user",
                                    "content": edited_question
                                },
                                new_assistant_message
                            ]
                        )
                        st.session_state[
                            "editing_index"
                        ] = None

                        st.rerun()

            # ==========================
            # ASSISTANT MESSAGE
            # ==========================

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
                # =====================================
                # Dashboard Response
                # =====================================

                if response_data.get(
                    "intent"
                ) == "dashboard":

                    st.header(
                        "📊 AI Dashboard"
                    )

                    for widget in response_data.get(
                        "widgets",
                        []
                    ):

                        st.subheader(
                            widget.get(
                                "title",
                                "Widget"
                            )
                        )

                        if widget.get(
                            "error"
                        ):

                            st.error(
                                widget["error"]
                            )

                            continue

                        result_table = (
                            widget.get(
                                "result",
                                []
                            )
                        )

                        chart_info = (
                            widget.get(
                                "chart"
                            )
                        )

                        if result_table:

                            st.dataframe(
                                result_table,
                                use_container_width=True
                            )

                        if chart_info:

                            render_chart(
                                chart_info,
                                result_table
                            )

                    st.stop()

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