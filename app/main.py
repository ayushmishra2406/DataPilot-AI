

import streamlit as st
from PIL import Image
from app_pages.upload import show as upload_page
from app_pages.cleaning import show as cleaning_page
from app_pages.dashboard import show as dashboard_page
from app_pages.analytics import show as analytics_page
from app_pages.ml import show as ml_page
from app_pages.reports import show as reports_page

logo = Image.open("assets/logo.png")


def load_css():

    with open("app/styles/style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )



st.set_page_config(
    page_title="DataPilot AI",
    page_icon="📊",
    layout="wide"
)

load_css() 

st.sidebar.image(
    logo,
    width=180
)

st.sidebar.title("DataPilot AI")
st.sidebar.caption("Business Intelligence Platform")

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

    col1, col2 = st.columns([1, 5])

    with col1:
        st.image(logo, width=100)

    with col2:
        st.title("DataPilot AI")
        st.subheader("AI-Powered Business Intelligence Platform")

    st.markdown("---")

    st.markdown(
        """
## Welcome 👋

**DataPilot AI** is an end-to-end Business Intelligence platform built using
Python and Streamlit.

The application allows users to upload datasets,
clean data, visualize insights,
train machine learning models,
and export professional reports.
"""
    )

    st.markdown("---")

    st.header("🚀 Key Features")

    c1, c2 = st.columns(2)

    with c1:

        st.success("📁 Upload CSV Dataset")

        st.success("🧹 Data Cleaning")

        st.success("📊 Interactive Dashboard")

    with c2:

        st.success("📈 Advanced Analytics")

        st.success("🤖 Machine Learning")

        st.success("📄 Reports & Export")

    st.markdown("---")

    st.header("🛠 Technology Stack")

    tech1, tech2, tech3 = st.columns(3)

    with tech1:

        st.info(
            """
### Backend

• Python

• Pandas

• NumPy
"""
        )

    with tech2:

        st.info(
            """
### Visualization

• Plotly

• Streamlit

• ReportLab
"""
        )

    with tech3:

        st.info(
            """
### Machine Learning

• Scikit-Learn

• Random Forest

• Linear Models
"""
        )

    st.markdown("---")

    st.header("📈 Project Statistics")

    a, b, c, d = st.columns(4)

    with a:
        st.metric("Modules", "6")

    with b:
        st.metric("Features", "20+")

    with c:
        st.metric("ML Models", "4")

    with d:
        st.metric("Exports", "3")

    st.markdown("---")

    st.caption(
        "Developed using Python • Streamlit • Plotly • Scikit-Learn"
    )

elif page == "📁 Upload Dataset":
    upload_page()

elif page == "🧹 Data Cleaning":
    cleaning_page()

elif page == "📊 Dashboard":
    st.write("Reached Dashboard block")
    dashboard_page()

elif page == "📈 Analytics":
    analytics_page()

elif page == "🤖 Machine Learning":
    ml_page()

elif page == "📄 Reports":
    reports_page()