import streamlit as st
import pandas as pd
import plotly.express as px


def show():
    st.title("📊 Dashboard")
    st.caption("Interactive analytics dashboard for uploaded datasets")
    st.divider()

    if "df" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first.")
        return

    # ==========================================================
    # LOAD DATA
    # ==========================================================
    df = st.session_state["df"]

    # ==========================================================
    # FILTERS
    # ==========================================================
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    st.header("📌 Overview")
    st.caption("Quick summary of your uploaded dataset")

    filtered_df = df.copy()

    if categorical_columns:
        st.subheader("🔍 Filter Data")

        filter_cols = st.columns(min(len(categorical_columns), 3))

        for i, column in enumerate(categorical_columns[:3]):

            with filter_cols[i]:

                options = ["All"] + sorted(
                    filtered_df[column]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                selected = st.selectbox(
                    column,
                    options,
                    key=f"filter_{column}"
                )

                if selected != "All":
                    filtered_df = filtered_df[
                        filtered_df[column].astype(str) == selected
                    ]

    # ==========================================================
    # KPI CARDS
    # ==========================================================
    missing_values = filtered_df.isnull().sum().sum()
    duplicate_rows = filtered_df.duplicated().sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Rows", filtered_df.shape[0])

    with col2:
        st.metric("📋 Columns", filtered_df.shape[1])

    with col3:
        st.metric("❓ Missing Values", missing_values)

    with col4:
        st.metric("🔁 Duplicate Rows", duplicate_rows)

    # ==========================================================
    # VISUALIZATIONS
    # ==========================================================
    st.divider()
    st.header("📊 Visualizations")

    st.subheader("📊 Missing Values Chart")

    missing = filtered_df.isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        st.bar_chart(missing)
    else:
        st.success("🎉 No missing values found!")

    numeric_columns = filtered_df.select_dtypes(
        include=["number"]
    ).columns

    if len(numeric_columns) > 0:

        selected_column = st.selectbox(
            "Select a numeric column",
            numeric_columns
        )

        col_left, col_right = st.columns(2)

        with col_left:

            st.subheader("📊 Distribution Plot")

            fig = px.histogram(
                filtered_df,
                x=selected_column,
                title=f"Distribution of {selected_column}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col_right:

            st.subheader("📦 Box Plot")

            fig_box = px.box(
                filtered_df,
                y=selected_column,
                title=f"Box Plot of {selected_column}"
            )

            st.plotly_chart(
                fig_box,
                use_container_width=True
            )

    else:
        st.warning("⚠️ No numeric columns found in the filtered dataset.")

    # ==========================================================
    # CORRELATION HEATMAP
    # ==========================================================
    numeric_df = filtered_df.select_dtypes(include=["number"])

    if numeric_df.shape[1] >= 2:

        st.subheader("🔥 Correlation Heatmap")

        correlation = numeric_df.corr()

        fig_heatmap = px.imshow(
            correlation,
            text_auto=True,
            color_continuous_scale="RdBu_r",
            title="Correlation Heatmap"
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True
        )

    elif numeric_df.shape[1] == 1:
        st.info(
            "Only one numeric column found. Correlation heatmap requires at least two numeric columns."
        )

    # ==========================================================
    # DATASET INFORMATION
    # ==========================================================
    st.divider()
    st.subheader("📋 Dataset Information")

    st.write("**Dataset Shape:**")
    st.write(filtered_df.shape)

    column_info = pd.DataFrame({
        "Column Name": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str).values,
        "Missing Values": filtered_df.isnull().sum().values
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )

    # ==========================================================
    # DATASET PREVIEW
    # ==========================================================
    st.divider()
    st.subheader("📄 Dataset Preview")

    st.dataframe(
        filtered_df.head(),
        use_container_width=True
    )