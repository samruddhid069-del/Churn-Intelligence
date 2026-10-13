
from theme import apply_theme

apply_theme()
import streamlit as st
import pandas as pd
from utils.data_cleaning import load_data
from utils.visualizations import churn_donut, risk_bar, churn_by_group
from utils.chatbot import answer_question

# Page Settings
st.set_page_config(
    page_title="Churn Intelligence",
    page_icon="📊",
    layout="wide"
)

# Custom Design
# st.markdown("""
# <style>
# /* Main background */
# .stApp {
#     background-color: #0B1220;
#     color: #F1F5F9;
# }

# /* Sidebar */
# [data-testid="stSidebar"] {
#     background-color: #101A2B;
#     border-right: 1px solid #263449;
# }

# /* Headings */
# h1, h2, h3 {
#     color: #F1F5F9 !important;
# }

# /* KPI cards */
# [data-testid="stMetric"] {
#     background-color: #151F32;
#     padding: 20px;
#     border-radius: 14px;
#     border: 1px solid #263449;
# }

# /* KPI values */
# [data-testid="stMetricValue"] {
#     color: #2DD4BF !important;
#     font-weight: 700;
# }

# /* Labels and descriptions */
# [data-testid="stMetricLabel"],
# [data-testid="stCaptionContainer"] {
#     color: #A9B8CC !important;
# }

# /* Buttons */
# .stButton > button,
# .stDownloadButton > button {
#     background-color: #0F766E;
#     color: white;
#     border: none;
#     border-radius: 9px;
#     padding: 10px 18px;
# }

#  /* Button hover */
# .stButton > button:hover,
# .stDownloadButton > button:hover {
#     background-color: #14B8A6;
#     color: #0B1220;
#     border: none;
# }

# /* Data table */
# [data-testid="stDataFrame"] {
#     border: 1px solid #263449;
#     border-radius: 10px;
# }

# /* Input fields */
# .stTextInput input,
# .stNumberInput input,
# [data-baseweb="select"] > div {
#     background-color: #151F32;
# }

# /* Dividers */
# hr {
#     border-color: #263449;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <style>
# /* Main background */
# .stApp {
#     background-color: #F5F7FB;
#     color: #172033;
# }

# /* Main content */
# .main .block-container {
#     padding-top: 2rem;
#     padding-bottom: 2rem;
# }

# /* Headings */
# h1, h2, h3 {
#     color: #172033 !important;
#     font-weight: 700;
# }

# # /* Sidebar */
# # [data-testid="stSidebar"] {
# #     background-color: #FFFFFF;
# #     border-right: 1px solid #E2E8F0;
# # }

# /* Metric cards */
# [data-testid="stMetric"] {
#     background-color: #FFFFFF;
#     padding: 20px;
#     border: 1px solid #E2E8F0;
#     border-radius: 12px;
#     box-shadow: 0 2px 8px rgba(23, 32, 51, 0.04);
# }

# [data-testid="stMetricLabel"] {
#     color: #64748B !important;
# }

# [data-testid="stMetricValue"] {
#     color: #2563EB !important;
#     font-weight: 700;
# }

# /* Buttons */
# .stButton > button,
# .stDownloadButton > button,
# .stFormSubmitButton > button {
#     background-color: #2563EB;
#     color: #FFFFFF;
#     border: 1px solid #2563EB;
#     border-radius: 8px;
#     font-weight: 600;
# }

# .stButton > button:hover,
# .stDownloadButton > button:hover,
# .stFormSubmitButton > button:hover {
#     background-color: #1D4ED8;
#     color: #FFFFFF;
#     border-color: #1D4ED8;
# }

# /* Input fields */
# .stTextInput input,
# .stNumberInput input,
# .stTextArea textarea {
#     background-color: #FFFFFF;
#     color: #172033;
#     border: 1px solid #CBD5E1;
#      border-radius: 8px;
# }

# /* Tables */
# [data-testid="stDataFrame"] {
#     background-color: #FFFFFF;
#     border: 1px solid #E2E8F0;
#     border-radius: 10px;
# }

