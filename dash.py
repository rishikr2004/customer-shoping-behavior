import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(layout="wide")

st.markdown("""
<style>

.main-title {
    text-align: center;
    background: linear-gradient(90deg, #c04cc0, #7b2cbf);
    padding: 18px;
    border-radius: 12px;
    color: white;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 20px;
}

.card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #7b2cbf;
}

.metric-label {
    font-size: 14px;
    color: gray;
}

.chart-box {
    background-color: #111827;
    padding: 15px;
    border-radius: 15px;
    margin-top: 10px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

.chart-title {
    color: white;
    font-size: 16px;
    margin-bottom: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown('<div class="main-title">Customer Behavior Dashboard</div>', unsafe_allow_html=True)

# LOAD DATA
df = pd.read_csv("customers.csv")

#  SIDEBAR FILTERS

st.sidebar.header("Filters")

subscription = st.sidebar.multiselect("Subscription Status",
                                      df["subscription_status"].unique(),
                                      default=df["subscription_status"].unique())

gender = st.sidebar.multiselect("Gender",
                               df["gender"].unique(),
                               default=df["gender"].unique())

category = st.sidebar.multiselect("Category",
                                 df["category"].unique(),
                                 default=df["category"].unique())

shipping = st.sidebar.multiselect("Shipping Type",
                                 df["shipping_type"].unique(),
                                 default=df["shipping_type"].unique())

# FILTER DATA

filtered_df = df[
    (df["subscription_status"].isin(subscription)) &
    (df["gender"].isin(gender)) &
    (df["category"].isin(category)) &
    (df["shipping_type"].isin(shipping))
]

if filtered_df.empty:
    st.warning("No data available")
    st.stop()

# KPI CARDS 
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-value">{filtered_df['customer_id'].nunique()}</div>
        <div class="metric-label">Number of Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-value">${filtered_df['purchase_amount'].mean():.2f}</div>
        <div class="metric-label">Average Purchase</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="metric-value">{filtered_df['review_rating'].mean():.2f}</div>
        <div class="metric-label">Average Rating</div>
    </div>
    """, unsafe_allow_html=True)


col4, col5, col6 = st.columns(3, gap="large")

#  Subscription
with col4:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">% Customers by Subscription</div>', unsafe_allow_html=True)

    sub_data = filtered_df["subscription_status"].value_counts().reset_index()
    sub_data.columns = ["subscription_status", "count"]

    fig1 = px.pie(sub_data, names="subscription_status", values="count", hole=0.6)
    fig1.update_layout(template="plotly_dark")

    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

#  Revenue by Category
with col5:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Revenue by Category</div>', unsafe_allow_html=True)

    rev_cat = filtered_df.groupby("category")["purchase_amount"].sum().reset_index()
    fig2 = px.bar(rev_cat, x="category", y="purchase_amount")
    fig2.update_layout(template="plotly_dark")

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

#  Sales by Category
with col6:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Sales by Category</div>', unsafe_allow_html=True)

    sales_cat = filtered_df["category"].value_counts().reset_index()
    sales_cat.columns = ["category", "count"]

    fig3 = px.bar(sales_cat, x="category", y="count")
    fig3.update_layout(template="plotly_dark")

    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


col7, col8 = st.columns(2, gap="large")

# 🔹 Revenue by Age
with col7:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Revenue by Age Group</div>', unsafe_allow_html=True)

    rev_age = filtered_df.groupby("age_groups")["purchase_amount"].sum().reset_index()
    fig4 = px.bar(rev_age, x="purchase_amount", y="age_groups", orientation="h")
    fig4.update_layout(template="plotly_dark")

    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

#  Sales by Age
with col8:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Sales by Age Group</div>', unsafe_allow_html=True)

    sales_age = filtered_df["age_groups"].value_counts().reset_index()
    sales_age.columns = ["age_groups", "count"]

    fig5 = px.bar(sales_age, x="age_groups", y="count")
    fig5.update_layout(template="plotly_dark")

    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
