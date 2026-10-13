from theme import apply_theme

apply_theme()

import streamlit as st
import pandas as pd
from io import BytesIO
from utils.data_cleaning import load_data
st.set_page_config(page_title='Reports',page_icon='📄',layout='wide')
st.title('📄 Reports and Downloads')
try: df=load_data()
except FileNotFoundError as e: st.error(str(e)); st.stop()
summary=pd.DataFrame({'Metric':['Total rows','Unique customers','Churn rate (%)','Average monthly charges','Average LTV'],'Value':[len(df),df['customerid'].nunique() if 'customerid' in df else len(df),round(df['churn_flag'].mean()*100,2) if 'churn_flag' in df and df['churn_flag'].notna().any() else None,round(df['monthly_charges'].mean(),2) if 'monthly_charges' in df else None,round(df['ltv'].mean(),2) if 'ltv' in df else None]})
st.subheader('Summary Report'); st.dataframe(summary,use_container_width=True,hide_index=True)
st.download_button('Download cleaned data (CSV)',df.to_csv(index=False).encode(), 'cleaned_churn_data.csv','text/csv')
st.download_button('Download summary (CSV)',summary.to_csv(index=False).encode(),'churn_summary_report.csv','text/csv')
buffer=BytesIO()
with pd.ExcelWriter(buffer,engine='openpyxl') as writer: df.to_excel(writer,sheet_name='Customer Data',index=False); summary.to_excel(writer,sheet_name='Summary',index=False)
st.download_button('Download Excel report',buffer.getvalue(),'churn_report.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
