import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)



def show():
    st.title("🤖 Machine Learning")
    st.caption("Train and evaluate machine learning models")
    st.divider()

    if "df" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first.")
        return

    df = st.session_state["df"]

    st.success("✅ Dataset loaded successfully!")

    st.header("📊 Dataset Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    st.divider()

    st.header("📄 Dataset Preview")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.divider()

    st.header("🎯 Target Selection")
    st.caption("Choose the column you want the model to predict.")

    target_column = st.selectbox(
        "Target Column",
        df.columns
    )

    st.success(f"Selected Target: **{target_column}**")

    # ==========================================================
# PROBLEM TYPE DETECTION
# ==========================================================

    st.divider()

    st.header("🧠 Problem Type Detection")

    if pd.api.types.is_numeric_dtype(df[target_column]):

        problem_type = "Regression"

        st.success(
            "📈 Regression Problem Detected"
        )

    else:

        problem_type = "Classification"

        st.success(
            "📊 Classification Problem Detected"
        )

    st.info(
        f"Selected Problem Type: **{problem_type}**"
    )

    # ==========================================================
# FEATURE SELECTION
# ==========================================================

    st.divider()

    st.header("📋 Feature Selection")
    st.caption("Select the input features for model training.")

    # Remove the target column from available features
    available_features = [
        column for column in df.columns
        if column != target_column
    ]

    selected_features = st.multiselect(
        "Choose Feature Columns",
        available_features,
        default=available_features
    )

    if len(selected_features) == 0:

        st.warning(
            "⚠️ Please select at least one feature."
        )

    else:

        st.success(
            f"{len(selected_features)} feature(s) selected."
        )

        st.write("### Selected Features")

        st.write(selected_features)

        # ==========================================================
# DATA PREPROCESSING
# ==========================================================

    st.divider()

    st.header("🧹 Data Preprocessing")
    st.caption("Preparing the dataset for machine learning.")

    if len(selected_features) == 0:

        st.warning("Please select at least one feature.")

    else:

            # ==========================================================
    # CREATE FEATURES (X) AND TARGET (y)
    # ==========================================================

        X = df[selected_features].copy()

        y = df[target_column]

    # ==========================================================
# HANDLE MISSING VALUES
# ==========================================================

# Numeric columns
        numeric_cols = X.select_dtypes(
            include=["number"]
        ).columns

        for col in numeric_cols:
            X[col] = X[col].fillna(
                X[col].median()
            )

        # Categorical columns
        categorical_cols = X.select_dtypes(
            include=["object", "category"]
        ).columns

        for col in categorical_cols:
            X[col] = X[col].fillna(
                X[col].mode()[0]
            )

        st.success("✅ Missing values handled successfully!")

    # ==========================================================
    # ENCODE CATEGORICAL FEATURES
    # ==========================================================

        categorical_cols = X.select_dtypes(
            include=["object", "category"]
        ).columns

        if len(categorical_cols) > 0:

            X = pd.get_dummies(
                X,
                columns=categorical_cols,
                drop_first=True
            )

        st.success("✅ Features and Target created successfully!")

        st.success("✅ Categorical features encoded successfully!")

        st.success("✅ Features and Target created successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Feature Columns",
                X.shape[1]
            )

        with col2:
            st.metric(
                "Training Samples",
                X.shape[0]
            )

        st.subheader("📋 Feature Preview")

        st.dataframe(
            X.head(),
            use_container_width=True
        )

        st.subheader("🎯 Target Preview")

        st.dataframe(
            y.head(),
            use_container_width=True
        )

        # ==========================================================
    # MODEL SELECTION
    # ==========================================================

        st.divider()

        st.header("🧠 Model Selection")
        st.caption("Choose a machine learning algorithm.")

        if problem_type == "Regression":

            models = [
                "Linear Regression",
                "Random Forest Regressor"
            ]

        else:

            models = [
                "Logistic Regression",
                "Random Forest Classifier"
            ]

        selected_model = st.selectbox(
            "Select Model",
            models
        )

        st.success(
            f"Selected Model: **{selected_model}**"
        )

        # ==========================================================
    # TRAIN MODEL
    # ==========================================================

        st.divider()

        st.header("🚀 Model Training")
        st.caption("Train the selected machine learning model.")

        if st.button("Train Model"):

            # Split the dataset
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )

            # Create model
            if selected_model == "Linear Regression":
                model = LinearRegression()

            elif selected_model == "Random Forest Regressor":
                model = RandomForestRegressor(
                    random_state=42
                )

            elif selected_model == "Logistic Regression":
                model = LogisticRegression(
                    max_iter=1000
                )

            elif selected_model == "Random Forest Classifier":
                model = RandomForestClassifier(
                    random_state=42
                )

            # Train model
            model.fit(X_train, y_train)

            st.success("✅ Model trained successfully!")

            st.write("### Training Summary")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Training Samples", len(X_train))

            with col2:
                st.metric("Testing Samples", len(X_test))

            # Save objects for next phase
            st.session_state["model"] = model
            st.session_state["X_test"] = X_test
            st.session_state["y_test"] = y_test
            st.session_state["problem_type"] = problem_type
            st.session_state["selected_model"] = selected_model

        
            # ==========================================================
