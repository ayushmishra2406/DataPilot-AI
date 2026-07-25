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
        st.write("Hello")

        df = pd.read_csv(uploaded_file)

        st.dataframe(df)