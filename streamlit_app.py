import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="European Bank Churn Analytics", layout="wide", page_icon="🏦")

# Premium Dark Mode CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0d1321 0%, #1a1a2e 100%); }
    [data-testid="stMetricValue"] { font-size: 34px !important; font-weight: 700 !important; color: #5a8ab5 !important; }
    [data-testid="stMetricLabel"] { color: #a0a8b8 !important; }
    h1, h2, h3 { color: #e8eef2 !important; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f1422 0%, #161c2d 100%); border-right: 1px solid #2a3042; }
    .st-emotion-cache-1r6slb0 { background: linear-gradient(135deg, #161c2d 0%, #1e2538 100%); border-radius: 16px; padding: 20px; border: 1px solid #2a3042; }
</style>
""", unsafe_allow_html=True)

st.title("🏦 Customer Segmentation & Churn Pattern Analytics")
st.markdown("### European Banking - Unified Mentor Project | Premium Analytics Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv('European_Bank_Cleaned_With_Segments.csv')

df = load_data()

# Sidebar Filters
st.sidebar.markdown("# 🔍 Filter Dashboard")
selected_geo = st.sidebar.multiselect("📍 Geography", df['Geography'].unique(), default=df['Geography'].unique())
selected_gender = st.sidebar.multiselect("👤 Gender", df['Gender'].unique(), default=df['Gender'].unique())
age_range = st.sidebar.slider("📅 Age Range", int(df['Age'].min()), int(df['Age'].max()), (18, 92))
credit_range = st.sidebar.slider("📊 Credit Score Range", int(df['CreditScore'].min()), int(df['CreditScore'].max()), (350, 850))

df_filtered = df[df['Geography'].isin(selected_geo) & df['Gender'].isin(selected_gender) &
                 (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1]) &
                 (df['CreditScore'] >= credit_range[0]) & (df['CreditScore'] <= credit_range[1])]

if len(df_filtered) == 0:
    st.warning("⚠️ No data matches your filters")
    st.stop()

total = len(df_filtered)
churned = df_filtered['Exited'].sum()
churn_rate = (churned / total) * 100
germany_rate = (df_filtered[df_filtered['Geography']=='Germany']['Exited'].sum() / len(df_filtered[df_filtered['Geography']=='Germany'])) * 100 if len(df_filtered[df_filtered['Geography']=='Germany']) > 0 else 0
inactive_rate = (df_filtered[df_filtered['IsActiveMember']==0]['Exited'].sum() / len(df_filtered[df_filtered['IsActiveMember']==0])) * 100 if len(df_filtered[df_filtered['IsActiveMember']==0]) > 0 else 0
active_rate = (df_filtered[df_filtered['IsActiveMember']==1]['Exited'].sum() / len(df_filtered[df_filtered['IsActiveMember']==1])) * 100 if len(df_filtered[df_filtered['IsActiveMember']==1]) > 0 else 0

st.markdown("## 📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("📊 Total Customers", f"{total:,}")
with col2: st.metric("⚠️ Overall Churn Rate", f"{churn_rate:.1f}%")
with col3: st.metric("🇩🇪 Germany Churn", f"{germany_rate:.1f}%")
with col4: st.metric("📉 Inactive Churn", f"{inactive_rate:.1f}%", delta=f"{inactive_rate/active_rate:.1f}x vs Active")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🌍 Churn Rate by Country")
    geo_churn = df_filtered.groupby('Geography')['Exited'].mean() * 100
    fig = px.bar(x=geo_churn.index, y=geo_churn.values, text=geo_churn.values.round(1), color=geo_churn.index, color_discrete_map={'Germany':'#5a8ab5','Spain':'#4a9e8f','France':'#6a7a9e'})
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 👥 Churn Rate by Age Group")
    age_churn = df_filtered.groupby('Age_Group', observed=True)['Exited'].mean() * 100
    fig = px.bar(x=age_churn.index, y=age_churn.values, text=age_churn.values.round(1), color=age_churn.values, color_continuous_scale='Blues')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8')
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 💰 Churn by Balance Segment")
    bal_churn = df_filtered.groupby('Balance_Segment', observed=True)['Exited'].mean() * 100
    fig = px.pie(values=bal_churn.values, names=bal_churn.index, hole=0.4, color_discrete_sequence=['#5a8ab5','#4a9e8f','#7a6a8e'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📈 Churn by Credit Score")
    credit_churn = df_filtered.groupby('Credit_Score_Band', observed=True)['Exited'].mean() * 100
    fig = px.line(x=credit_churn.index, y=credit_churn.values, markers=True)
    fig.update_traces(line=dict(width=3, color='#5a8ab5'), marker=dict(size=10, color='#4a9e8f'))
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8')
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### ⏰ Churn by Tenure")
    tenure_churn = df_filtered.groupby('Tenure_Group', observed=True)['Exited'].mean() * 100
    fig = px.bar(x=tenure_churn.index, y=tenure_churn.values, text=tenure_churn.values.round(1), color=tenure_churn.values, color_continuous_scale='Teal')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📦 Churn by Products")
    product_churn = df_filtered.groupby('NumOfProducts')['Exited'].mean() * 100
    fig = px.bar(x=product_churn.index, y=product_churn.values, text=product_churn.values.round(1), color=product_churn.values, color_continuous_scale='Oranges')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("## 💎 High-Value Customer Analysis")
high_balance_threshold = df_filtered['Balance'].quantile(0.8)
high_value = df_filtered[df_filtered['Balance'] >= high_balance_threshold]
hv_churn_rate = (high_value['Exited'].sum() / len(high_value)) * 100 if len(high_value) > 0 else 0

col1, col2, col3 = st.columns(3)
with col1: st.metric("💎 High-Value Customers", f"{len(high_value):,}")
with col2: st.metric("⚠️ HV Churn Rate", f"{hv_churn_rate:.1f}%")
with col3: st.metric("💰 Balance at Risk", f"€{high_value['Balance'].sum():,.0f}")

st.markdown("---")
st.markdown("## 📌 Strategic Insights")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **🔴 CRITICAL FINDINGS:**
    - Germany: 32.4% churn (Highest)
    - Age 46-60: 51.1% churn (Critical)
    - Inactive members: 1.9x more likely to churn
    - 3-4 products: 82-100% churn
    """)
with col2:
    st.markdown("""
    **💡 RECOMMENDATIONS:**
    1. Launch retention campaigns in Germany
    2. Engage inactive members
    3. Create loyalty benefits for age 46-60
    4. Simplify product bundles to 2 products
    5. Monitor high-balance customers
    """)

st.caption("Project: Customer Segmentation & Churn Pattern Analytics | Unified Mentor | European Central Bank")
