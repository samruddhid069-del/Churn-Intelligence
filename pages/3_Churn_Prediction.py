from theme import apply_theme

apply_theme()

import streamlit as st
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from utils.data_cleaning import load_data


# Page Settings
st.set_page_config(
    page_title="Churn Prediction",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Churn Prediction")
st.caption("Machine Learning • Customer Risk Analysis • Retention Insights")

st.info(
    "💡 Churn Prediction Insights: Explore customer churn "
    "probabilities and identify customers who may need "
    "retention support. Predictions are estimates based "
    "on the available customer data."
)


# Load Dataset
try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Dataset not found. Please check your data folder "
        "and exported_churn_data.csv file."
    )
    st.stop()

if df.empty:
    st.warning("The dataset is empty.")
    st.stop()


# Target and Features
target = "churn_flag"

if target not in df.columns:
    st.error("Dataset needs a churn_flag column coded as 0 and 1.")
    st.stop()

excluded = {
    target,
    "customerid",
    "customer_name",
    "churn_score",
    "cancellation_date",
    "cancellation_reason",
    "complaint_date",
    "renewal_date",
    "dob"
}

features = [
    col for col in df.columns
    if col not in excluded
    and not col.endswith("_date")
    and df[col].nunique(dropna=True) > 1
]

if not features:
    st.error("No suitable features were found for model training.")
    st.stop()


# Model File Path
model_path = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "churn_model.pkl"
)

model_path.parent.mkdir(parents=True, exist_ok=True)


# Train Model
st.subheader("📊 Model Training and Evaluation")

if st.button("🚀 Train and Evaluate Model", use_container_width=True):

    data = df.dropna(subset=[target]).copy()
    data = data[data[target].isin([0, 1])]

    if len(data) < 10 or data[target].nunique() < 2:
        st.error(
            "Not enough valid records. The target must contain "
            "both 0 and 1, with sufficient records for testing."
        )
        st.stop()

    X = data[features]
    y = data[target].astype(int)

    if y.value_counts().min() < 2:
        st.error(
            "Each churn class needs at least two records."
        )
        st.stop()

    # Identify Column Types
    numeric = X.select_dtypes(include="number").columns.tolist()
    categorical = [
        col for col in X.columns if col not in numeric
    ]

    # Preprocessing
    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    transformers = []

    if numeric:
        transformers.append(("num", num_pipe, numeric))

    if categorical:
        transformers.append(("cat", cat_pipe, categorical))

    prep = ColumnTransformer(transformers)

    # Machine Learning Model
    model = Pipeline([
        ("prep", prep),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ])

    # Split Data
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.25,
            random_state=42,
            stratify=y
        )
    except ValueError as e:
        st.error(f"Cannot split data: {e}")
        st.stop()

    # Train and Evaluate
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]

    st.success("Model training and evaluation completed.")

    st.subheader("📈 Model Performance")

    a, b, c, d = st.columns(4)

    a.metric(
        "Accuracy",
        f"{accuracy_score(y_test, pred):.3f}"
    )

    b.metric(
        "Precision",
        f"{precision_score(y_test, pred, zero_division=0):.3f}"
    )

    c.metric(
        "Recall",
        f"{recall_score(y_test, pred, zero_division=0):.3f}"
    )

    d.metric(
        "F1-score",
        f"{f1_score(y_test, pred, zero_division=0):.3f}"
    )

    try:
        auc = roc_auc_score(y_test, prob)
        st.metric("ROC-AUC", f"{auc:.3f}")
    except ValueError:
        st.info("ROC-AUC is unavailable for this test split.")

    # Confusion Matrix
    st.subheader("🔍 Confusion Matrix")

    cm = confusion_matrix(
        y_test,
        pred,
        labels=[0, 1]
    )

    cm_df = pd.DataFrame(
        cm,
        index=["Actual Retained", "Actual Churned"],
        columns=["Predicted Retained", "Predicted Churned"]
    )

    st.dataframe(
        cm_df,
        use_container_width=True
    )

    # Classification Report
    st.subheader("📋 Classification Report")

    report = classification_report(
        y_test,
        pred,
        output_dict=True,
        zero_division=0
    )

    st.dataframe(
        pd.DataFrame(report).transpose().round(3),
        use_container_width=True
    )

    # Save Trained Model
    joblib.dump(model, model_path)

    st.success(
        "Model saved successfully! You can now score customer records."
    )


# Score Customer
if model_path.exists():

    st.divider()
    st.subheader("🔮 Customer Churn Prediction")

    st.write(
        "Enter customer details to estimate their probability of churn."
    )

    model = joblib.load(model_path)

    with st.form("prediction_form"):

        row = {}

        for col in features:

            if pd.api.types.is_numeric_dtype(df[col]):

                default = (
                    float(df[col].median())
                    if df[col].notna().any()
                    else 0.0
                )

                row[col] = st.number_input(
                    col.replace("_", " ").title(),
                    value=default
                )

            else:

                opts = sorted(
                    df[col].dropna().astype(str).unique().tolist()
                )

                if opts:
                    row[col] = st.selectbox(
                        col.replace("_", " ").title(),
                        opts
                    )
                else:
                    row[col] = st.text_input(
                        col.replace("_", " ").title()
                    )

        submit = st.form_submit_button(
            "🔍 Estimate Churn Probability",
            use_container_width=True
        )

    if submit:

        customer = pd.DataFrame(
            [row],
            columns=features
        )

        probability = float(
            model.predict_proba(customer)[0][1]
        )

        st.subheader("Prediction Result")

        st.metric(
            "Estimated Churn Probability",
            f"{probability:.1%}"
        )

        st.progress(probability)

        if probability >= 0.7:
            st.error(
                "🔴 High Estimated Risk — Consider reviewing "
                "this customer's needs and retention options."
            )

        elif probability >= 0.4:
            st.warning(
                "🟠 Medium Estimated Risk — Monitor this "
                "customer and review their experience."
            )

        else:
            st.success(
                "🟢 Low Estimated Risk — Continue regular "
                "customer engagement."
            )

        st.caption(
            "This is a model estimate, not a guarantee of future churn."
        )

else:
    st.info(
        "Train the model first using the button above "
        "to enable customer scoring."
    )
