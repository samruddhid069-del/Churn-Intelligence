
import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    /* Main page background */
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #F5F7FB !important;
        color: #172033 !important;
    }

    /* Main content area */
    .stApp {
        background-color: #F5F7FB !important;
    }

    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }

    [data-testid="stSidebar"] * {
        color: #172033;
    }

    /* Headings */
    h1, h2, h3, h4, h5 {
        color: #172033 !important;
        font-weight: 700;
    }

    /* Normal text and labels */
    .stMarkdown p,
    .stCaption,
    label,
    [data-testid="stWidgetLabel"] p {
        color: #172033 !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(23, 32, 51, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
    }

    [data-testid="stMetricValue"] {
        color: #2563EB !important;
        font-weight: 700;
    }

    /* Dropdowns and multiselect boxes */
    [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #CBD5E1 !important;
        color: #172033 !important;
    }

    [data-baseweb="select"] input {
        color: #172033 !important;
    }

    /* Multiselect selected items */
    [data-baseweb="tag"] {
        background-color: #2563EB !important;
    }

    [data-baseweb="tag"] span {
        color: #FFFFFF !important;
    }

    /* Text and number inputs */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    [data-baseweb="input"] input {
        background-color: #FFFFFF !important;
        color: #172033 !important;
        border-color: #CBD5E1 !important;
    }

    /* Buttons */
    .stButton button,
    .stDownloadButton button,
    .stFormSubmitButton button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
        border-radius: 8px;
        font-weight: 600;
    }

    .stButton button:hover,
    .stDownloadButton button:hover,
    .stFormSubmitButton button:hover {
        background-color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
    }

    /* Data tables */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
    }

    /* Tabs */
    [data-testid="stTabs"] button {
        color: #475569 !important;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #2563EB !important;
        border-bottom-color: #2563EB !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
    }

    /* Dividers */
    hr {
        border-color: #E2E8F0 !important;
    }

    /* Links */
    a {
        color: #2563EB !important;
    }

    </style>
    """, unsafe_allow_html=True)
