import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="European Bank Churn Analytics", layout="wide")

st.title("🏦 Customer Segmentation & Churn Pattern Analytics")
st.markdown("### European Banking - Unified Mentor Project")

df = pd.read_csv('European_Bank_Cleaned_With_Segments.csv')
st.success(f"✅ Loaded {len(df):,} customer records")

selected_geo = st.sidebar.multiselect("Geography", df['Geography'].unique(), default=df['Geography'].unique())
selected_gender = st.sidebar.multiselect("Gender", df['Gender'].unique(), default=df['Gender'].unique())
df_filtered = df[df['Geography'].isin(selected_geo) & df['Gender'].isin(selected_gender)]

if len(df_filtered) == 0:
    st.error("No data matches your filters")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
total = len(df_filtered)
churn_rate = (df_filtered['Exited'].sum() / total) * 100
germany_data = df_filtered[df_filtered['Geography'] == 'Germany']
germany_rate = (germany_data['Exited'].sum() / len(germany_data)) * 100 if len(germany_data) > 0 else 0
inactive_data = df_filtered[df_filtered['IsActiveMember'] == 0]
inactive_rate = (inactive_data['Exited'].sum() / len(inactive_data)) * 100 if len(inactive_data) > 0 else 0

with col1: st.metric("Total Customers", f"{total:,}")
with col2: st.metric("Overall Churn Rate", f"{churn_rate:.1f}%")
with col3: st.metric("Germany Churn", f"{germany_rate:.1f}%")
with col4: st.metric("Inactive Churn", f"{inactive_rate:.1f}%")

st.subheader("Churn Rate by Geography")
geo_churn = df_filtered.groupby('Geography')['Exited'].mean() * 100
fig1 = px.bar(x=geo_churn.index, y=geo_churn.values, text=geo_churn.values.round(1))
st.plotly_chart(fig1)

st.subheader("Churn Rate by Age Group")
age_churn = df_filtered.groupby('Age_Group', observed=True)['Exited'].mean() * 100
fig2 = px.bar(x=age_churn.index, y=age_churn.values, text=age_churn.values.round(1))
st.plotly_chart(fig2)

st.success("Dashboard loaded successfully!")
