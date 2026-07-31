import streamlit as st
import pandas as pd
import plotly.express as px
from utils.report_generator import generate_basic_report


def show():
    st.title("📈 Analytics")
    st.caption("Deep statistical analysis of your dataset")
    st.divider()

    # ==========================================================
    # CHECK DATASET
    # ==========================================================

    if "df" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first.")
        return

    df = st.session_state["df"]

    # ==========================================================
    # DATASET SUMMARY
    # ==========================================================

    st.header("📊 Dataset Summary")
    st.caption("Basic information about the uploaded dataset.")

    numeric_columns = df.select_dtypes(include=["number"]).shape[1]
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).shape[1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Numeric Columns", numeric_columns)

    with col4:
        st.metric("Categorical Columns", categorical_columns)

    st.divider()

    # ==========================================================
    # DATA QUALITY SUMMARY
    # ==========================================================

    st.header("🧹 Data Quality Summary")
    st.caption("Overview of missing values and duplicate records.")

    total_missing = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Missing Values", total_missing)

    with col2:
        st.metric("Duplicate Rows", duplicate_rows)

    st.subheader("Missing Values by Column")

    missing_df = (
        df.isnull()
        .sum()
        .reset_index()
    )

    missing_df.columns = ["Column", "Missing Values"]

    missing_df = missing_df.sort_values(
        by="Missing Values",
        ascending=False
    )

    st.dataframe(
        missing_df,
        use_container_width=True
    )

    st.divider()

    # ==========================================================
    # DESCRIPTIVE STATISTICS
    # ==========================================================

    st.header("📈 Descriptive Statistics")
    st.caption("Statistical summary of all numerical columns.")

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        st.info("No numerical columns found in the dataset.")
    else:
        st.dataframe(
            numeric_df.describe().round(2),
            use_container_width=True
        )

    st.divider()

    # ==========================================================
    # INTERACTIVE NUMERICAL ANALYSIS
    # ==========================================================

    st.header("🔢 Interactive Numerical Analysis")
    st.caption("Analyze a numerical column in detail.")

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if numeric_cols:

        selected_col = st.selectbox(
            "Select a Numerical Column",
            numeric_cols
        )

        series = df[selected_col].dropna()

        mean = series.mean()
        median = series.median()
        mode = series.mode().iloc[0] if not series.mode().empty else "N/A"

        std = series.std()
        variance = series.var()

        minimum = series.min()
        maximum = series.max()
        data_range = maximum - minimum

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        skewness = series.skew()
        kurtosis = series.kurt()

        metric1, metric2 = st.columns(2)

        with metric1:
            st.metric("Mean", f"{mean:.2f}")
            st.metric("Median", f"{median:.2f}")
            st.metric("Mode", f"{mode}")
            st.metric("Standard Deviation", f"{std:.2f}")
            st.metric("Variance", f"{variance:.2f}")

        with metric2:
            st.metric("Minimum", f"{minimum:.2f}")
            st.metric("Maximum", f"{maximum:.2f}")
            st.metric("Range", f"{data_range:.2f}")
            st.metric("Q1", f"{q1:.2f}")
            st.metric("Q3", f"{q3:.2f}")
            st.metric("IQR", f"{iqr:.2f}")

        st.info(
            f"""
### 📌 Distribution Metrics

- **Skewness:** `{skewness:.2f}`
- **Kurtosis:** `{kurtosis:.2f}`
"""
        )

        # ==========================================================
        # DISTRIBUTION VISUALIZATIONS
        # ==========================================================

        st.subheader("📊 Distribution Visualizations")

        chart1, chart2 = st.columns(2)

        with chart1:
            fig_hist = px.histogram(
                df,
                x=selected_col,
                nbins=30,
                title=f"Distribution of {selected_col}"
            )

            st.plotly_chart(
                fig_hist,
                use_container_width=True
            )

        with chart2:
            fig_box = px.box(
                df,
                y=selected_col,
                title=f"Box Plot of {selected_col}"
            )

            st.plotly_chart(
                fig_box,
                use_container_width=True
            )

    else:
        st.warning("No numerical columns available.")

    st.divider()

    st.success("✅ Numerical analysis completed successfully.")

    # ==========================================================
# OUTLIER DETECTION
# ==========================================================

    st.subheader("🚨 Outlier Detection (IQR Method)")

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = series[
        (series < lower_bound) |
        (series > upper_bound)
    ]

    outlier_count = len(outliers)
    outlier_percentage = (outlier_count / len(series)) * 100

    metric1, metric2 = st.columns(2)

    with metric1:
        st.metric(
            "Outliers Found",
            outlier_count
        )

    with metric2:
        st.metric(
            "Outlier %",
            f"{outlier_percentage:.2f}%"
        )

    if outlier_count == 0:
        st.success("✅ No significant outliers detected.")

    else:
        st.warning(
            f"⚠️ {outlier_count} outliers were detected using the IQR method."
        )

        with st.expander("View Outlier Values"):
            st.dataframe(
                outliers.to_frame(name=selected_col),
                use_container_width=True
            )

    st.divider()

        # ==========================================================
    # SMART INSIGHTS
    # ==========================================================

    st.header("💡 Smart Insights")
    st.caption("Automatically generated insights based on the selected numerical column.")

    insights = []

    # ----------------------------------------------------------
    # Mean vs Median
    # ----------------------------------------------------------

    if abs(mean - median) < (std * 0.1 if std != 0 else 0.01):
        insights.append(
            "📌 Mean and Median are very close, indicating a fairly balanced distribution."
        )
    else:
        insights.append(
            "📌 Mean and Median differ noticeably, suggesting possible skewness or the presence of outliers."
        )

    # ----------------------------------------------------------
    # Skewness
    # ----------------------------------------------------------

    if skewness > 1:
        insights.append(
            "➡️ The distribution is highly positively skewed (long right tail)."
        )
    elif skewness > 0.5:
        insights.append(
            "➡️ The distribution is moderately positively skewed."
        )
    elif skewness < -1:
        insights.append(
            "⬅️ The distribution is highly negatively skewed (long left tail)."
        )
    elif skewness < -0.5:
        insights.append(
            "⬅️ The distribution is moderately negatively skewed."
        )
    else:
        insights.append(
            "✅ The distribution is approximately symmetric."
        )

    # ----------------------------------------------------------
    # Kurtosis
    # ----------------------------------------------------------

    if kurtosis > 3:
        insights.append(
            "📈 High kurtosis detected. Extreme values are more likely than in a normal distribution."
        )
    elif kurtosis < 0:
        insights.append(
            "📉 Low kurtosis detected. The distribution is relatively flat."
        )
    else:
        insights.append(
            "📊 Kurtosis is within a normal range."
        )

    # ----------------------------------------------------------
    # Variability
    # ----------------------------------------------------------

    coefficient_of_variation = std / abs(mean) if mean != 0 else 0

    if coefficient_of_variation < 0.20:
        insights.append(
            "📉 The data has low variability."
        )
    elif coefficient_of_variation < 0.50:
        insights.append(
            "📊 The data has moderate variability."
        )
    else:
        insights.append(
            "📈 The data has high variability."
        )

    # ----------------------------------------------------------
    # Outliers
    # ----------------------------------------------------------

    if outlier_count == 0:
        insights.append(
            "✅ No significant outliers were detected."
        )
    elif outlier_percentage < 5:
        insights.append(
            f"⚠️ {outlier_percentage:.2f}% of the data consists of outliers."
        )
    else:
        insights.append(
            f"🚨 A high number of outliers ({outlier_percentage:.2f}%) were detected."
        )

    # ----------------------------------------------------------
    # Missing Values
    # ----------------------------------------------------------

    missing_selected = int(df[selected_col].isnull().sum())

    if missing_selected == 0:
        insights.append(
            "✅ The selected column contains no missing values."
        )
    else:
        insights.append(
            f"⚠️ The selected column contains {missing_selected} missing values."
        )

    # ----------------------------------------------------------
    # Display Insights
    # ----------------------------------------------------------

    for insight in insights:
        st.info(insight)

    st.divider()

    # ==========================================================
    # DOWNLOAD ANALYSIS REPORT
    # ==========================================================

    st.header("📄 Export Analysis Report")

    report = f"""
=========================================
DataPilot AI - Numerical Analysis Report
=========================================

Selected Column : {selected_col}

-----------------------------------------
Basic Statistics
-----------------------------------------

Mean                : {mean:.2f}
Median              : {median:.2f}
Mode                : {mode}
Standard Deviation  : {std:.2f}
Variance            : {variance:.2f}

Minimum             : {minimum:.2f}
Maximum             : {maximum:.2f}
Range               : {data_range:.2f}

Q1                  : {q1:.2f}
Q3                  : {q3:.2f}
IQR                 : {iqr:.2f}

Skewness            : {skewness:.2f}
Kurtosis            : {kurtosis:.2f}

-----------------------------------------
Outlier Analysis
-----------------------------------------

Outliers Found      : {outlier_count}
Outlier Percentage  : {outlier_percentage:.2f}%

=========================================
Generated by DataPilot AI
=========================================
"""

    st.download_button(
        label="⬇️ Download Analysis Report",
        data=report,
        file_name=f"{selected_col}_analysis_report.txt",
        mime="text/plain"
    )

    st.divider()

    st.success("✅ Analytics completed successfully.")

    # ==========================================================
# CORRELATION EXPLORER
# ==========================================================

    st.header("🔗 Correlation Explorer")
    st.caption("Analyze the relationship between two numerical columns.")

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if len(numeric_cols) >= 2:

        col_x = st.selectbox(
            "Select X-axis",
            numeric_cols,
            key="corr_x"
        )

        remaining = [c for c in numeric_cols if c != col_x]

        col_y = st.selectbox(
            "Select Y-axis",
            remaining,
            key="corr_y"
        )

        correlation = df[col_x].corr(df[col_y])

        st.metric(
            "Correlation Coefficient",
            f"{correlation:.2f}"
        )

        if correlation >= 0.7:
                st.success("Strong Positive Correlation")

        elif correlation >= 0.3:
            st.info("Moderate Positive Correlation")

        elif correlation > -0.3:
            st.info("Weak or No Correlation")

        elif correlation > -0.7:
            st.warning("Moderate Negative Correlation")

        else:
            st.error("Strong Negative Correlation")

        fig = px.scatter(
            df,
            x=col_x,
            y=col_y,
            title=f"{col_x} vs {col_y}",
            trendline="ols"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning("At least two numerical columns are required.")

    # ==========================================================
# CATEGORICAL ANALYSIS
# ==========================================================

    st.header("📂 Categorical Analysis")
    st.caption("Analyze categorical columns in your dataset.")

    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if cat_cols:

        selected_cat = st.selectbox(
            "Select a Categorical Column",
            cat_cols,
            key="cat_analysis"
        )

        value_counts = df[selected_cat].value_counts(dropna=False)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Unique Categories", value_counts.shape[0])

        with col2:
            st.metric("Most Frequent", value_counts.idxmax())

        st.subheader("Category Counts")

        category_df = (
            value_counts
            .reset_index()
            .rename(columns={
                "index": selected_cat,
                selected_cat: "Count"
            })
        )

        st.dataframe(
            category_df,
            use_container_width=True
        )

        chart1, chart2 = st.columns(2)

        with chart1:

            fig_bar = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                labels={
                    "x": selected_cat,
                    "y": "Count"
                },
                title="Category Counts"
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )

        with chart2:

            fig_pie = px.pie(
                names=value_counts.index,
                values=value_counts.values,
                title="Category Distribution"
            )

            st.plotly_chart(
                fig_pie,
                use_container_width=True
            )

    else:
        st.info("No categorical columns found in the dataset.")
    

        # ==========================================================
# PDF REPORT GENERATION
# ==========================================================

    
    st.divider()

    st.header("📄 Professional PDF Report")

    st.caption(
        "Generate a professional PDF summary of the dataset."
    )

    if st.button("📄 Generate PDF Report"):

        file_name = "DataPilot_Report.pdf"

        generate_basic_report(
            file_path=file_name,
            rows=df.shape[0],
            columns=df.shape[1],
            missing_values=int(df.isnull().sum().sum()),
            duplicate_rows=int(df.duplicated().sum()),
            numeric_columns=df.select_dtypes(include=["number"]).shape[1],
            categorical_columns=df.select_dtypes(
                include=["object", "category"]
            ).shape[1]
        )

        with open(file_name, "rb") as pdf:

            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf,
                file_name=file_name,
                mime="application/pdf"
            )

        st.success("✅ PDF Report generated successfully!")