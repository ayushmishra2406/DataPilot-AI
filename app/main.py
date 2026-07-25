

import streamlit as st
from pages.upload import show

st.set_page_config(
    page_title="DataPilot AI",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("📊 DataPilot AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📁 Upload Dataset",
        "📊 Dashboard",
        "📈 Analytics",
        "🤖 Machine Learning",
        "📄 Reports"
    ]
)

if page == "🏠 Home":

    st.title("📊 DataPilot AI")

    st.subheader("AI-Powered Business Intelligence Platform")

    st.write("""
    Welcome to **DataPilot AI**.

    This platform will help you:

    - 📁 Upload datasets
    - 📊 Analyze business data
    - 📈 Build interactive dashboards
    - 🤖 Train machine learning models
    - 📄 Generate reports
    """)

elif page == "📁 Upload Dataset":
    show()



