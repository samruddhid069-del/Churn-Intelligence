from theme import apply_theme

apply_theme()

import streamlit as st
from utils.data_cleaning import load_data
from utils.visualizations import churn_donut,risk_bar,churn_by_group
st.set_page_config(page_title='Overview',page_icon='📊',layout='wide')
st.title('📊 Overview')
try: df=load_data()
except FileNotFoundError as e: st.error(str(e)); st.stop()
a,b,c=st.columns(3)
a.metric('Customers',f"{df['customerid'].nunique():,}" if 'customerid' in df else f'{len(df):,}')
b.metric('Churn Rate',f"{df['churn_flag'].mean()*100:.1f}%" if 'churn_flag' in df and df['churn_flag'].notna().any() else 'N/A')
c.metric('Average Monthly Charges',f"{df['monthly_charges'].mean():,.2f}" if 'monthly_charges' in df else 'N/A')
x,y=st.columns(2); x.plotly_chart(churn_donut(df),use_container_width=True); y.plotly_chart(risk_bar(df),use_container_width=True)
if {'plan_type','churn_flag'}.issubset(df.columns): st.plotly_chart(churn_by_group(df,'plan_type'),use_container_width=True)
