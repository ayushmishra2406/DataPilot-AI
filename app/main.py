

import streamlit as st
from app_pages.upload import show as upload_page
from app_pages.cleaning import show as cleaning_page
from app_pages.dashboard import show as dashboard_page
from app_pages.analytics import show as analytics_page



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
        "🧹 Data Cleaning",
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
    - 🧹 Data Cleaning 
    - 📈 Build interactive dashboards
    - 🤖 Train machine learning models
    - 📄 Generate reports
    """)

elif page == "📁 Upload Dataset":
    upload_page()

elif page == "🧹 Data Cleaning":
    cleaning_page()

elif page == "📊 Dashboard":
    st.write("Reached Dashboard block")
    dashboard_page()

elif page == "📈 Analytics":
    analytics_page()


