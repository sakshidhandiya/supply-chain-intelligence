# ================================
# 📊 EXECUTIVE SUMMARY DASHBOARD
# ================================

import streamlit as st
import pandas as pd
import numpy as np

from utils.data_loader import load_data   # ✅ correct import

st.set_page_config(page_title="Executive Summary", layout="wide")

# ================================
# ✅ LOAD DATA (ONLY ONCE)
# ================================
df = load_data()

# ================================
# 🏷️ HEADER
# ================================
st.title("📊 Executive Summary Dashboard")
st.markdown("### AI-Powered Supply Chain Intelligence Overview")

st.info("This dashboard provides a high-level view of supply chain performance, risks, and business impact.")

# ================================
# 🧹 DATA PREP
# ================================
df = df.copy()

df["Delay_Gap"] = (
    df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]
)

# ================================
# 📊 KPI CALCULATIONS
# ================================
total_orders = len(df)
delay_rate = df["Late_delivery_risk"].mean()
avg_delay_gap = df["Delay_Gap"].mean()

on_time = df[df["Late_delivery_risk"] == 0]
delayed = df[df["Late_delivery_risk"] == 1]

avg_profit_on_time = on_time["Order Profit Per Order"].mean()
avg_profit_delayed = delayed["Order Profit Per Order"].mean()

profit_loss_pct = (
    (avg_profit_on_time - avg_profit_delayed) / abs(avg_profit_on_time)
) * 100

top_region = df.groupby("Order Region")["Late_delivery_risk"].mean().idxmax()
top_category = df.groupby("Category Name")["Late_delivery_risk"].mean().idxmax()

# ================================
# 📊 KPI DISPLAY
# ================================
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Delay Rate", f"{delay_rate:.2%}")
col3.metric("Avg Delay Gap", f"{avg_delay_gap:.2f} days")
col4.metric("Profit Loss", f"{profit_loss_pct:.2f}%")

# ================================
# 📊 SECOND ROW
# ================================
col1, col2 = st.columns(2)

col1.metric("🔴 Highest Risk Region", top_region)
col2.metric("📦 Highest Risk Category", top_category)

# ================================
# 📈 TREND
# ================================
st.subheader("📈 Delay Trend Over Time")

df["order date (DateOrders)"] = pd.to_datetime(df["order date (DateOrders)"])

trend = (
    df.groupby(df["order date (DateOrders)"].dt.to_period("M"))["Late_delivery_risk"]
    .mean()
)

trend.index = trend.index.astype(str)

st.line_chart(trend)

# ================================
# 📍 REGION
# ================================
st.subheader("📍 Delay Rate by Region")

region_delay = (
    df.groupby("Order Region")["Late_delivery_risk"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(region_delay)

# ================================
# 🧠 INSIGHTS
# ================================
st.subheader("🧠 Executive Insights")

st.success(f"""
📌 **Overall Delay Rate:** {delay_rate:.1%} of orders are delayed  

📍 **Critical Region:** {top_region} requires attention  

📦 **High-Risk Category:** {top_category} drives delays  

💰 **Financial Impact:** Profit drops by ~{profit_loss_pct:.1f}%  

---

### 🎯 Recommendations:

• Improve logistics in high-risk regions  
• Optimize shipping modes  
• Reduce delay gap  
• Focus on high-value orders  
""")

# ================================
# 📊 FOOTER
# ================================
st.markdown("---")
st.caption("Built by Sakshi Dhandiya 🚀")