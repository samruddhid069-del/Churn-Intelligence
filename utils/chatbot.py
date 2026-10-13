import pandas as pd

def answer_question(question,df):
    q=question.lower()
    if 'churn rate' in q or 'churn percentage' in q:
        return f"Churn rate in filtered data: {df['churn_flag'].mean()*100:.2f}%." if 'churn_flag' in df and df['churn_flag'].notna().any() else 'Churn flag data is unavailable.'
    if 'retention' in q:
        return f"Retention rate: {(1-df['churn_flag'].mean())*100:.2f}%." if 'churn_flag' in df and df['churn_flag'].notna().any() else 'Churn flag data is unavailable.'
    if 'customer' in q and any(w in q for w in ['how many','total','number']):
        return f"There are {df['customerid'].nunique() if 'customerid' in df else len(df):,} customers in the filtered data."
    if 'high risk' in q and 'churn_score' in df: return f"{int((df['churn_score']>=70).sum()):,} customers have churn_score >= 70."
    if 'complaint' in q and 'complaint_count' in df:
        total=df['complaint_count'].sum(); return f'Total recorded complaints: {total:,.0f}.' if pd.notna(total) else 'Complaint data unavailable.'
    if 'satisfaction' in q and 'csat_score' in df:
        avg=df['csat_score'].mean(); return f'Average satisfaction score: {avg:.2f}.' if pd.notna(avg) else 'Satisfaction data unavailable.'
    if 'plan' in q and 'most' in q and 'plan_type' in df:
        counts=df['plan_type'].value_counts(); return f'{counts.index[0]} has the most customers ({counts.iloc[0]:,}).' if not counts.empty else 'Plan data unavailable.'
    if 'cancellation reason' in q or 'churn reason' in q:
        reasons=df['cancellation_reason'].dropna().value_counts() if 'cancellation_reason' in df else pd.Series(dtype=int)
        return f"Most common recorded reason: {reasons.index[0]} ({reasons.iloc[0]} records)." if not reasons.empty else 'No cancellation reasons available.'
    return 'Try: What is the churn rate? How many customers are there? Which plan has the most customers? How many complaints are there? What is the most common cancellation reason?'