# /* Tabs */
# .stTabs [data-baseweb="tab"] {
#     color: #475569;
# }

# .stTabs [aria-selected="true"] {
#     color: #2563EB !important;
# }

# /* Dividers */
# hr {
#     border-color: #E2E8F0;
# }

# /* Links */
# a {
#     color: #2563EB !important;
# }
# </style>
# """, unsafe_allow_html=True)


# Dashboard Heading
st.title("📊 Churn Intelligence Dashboard")
st.caption("Customer Retention • Churn Analysis • Business Insights")

# Load Dataset
try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Dataset not found. Put exported_churn_data.csv "
        "inside the data/ folder."
    )
    st.stop()

if df.empty:
    st.warning("Dataset is empty.")
    st.stop()

# Sidebar Filters
st.sidebar.header("🔎 Dashboard Filters")

filtered = df.copy()

filter_columns = [
    "country",
    "state",
    "plan_type",
    "contract_type",
    "gender",
    "subscription_type"
]

for col in filter_columns:
    if col in filtered.columns:
        options = sorted(
            filtered[col].dropna().astype(str).unique().tolist()
        )

        selected = st.sidebar.multiselect(
            col.replace("_", " ").title(),
            options,
            default=options
        )

        filtered = filtered[
            filtered[col].astype("string").isin(selected)
        ]

# Churn Risk Filter
if "churn_score" in filtered.columns:
    filtered["Churn Risk"] = pd.cut(
        filtered["churn_score"],
        bins=[-1, 39, 69, 100],
        labels=["Low", "Medium", "High"]
    ).astype("string")

    risks = st.sidebar.multiselect(
        "Churn Risk",
        ["Low", "Medium", "High"],
        default=["Low", "Medium", "High"]
    )

    filtered = filtered[
        filtered["Churn Risk"].isin(risks)
    ]

# Business Overview
st.subheader("📌 Business Overview")

customer_count = (
    filtered["customerid"].nunique()
    if "customerid" in filtered.columns
    else len(filtered)
)

# Calculate churn and retention
if "churn_flag" in filtered.columns:
    valid_churn = filtered["churn_flag"].dropna()

    if not valid_churn.empty:
        churn_rate = valid_churn.mean() * 100
        churned_customers = int((valid_churn == 1).sum())
        retention_rate = 100 - churn_rate
    else:
        churn_rate = 0
        churned_customers = 0
        retention_rate = 0
else:
    churn_rate = 0
    churned_customers = 0
    retention_rate = 0

# Average Customer Satisfaction
avg_csat = (
    filtered["csat_score"].mean()
    if "csat_score" in filtered.columns
    else float("nan")
)

# Display KPI Cards
a, b, c, d = st.columns(4)

a.metric("Total Customers", f"{customer_count:,}")
b.metric("Churned Customers", f"{churned_customers:,}")
c.metric("Churn Rate", f"{churn_rate:.1f}%")
d.metric("Retention Rate", f"{retention_rate:.1f}%")

st.divider()

# Customer Analytics Charts
st.subheader("📈 Customer Analytics")

left, right = st.columns(2)

with left:
    st.plotly_chart(
        churn_donut(filtered),
        use_container_width=True
    )

with right:
    st.plotly_chart(
        risk_bar(filtered),
        use_container_width=True
    )

# Plan-wise Churn Analysis
if {"plan_type", "churn_flag"}.issubset(filtered.columns):
    st.subheader("📊 Churn Rate by Plan")

    st.plotly_chart(
        churn_by_group(filtered, "plan_type"),
        use_container_width=True
    )

# Customer Records
st.subheader("👥 Customer Records")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# Download Filtered Data
st.download_button(
    label="⬇️ Download Filtered CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_churn_data.csv",
    mime="text/csv"
)

# Chatbot
st.divider()
st.subheader("🤖 Churn Assistant")
st.caption(
    "Rule-based chatbot; it does not use an external AI API."
)

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input(
    "Ask about churn, customers, complaints, or satisfaction"
)

if question:
    st.session_state.chat_messages.append({
        "role": "user",
        "content": question
    })

    answer = answer_question(question, filtered)

    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()
