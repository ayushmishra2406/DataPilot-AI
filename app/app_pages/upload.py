import streamlit as st
import pandas as pd
import os

print("LOADED: app/app_pages/upload.py")


def show():
    st.title("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    # If a new file is uploaded
    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        os.makedirs("uploads", exist_ok=True)

        with open("uploads/latest_dataset.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state["df"] = df

        st.success("✅ Dataset uploaded successfully!")

    # If no file is uploaded, load the last saved dataset
    elif "df" not in st.session_state and os.path.exists("uploads/latest_dataset.csv"):

        df = pd.read_csv("uploads/latest_dataset.csv")
        st.session_state["df"] = df

    # If there is still no dataset
    if "df" not in st.session_state:
        st.info("👆 Please upload a CSV file to get started.")
        return

    # Use the dataframe stored in session state
    df = st.session_state["df"]

    # Create tabs
    tab1, tab2 = st.tabs([
        "📄 Dataset",
        "📊 Statistics"
    ])

    # ==========================
    # Dataset Tab
    # ==========================
    with tab1:

        st.subheader("📄 Dataset Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("📋 Column Names")

        for column in df.columns:
            st.write(f"• {column}")

        st.subheader("📌 Data Types")
        st.write(df.dtypes)

    # ==========================
    # Statistics Tab
    # ==========================
    with tab2:

        st.subheader("📊 Dataset Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        st.subheader("❓ Missing Values")

        missing_values = df.isnull().sum()
        st.dataframe(missing_values)

        st.subheader("📈 Statistical Summary")

        try:
            st.dataframe(df.describe(include="all"))
        except Exception:
            st.dataframe(df.describe())

        st.subheader("🔁 Duplicate Rows")

        duplicates = df.duplicated().sum()
        st.write(f"Number of duplicate rows: {duplicates}")

        st.subheader("💾 Memory Usage")

        memory = df.memory_usage(deep=True).sum()
        st.write(f"Memory Used: {memory / 1024:.2f} KB")

        st.subheader("ℹ️ Dataset Information")

        info_df = pd.DataFrame({
            "Data Type": df.dtypes.astype(str),
            "Non-Null Count": df.count()
        })

        st.dataframe(info_df, use_container_width=True)