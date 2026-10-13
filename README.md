# Churn Intelligence Dashboard

Streamlit portfolio project for customer churn analysis, interactive visualisations, a baseline machine-learning model, and downloadable reports.

## Setup on Windows / VS Code
1. Put your `exported_churn_data.csv` in the `data` folder.
2. Open the terminal in this project root.
3. Create a virtual environment if needed: `py -m venv .venv`
4. Install packages: ` .\.venv\Scripts\python.exe -m pip install -r requirements.txt`
5. Run: ` .\.venv\Scripts\python.exe -m streamlit run app.py`

Streamlit automatically shows scripts in `pages/` in the sidebar.

## Dataset
The CSV should include `churn_flag` coded 0 = retained and 1 = churned for churn metrics and model training. Optional fields include `customerid`, `churn_score`, `plan_type`, `contract_type`, `state`, `monthly_charges`, `ltv`, `complaint_count`, `csat_score`, and `cancellation_reason`.

## Model notes
The prediction page trains a baseline logistic regression pipeline and evaluates it on a held-out test set. IDs, cancellation details, the existing churn score, and selected dates are excluded as potential leakage sources. Review the actual meaning and timing of every feature before interpreting the model. This is an educational project, not a validated production decision system.

## Chatbot
The chatbot is rule-based and answers a limited set of data questions. It does not use an external AI API.