# MODEL EVALUATION
# ==========================================================

        if "model" in st.session_state:

            st.divider()
            st.header("📊 Model Evaluation")

            model = st.session_state["model"]
            X_test = st.session_state["X_test"]
            y_test = st.session_state["y_test"]
            problem_type = st.session_state["problem_type"]

            y_pred = model.predict(X_test)

            if problem_type == "Regression":

                mae = mean_absolute_error(y_test, y_pred)
                mse = mean_squared_error(y_test, y_pred)
                rmse = mse ** 0.5
                r2 = r2_score(y_test, y_pred)

                c1, c2 = st.columns(2)

                with c1:
                    st.metric("MAE", f"{mae:.2f}")
                    st.metric("MSE", f"{mse:.2f}")

                with c2:
                    st.metric("RMSE", f"{rmse:.2f}")
                    st.metric("R² Score", f"{r2:.2f}")

            else:

                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(
                    y_test,
                    y_pred,
                    average="weighted",
                    zero_division=0
                )

                recall = recall_score(
                    y_test,
                    y_pred,
                    average="weighted",
                    zero_division=0
                )

                f1 = f1_score(
                    y_test,
                    y_pred,
                    average="weighted",
                    zero_division=0
                )

                c1, c2 = st.columns(2)

                with c1:
                    st.metric("Accuracy", f"{accuracy:.2%}")
                    st.metric("Precision", f"{precision:.2%}")

                with c2:
                    st.metric("Recall", f"{recall:.2%}")
                    st.metric("F1 Score", f"{f1:.2%}")


                    # ==========================================================
# PREDICTION INTERFACE
# ==========================================================

        if "model" in st.session_state:

            st.divider()

            st.header("🎯 Make Prediction")
            st.caption("Enter feature values and let the trained model make a prediction.")

            model = st.session_state["model"]

            input_data = {}

            for column in selected_features:

                # Numeric Columns
                if pd.api.types.is_numeric_dtype(df[column]):

                    default_value = float(df[column].median())

                    input_data[column] = st.number_input(
                        f"{column}",
                        value=default_value
                    )

                # Categorical Columns
                else:

                    categories = (
                        df[column]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )

                    input_data[column] = st.selectbox(
                        column,
                        categories,
                        key=f"predict_{column}"
                    )

            if st.button("Predict"):

                prediction_df = pd.DataFrame([input_data])

                # Handle missing values

                numeric_cols = prediction_df.select_dtypes(
                    include=["number"]
                ).columns

                for col in numeric_cols:
                    prediction_df[col] = prediction_df[col].fillna(
                        prediction_df[col].median()
                    )

                categorical_cols = prediction_df.select_dtypes(
                    include=["object", "category"]
                ).columns

                if len(categorical_cols) > 0:

                    prediction_df = pd.get_dummies(
                        prediction_df,
                        columns=categorical_cols,
                        drop_first=True
                    )

                # Match training columns

                prediction_df = prediction_df.reindex(
                    columns=X.columns,
                    fill_value=0
                )

                prediction = model.predict(prediction_df)

                st.subheader("Prediction Result")

                if problem_type == "Regression":

                    st.success(
                        f"Predicted Value: {prediction[0]:.2f}"
                    )

                else:

                    st.success(
                        f"Predicted Class: {prediction[0]}"
                    )