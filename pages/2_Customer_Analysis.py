from theme import apply_theme

apply_theme()
import streamlit as st
import plotly.express as px
from utils.data_cleaning import load_data
st.set_page_config(page_title='Customer Analysis',page_icon='👥',layout='wide')
st.title('👥 Customer Analysis')
try: df=load_data()
except FileNotFoundError as e: st.error(str(e)); st.stop()
for col in [c for c in ['country','state','plan_type','contract_type','gender','subscription_type'] if c in df]:
    opts=sorted(df[col].dropna().astype(str).unique()); chosen=st.multiselect(f'Filter by {col.replace("_"," ").title()}',opts,default=opts); df=df[df[col].astype('string').isin(chosen)]
if 'state' in df:
    data=df['state'].value_counts().rename_axis('State').reset_index(name='Customers')
    st.plotly_chart(px.bar(data,x='State',y='Customers',color='Customers',title='Customers by State',template='plotly_dark'),use_container_width=True)
if 'cancellation_reason' in df:
    data=df['cancellation_reason'].dropna().value_counts().rename_axis('Reason').reset_index(name='Count')
    if not data.empty: st.plotly_chart(px.bar(data,x='Count',y='Reason',orientation='h',color='Count',title='Cancellation Reasons',template='plotly_dark'),use_container_width=True)
if {'plan_type','churn_flag'}.issubset(df.columns): st.plotly_chart(px.bar(df.dropna(subset=['plan_type','churn_flag']).groupby('plan_type',observed=True)['churn_flag'].mean().mul(100).reset_index(name='Churn Rate (%)'),x='plan_type',y='Churn Rate (%)',color='Churn Rate (%)',title='Churn Rate by Plan',template='plotly_dark'),use_container_width=True)
st.dataframe(df,use_container_width=True,hide_index=True)
