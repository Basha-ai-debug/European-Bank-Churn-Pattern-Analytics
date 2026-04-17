import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="European Bank Churn Analytics", layout="wide", page_icon="🏦", initial_sidebar_state="expanded")

# PREMIUM DARK MODE CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0d1321 0%, #1a1a2e 100%);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 34px !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #e0e0e0 0%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px !important;
        color: #a0a8b8 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #7c8db0 !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1422 0%, #161c2d 100%);
        border-right: 1px solid #2a3042;
    }
    
    h1, h2, h3, h4 {
        color: #e8eef2 !important;
        font-weight: 600 !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #161c2d 0%, #1e2538 100%);
        border-radius: 16px;
        padding: 22px;
        border: 1px solid #2a3042;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #3a6ea5;
    }
    
    .metric-card h3 {
        color: #e8eef2 !important;
        margin: 0;
        font-size: 28px;
    }
    
    .metric-card p {
        color: #a0a8b8;
        margin: 8px 0 0 0;
        font-size: 13px;
    }
    
    .metric-card small {
        color: #5a6a85;
        font-size: 11px;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #1a2942 0%, #1e3354 100%);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #2a4060;
        border-left: 4px solid #3a86ff;
    }
    
    .insight-box h3 {
        color: #e8eef2 !important;
        margin-bottom: 15px;
    }
    
    .insight-box ul, .insight-box ol {
        color: #c0c8d8;
        margin: 0;
        padding-left: 20px;
    }
    
    .insight-box li {
        margin: 8px 0;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #1a2a3a 0%, #1e3348 100%);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #2a4055;
        border-left: 4px solid #2a9d8f;
    }
    
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #3a6ea5, #5a8ab5, #3a6ea5, transparent);
        margin: 25px 0;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #161c2d 0%, #1e2538 100%);
        border-radius: 16px;
        border: 1px solid #2a3042;
    }
    
    .footer p {
        color: #7c8db0;
        margin: 0;
    }
    
    /* Plotly chart background */
    .plotly-chart {
        background: transparent;
    }
    
    /* Sidebar text */
    .sidebar-text {
        color: #a0a8b8 !important;
    }
    
    hr {
        border-color: #2a3042;
    }
