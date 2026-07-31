import streamlit as st
import pandas as pd
from io import BytesIO

from utils.report_generator import generate_basic_report


def show():

    st.title("📄 Reports Center")
    st.caption("Export your dataset in multiple formats.")

    st.divider()

    # ==========================================================
    # CHECK DATASET
    # ==========================================================

    if "df" not in st.session_state:

        st.warning("⚠️ Please upload a dataset first.")

        return

    df = st.session_state["df"]

    # ==========================================================
    # DATASET OVERVIEW
    # ==========================================================

    st.header("📊 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )

    with col4:
        st.metric(
            "Duplicate Rows",
            int(df.duplicated().sum())
        )

    st.divider()

    # ==========================================================
    # DATA PREVIEW
    # ==========================================================

    st.header("👀 Dataset Preview")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.divider()

    # ==========================================================
    # PDF EXPORT
    # ==========================================================

    st.header("📄 Export PDF Report")

    if st.button("Generate PDF Report"):

        file_name = "DataPilot_Report.pdf"

        generate_basic_report(
            file_path=file_name,
            rows=df.shape[0],
            columns=df.shape[1],
            missing_values=int(df.isnull().sum().sum()),
            duplicate_rows=int(df.duplicated().sum()),
            numeric_columns=df.select_dtypes(
                include=["number"]
            ).shape[1],
            categorical_columns=df.select_dtypes(
                include=["object", "category"]
            ).shape[1]
        )

        with open(file_name, "rb") as pdf:

            st.download_button(
                label="⬇️ Download PDF",
                data=pdf,
                file_name=file_name,
                mime="application/pdf"
            )

    st.divider()

    # ==========================================================
    # CSV EXPORT
    # ==========================================================

    st.header("📊 Export CSV")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="dataset.csv",
        mime="text/csv"
    )

    st.divider()

    # ==========================================================
    # EXCEL EXPORT
    # ==========================================================

    st.header("📗 Export Excel")

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Dataset"
        )

    excel_data = output.getvalue()

    st.download_button(
        label="⬇️ Download Excel",
        data=excel_data,
        file_name="dataset.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.divider()

    st.success("✅ Export Center Ready")