import streamlit as st
import pandas as pd
import plotly.express as px

print("LOADED: app/app_pages/upload.py")


def show():
    st.title("Welcome")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        st.success("✅ Dataset uploaded successfully!")

        df = pd.read_csv(uploaded_file)

        st.session_state["df"] = df

        st.write(st.session_state["df"].head())

        
        tab1, tab2, tab3 = st.tabs([
            "📄 Dataset",
            "📊 Statistics",
            "📈 Visualizations"
        ])

       
        with tab1:

            st.subheader("📄 Dataset Preview")
            st.dataframe(df)

            st.subheader("📋 Column Names")

            for column in df.columns:
                st.write(f"• {column}")

            st.subheader("📌 Data Types")
            st.write(df.dtypes)

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
            st.dataframe(df.describe())

            st.subheader("🔁 Duplicate Rows")

            duplicates = df.duplicated().sum()
            st.write(f"Number of duplicate rows: {duplicates}")

            st.subheader("💾 Memory Usage")

            memory = df.memory_usage(deep=True).sum()
            st.write(f"Memory Used: {memory / 1024:.2f} KB")

            st.subheader("ℹ️ Dataset Information")

            info_df = pd.DataFrame({
                "Data Type": df.dtypes,
                "Non-Null Count": df.count()
            })

            st.dataframe(info_df)

       
        with tab3:

            st.subheader("📊 Missing Values Chart")

            missing_values = df.isnull().sum()
            missing_values = missing_values[missing_values > 0]

            if not missing_values.empty:
                st.bar_chart(missing_values)
            else:
                st.success("🎉 No missing values found!")

            st.subheader("📊 Distribution Plot")

            numeric_columns = df.select_dtypes(include=["number"]).columns

            if len(numeric_columns) > 0:

                selected_column = st.selectbox(
                    "Select a numeric column",
                    numeric_columns
                )

                fig = px.histogram(
                    df,
                    x=selected_column,
                    title=f"Distribution of {selected_column}"
                )

                st.plotly_chart(fig, use_container_width=True)

                st.subheader("📦 Box Plot")

                fig_box = px.box(
                    df,
                    y=selected_column,
                    title=f"Box Plot of {selected_column}"
                )

                st.plotly_chart(fig_box, use_container_width=True)

            else:
                st.warning("No numeric columns found in the dataset.")

            st.subheader("🔥 Correlation Heatmap")

            correlation = df.select_dtypes(include=["number"]).corr()

            fig_heatmap = px.imshow(
                correlation,
                text_auto=True,
                color_continuous_scale="RdBu_r",
                title="Correlation Heatmap"
            )

            st.plotly_chart(fig_heatmap, use_container_width=True)