</style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("""
<div style='background: linear-gradient(135deg, #0f1422 0%, #1a1a2e 100%); padding: 30px; border-radius: 20px; margin-bottom: 30px; border: 1px solid #2a3042; text-align: center;'>
    <h1 style='color: #e8eef2; margin: 0; font-size: 32px;'>🏦 Customer Segmentation & Churn Pattern Analytics</h1>
    <p style='color: #7c8db0; margin: 12px 0 0 0;'>European Banking - Unified Mentor Project | Premium Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('European_Bank_Cleaned_With_Segments.csv')
    return df

df = load_data()

# Sidebar Filters
st.sidebar.markdown("# 🔍 Filter Dashboard")
st.sidebar.markdown("---")

selected_geo = st.sidebar.multiselect("📍 Geography", df['Geography'].unique(), default=df['Geography'].unique())
selected_gender = st.sidebar.multiselect("👤 Gender", df['Gender'].unique(), default=df['Gender'].unique())
age_range = st.sidebar.slider("📅 Age Range", int(df['Age'].min()), int(df['Age'].max()), (18, 92))
credit_range = st.sidebar.slider("📊 Credit Score Range", int(df['CreditScore'].min()), int(df['CreditScore'].max()), (350, 850))

# Apply filters
df_filtered = df[
    df['Geography'].isin(selected_geo) & 
    df['Gender'].isin(selected_gender) &
    (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1]) &
    (df['CreditScore'] >= credit_range[0]) & (df['CreditScore'] <= credit_range[1])
]

if len(df_filtered) == 0:
    st.warning("⚠️ No data matches your filters. Please adjust your selection.")
    st.stop()

# Calculate KPIs
total = len(df_filtered)
churned = df_filtered['Exited'].sum()
churn_rate = (churned / total) * 100
retained = total - churned

germany_data = df_filtered[df_filtered['Geography'] == 'Germany']
germany_rate = (germany_data['Exited'].sum() / len(germany_data)) * 100 if len(germany_data) > 0 else 0

inactive_data = df_filtered[df_filtered['IsActiveMember'] == 0]
inactive_rate = (inactive_data['Exited'].sum() / len(inactive_data)) * 100 if len(inactive_data) > 0 else 0

active_data = df_filtered[df_filtered['IsActiveMember'] == 1]
active_rate = (active_data['Exited'].sum() / len(active_data)) * 100 if len(active_data) > 0 else 0

# KPI Row
st.markdown("## 📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{total:,}</h3>
        <p>Total Customers</p>
        <small>Filtered from {len(df):,}</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{churn_rate:.1f}%</h3>
        <p>Overall Churn Rate</p>
        <small>{churned:,} customers lost</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{germany_rate:.1f}%</h3>
        <p>🇩🇪 Germany Churn</p>
        <small>Highest risk region</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{inactive_rate:.1f}%</h3>
        <p>📉 Inactive Members</p>
        <small>{inactive_rate/active_rate:.1f}x vs Active</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Row 1: Geography and Age
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌍 Churn Rate by Country")
    geo_churn = df_filtered.groupby('Geography')['Exited'].agg(['sum', 'count']).reset_index()
    geo_churn.columns = ['Geography', 'Churned', 'Total']
    geo_churn['Rate'] = (geo_churn['Churned'] / geo_churn['Total']) * 100
    
    fig = px.bar(geo_churn, x='Geography', y='Rate', color='Geography',
                 text=geo_churn['Rate'].apply(lambda x: f'{x:.1f}%'),
                 color_discrete_map={'Germany': '#5a8ab5', 'Spain': '#4a9e8f', 'France': '#6a7a9e'},
                 title="<b>Churn Rate by Country</b>")
    fig.update_traces(textposition='outside', marker_line_width=0)
    fig.update_layout(height=450, showlegend=False, yaxis_title="Churn Rate (%)", yaxis_range=[0, 40],
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8',
                      xaxis=dict(gridcolor='#2a3042'), yaxis=dict(gridcolor='#2a3042'))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 👥 Churn Rate by Age Group")
    age_churn = df_filtered.groupby('Age_Group', observed=True)['Exited'].mean() * 100
    age_df = pd.DataFrame({'Age_Group': age_churn.index, 'Churn_Rate': age_churn.values})
    
    fig = px.bar(age_df, x='Age_Group', y='Churn_Rate', color='Churn_Rate',
                 color_continuous_scale='Blues', text=age_df['Churn_Rate'].apply(lambda x: f'{x:.1f}%'),
                 title="<b>Churn Rate by Age Group</b>")
    fig.update_traces(textposition='outside')
    fig.update_layout(height=450, yaxis_title="Churn Rate (%)", yaxis_range=[0, 60],
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8',
                      xaxis=dict(gridcolor='#2a3042'), yaxis=dict(gridcolor='#2a3042'))
    st.plotly_chart(fig, use_container_width=True)

# Row 2: Balance and Credit Score
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💰 Churn by Balance Segment")
    bal_churn = df_filtered.groupby('Balance_Segment', observed=True)['Exited'].mean() * 100
    bal_df = pd.DataFrame({'Segment': bal_churn.index, 'Churn_Rate': bal_churn.values})
    
    fig = px.pie(bal_df, values='Churn_Rate', names='Segment', title='<b>Churn Distribution by Balance</b>',
                 hole=0.4, color_discrete_sequence=['#5a8ab5', '#4a9e8f', '#7a6a8e'])
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont_color='#e8eef2')
    fig.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📈 Churn by Credit Score")
    credit_churn = df_filtered.groupby('Credit_Score_Band', observed=True)['Exited'].mean() * 100
    credit_df = pd.DataFrame({'Score_Band': credit_churn.index, 'Churn_Rate': credit_churn.values})
    
    fig = px.line(credit_df, x='Score_Band', y='Churn_Rate', markers=True,
                  title='<b>Churn Rate Trend by Credit Score</b>')
    fig.update_traces(line=dict(width=3, color='#5a8ab5'), marker=dict(size=10, color='#4a9e8f', symbol='circle'))
    fig.update_layout(height=450, yaxis_title="Churn Rate (%)", yaxis_range=[0, 30],
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8',
                      xaxis=dict(gridcolor='#2a3042'), yaxis=dict(gridcolor='#2a3042'))
    st.plotly_chart(fig, use_container_width=True)

# Row 3: Tenure and Products
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⏰ Churn by Tenure")
    tenure_churn = df_filtered.groupby('Tenure_Group', observed=True)['Exited'].mean() * 100
    tenure_df = pd.DataFrame({'Tenure': tenure_churn.index, 'Churn_Rate': tenure_churn.values})
    
    fig = px.bar(tenure_df, x='Tenure', y='Churn_Rate', color='Churn_Rate',
                 color_continuous_scale='Tealgrn', text=tenure_df['Churn_Rate'].apply(lambda x: f'{x:.1f}%'),
                 title="<b>Churn Rate by Customer Tenure</b>")
    fig.update_traces(textposition='outside')
    fig.update_layout(height=450, yaxis_title="Churn Rate (%)",
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8',
                      xaxis=dict(gridcolor='#2a3042'), yaxis=dict(gridcolor='#2a3042'))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📦 Churn by Number of Products")
    product_churn = df_filtered.groupby('NumOfProducts')['Exited'].mean() * 100
    product_df = pd.DataFrame({'Products': product_churn.index, 'Churn_Rate': product_churn.values})
    
    fig = px.bar(product_df, x='Products', y='Churn_Rate', color='Churn_Rate',
                 color_continuous_scale='Oranges', text=product_df['Churn_Rate'].apply(lambda x: f'{x:.1f}%'),
                 title="<b>Churn Rate by Product Count</b>")
    fig.update_traces(textposition='outside')
    fig.update_layout(height=450, yaxis_title="Churn Rate (%)", yaxis_range=[0, 100],
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8',
                      xaxis=dict(gridcolor='#2a3042'), yaxis=dict(gridcolor='#2a3042'))
    st.plotly_chart(fig, use_container_width=True)

# High-Value Analysis
st.markdown("---")
st.markdown("## 💎 High-Value Customer Analysis")

high_balance_threshold = df_filtered['Balance'].quantile(0.8)
high_value = df_filtered[df_filtered['Balance'] >= high_balance_threshold]
hv_churn_rate = (high_value['Exited'].sum() / len(high_value)) * 100 if len(high_value) > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{len(high_value):,}</h3>
        <p>High-Value Customers</p>
        <small>Top 20% by Balance</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{hv_churn_rate:.1f}%</h3>
        <p>HV Churn Rate</p>
        <small>Premium customers at risk</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>€{high_value['Balance'].sum():,.0f}</h3>
        <p>Balance at Risk</p>
        <small>Total HV balance</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    hv_churned_balance = high_value[high_value['Exited']==1]['Balance'].mean() if len(high_value[high_value['Exited']==1]) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <h3>€{hv_churned_balance:,.0f}</h3>
        <p>Avg Lost per HV</p>
        <small>Per churned customer</small>
    </div>
    """, unsafe_allow_html=True)

