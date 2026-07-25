import streamlit as st
import pandas as pd


def show():
    st.title("📁 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        st.success("✅ Dataset uploaded successfully!")
    

        df = pd.read_csv(uploaded_file)

        st.dataframe(df)

        st.subheader("📊 Dataset Summary")

        st.write("Rows:", df.shape[0])

        st.write("Columns:", df.shape[1])
