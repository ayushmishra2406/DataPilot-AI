import streamlit as st

print("LOADED: app/app_pages/cleaning.py")


def show():
    st.title("🧹 Data Cleaning")

    if "df" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first.")
        return

    df = st.session_state["df"]

    st.success("Dataset loaded successfully!")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("🔁 Remove Duplicate Rows")

    duplicates = df.duplicated().sum()

    st.write(f"Duplicate rows found: {duplicates}")

    if duplicates == 0:
        st.success("🎉 No duplicate rows found!")
    else:
        if st.button("Remove Duplicates"):
            cleaned_df = df.drop_duplicates()

            st.session_state["df"] = cleaned_df

            st.success(f"✅ Removed {duplicates} duplicate rows!")

            st.write("Updated Dataset")

            st.dataframe(df.head())

    st.divider()

    st.subheader("❓ Handle Missing Values")

    missing_values = df.isnull().sum().sum()

    st.write(f"Total missing values: {missing_values}")

    if missing_values == 0:
        st.success("🎉 No missing values found!")

    else:

        if st.button("Drop Rows with Missing Values"):

            cleaned_df = df.dropna()

            removed_rows = len(df) - len(cleaned_df)

            st.session_state["df"] = cleaned_df

            st.success(
                f"✅ Removed {removed_rows} rows containing missing values."
            )

            st.write("Updated Dataset")

            st.dataframe(cleaned_df.head())

    st.divider()

    st.subheader("✏️ Rename Columns")

    selected_column = st.selectbox(
        "Select a column",
        df.columns
    )

    new_column_name = st.text_input(
        "Enter new column name"
    )

    if st.button("Rename Column"):

        if new_column_name.strip() == "":
                st.error("❌ Please enter a valid column name.")

        else:

            cleaned_df = df.rename(
                columns={selected_column: new_column_name}
            )

            st.session_state["df"] = cleaned_df

            st.success(
                f"✅ '{selected_column}' renamed to '{new_column_name}'."
            )

            st.write("Updated Columns")

            st.write(cleaned_df.columns)

    st.divider()

    st.subheader("🔄 Change Data Type")

    selected_column = st.selectbox(
        "Select Column",
        df.columns,
        key="datatype_column"
    )

    new_type = st.selectbox(
        "Select Data Type",
        ["int", "float", "string"],
        key="datatype_type"
    )

    if st.button("Convert Data Type"):

        try:

            cleaned_df = df.copy()

            if new_type == "int":
                cleaned_df[selected_column] = cleaned_df[selected_column].astype(int)

            elif new_type == "float":
                cleaned_df[selected_column] = cleaned_df[selected_column].astype(float)

            elif new_type == "string":
                cleaned_df[selected_column] = cleaned_df[selected_column].astype(str)

            st.session_state["df"] = cleaned_df

            st.success(
                f"✅ '{selected_column}' converted to {new_type}."
            )

            st.write(cleaned_df.dtypes)

        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")  

    st.divider()

    st.subheader("📥 Download Cleaned Dataset")

    cleaned_df = st.session_state["df"]

    csv = cleaned_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

    
    st.divider()

    st.subheader("📈 Handle Outliers")

    numeric_columns = df.select_dtypes(include=["number"]).columns

    if len(numeric_columns) == 0:
        st.warning("No numeric columns available.")

    else:

        selected_column = st.selectbox(
            "Select Numeric Column",
            numeric_columns,
            key="outlier_column"
        )

        Q1 = df[selected_column].quantile(0.25)
        Q3 = df[selected_column].quantile(0.75)

        IQR = Q3 - Q1

        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR

        outliers = df[
            (df[selected_column] < lower_limit)
            |
            (df[selected_column] > upper_limit)
        ]

        st.write(f"Outliers Found: {len(outliers)}")

        if len(outliers) > 0:

            st.dataframe(outliers)

            if st.button("Remove Outliers"):

                cleaned_df = df[
                    (df[selected_column] >= lower_limit)
                    &
                    (df[selected_column] <= upper_limit)
                ]

                st.session_state["df"] = cleaned_df

                st.success(
                    f"✅ Removed {len(outliers)} outlier(s)."
                )

                st.dataframe(cleaned_df.head())

        else:
            st.success("🎉 No outliers detected!")  