# Gender and Heatmap
st.markdown("---")
st.markdown("## 👫 Advanced Analytics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👥 Churn Rate by Gender")
    gender_churn = df_filtered.groupby('Gender')['Exited'].mean() * 100
    gender_df = pd.DataFrame({'Gender': gender_churn.index, 'Churn_Rate': gender_churn.values})
    
    fig = px.bar(gender_df, x='Gender', y='Churn_Rate', color='Gender',
                 text=gender_df['Churn_Rate'].apply(lambda x: f'{x:.1f}%'),
                 color_discrete_map={'Female': '#9a8ab5', 'Male': '#5a8ab5'},
                 title="<b>Churn Rate by Gender</b>")
    fig.update_traces(textposition='outside')
    fig.update_layout(height=400, yaxis_title="Churn Rate (%)",
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8',
                      xaxis=dict(gridcolor='#2a3042'), yaxis=dict(gridcolor='#2a3042'))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🔥 Churn Heatmap: Geography × Age")
    heatmap_data = df_filtered.groupby(['Geography', 'Age_Group'], observed=True)['Exited'].mean().unstack() * 100
    fig = px.imshow(heatmap_data, text_auto='.1f', aspect="auto", 
                    color_continuous_scale='Blues',
                    title="<b>Churn Rate Heatmap - Geography vs Age</b>")
    fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8')
    st.plotly_chart(fig, use_container_width=True)

# Interactive Risk Explorer
st.markdown("---")
st.markdown("## 🎯 Customer Risk Explorer")

sample_size = min(1000, len(df_filtered))
risk_sample = df_filtered.sample(sample_size)
risk_sample['Risk_Level'] = risk_sample['Exited'].map({0: 'Low Risk', 1: 'High Risk'})

fig = px.scatter(risk_sample, x='Age', y='CreditScore', size='Balance', color='Risk_Level',
                 hover_data=['Geography', 'Gender', 'NumOfProducts', 'IsActiveMember', 'Balance'],
                 color_discrete_map={'Low Risk': '#4a9e8f', 'High Risk': '#5a8ab5'},
                 title="<b>Customer Risk Explorer - Hover for details</b>",
                 labels={'CreditScore': 'Credit Score', 'Age': 'Age', 'Balance': 'Balance (€)'})
fig.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c0c8d8',
                  xaxis=dict(gridcolor='#2a3042'), yaxis=dict(gridcolor='#2a3042'))
st.plotly_chart(fig, use_container_width=True)

# Insights Section
st.markdown("---")
st.markdown("## 📌 Strategic Insights & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="insight-box">
        <h3>📊 Key Findings</h3>
        <ul>
            <li><b>Germany</b> has <b style="color: #8ab5d8;">{germany_rate:.1f}% churn</b> - Highest among regions</li>
            <li><b>Age 46-60</b> shows <b style="color: #8ab5d8;">{age_churn['46-60']:.1f}% churn</b> - Critical segment</li>
            <li><b>Inactive members</b> are <b style="color: #8ab5d8;">{inactive_rate/active_rate:.1f}x more likely</b> to churn</li>
            <li><b>3-4 products</b> = <b style="color: #8ab5d8;">{product_churn[3]:.1f}% churn</b> - Product bundling issue</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="recommendation-box">
        <h3>💡 Recommendations</h3>
        <ol>
            <li>Launch retention campaigns in Germany</li>
            <li>Engage inactive members with personalized offers</li>
            <li>Create loyalty benefits for age 46-60 customers</li>
            <li>Simplify product bundles to 2 products</li>
            <li>Monitor high-balance customers proactively</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🏦 <b>Customer Segmentation & Churn Pattern Analytics</b> | Unified Mentor | European Central Bank</p>
    <p style="font-size: 12px; margin-top: 8px;">Premium Dark Mode Dashboard | Professional Banking Analytics</p>
</div>
""", unsafe_allow_html=True)
