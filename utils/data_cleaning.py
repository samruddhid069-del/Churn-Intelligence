from pathlib import Path
import html, re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'exported_churn_data.csv'

def load_data(path=DATA_PATH):
    path = Path(path)
    if not path.exists(): raise FileNotFoundError(f'Dataset not found: {path}')
    df = pd.read_csv(path, dtype={'customerid':'string'})
    df.columns = [re.sub(r'\s+','_',html.unescape(str(c)).strip().lstrip('*')).lower() for c in df.columns]
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].map(lambda v: re.sub(r'^\*+','',v.strip()) if isinstance(v,str) else v).replace('',pd.NA)
    for col in ['monthly_charges','ltv','churn_score','churn_flag','escalations','csat_score','complaint_count']:
        if col in df.columns: df[col] = pd.to_numeric(df[col],errors='coerce')
    for col in ['subscription_start_date','renewal_date','cancellation_date','dob','complaint_date']:
        if col in df.columns: df[col] = pd.to_datetime(df[col],errors='coerce')
    if 'churn_flag' in df.columns: df['churn_flag'] = df['churn_flag'].where(df['churn_flag'].isin([0,1]))
    return df
