# ================================
# ⏱ LEAD TIME ANALYSIS DASHBOARD
# ================================

import streamlit as st
import pandas as pd
import numpy as np

from utils.data_loader import load_data   # ✅ centralized loader

st.set_page_config(page_title="Lead Time Analysis", layout="wide")

st.title("⏱ Lead Time & Delivery Efficiency")
st.markdown("Analyze **planned vs actual delivery performance**")

# ================================
# ✅ LOAD DATA (FIRST THING)
# ================================
df = load_data()

# ================================
# 🧪 SAFETY CHECK
# ================================
if df is None or df.empty:
    st.error("Dataset not loaded properly")
    st.stop()

# ================================
# 🧹 DATA PREP
# ================================
df = df.copy()

df["Delay_Gap"] = (
    df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]
)

# ================================
# 🎛️ FILTERS
# ================================
st.sidebar.header("⚙️ Filters")

region_filter = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Order Region"].unique()),
    default=sorted(df["Order Region"].unique())
)

shipping_filter = st.sidebar.multiselect(
    "Shipping Mode",
    options=sorted(df["Shipping Mode"].unique()),
    default=sorted(df["Shipping Mode"].unique())
)

filtered_df = df[
    (df["Order Region"].isin(region_filter)) &
    (df["Shipping Mode"].isin(shipping_filter))
]

# ================================
# 📊 KPI SECTION
# ================================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

avg_planned = filtered_df["Days for shipment (scheduled)"].mean()
avg_actual = filtered_df["Days for shipping (real)"].mean()
avg_gap = filtered_df["Delay_Gap"].mean()

col1.metric("Avg Planned Time", f"{avg_planned:.2f} days")
col2.metric("Avg Actual Time", f"{avg_actual:.2f} days")
col3.metric("Avg Delay Gap", f"{avg_gap:.2f} days")

# ================================
# 📊 DELAY BY REGION
# ================================
st.subheader("📍 Delay Gap by Region")

region_gap = (
    filtered_df.groupby("Order Region")["Delay_Gap"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(region_gap)

# ================================
# 🚚 SHIPPING MODE PERFORMANCE
# ================================
st.subheader("🚚 Shipping Mode Reliability")

shipping_perf = (
    filtered_df.groupby("Shipping Mode")["Delay_Gap"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(shipping_perf)

# ================================
# 📈 DISTRIBUTION
# ================================
st.subheader("📈 Delay Distribution")

dist = filtered_df["Delay_Gap"].value_counts().sort_index()
st.line_chart(dist)

# ================================
# 🧠 INSIGHTS
# ================================
st.subheader("🧠 Key Insights")

if not region_gap.empty and not shipping_perf.empty:

    worst_region = region_gap.index[0]
    best_region = region_gap.index[-1]

    worst_mode = shipping_perf.index[0]
    best_mode = shipping_perf.index[-1]

    st.info(f"""
🔴 **Worst Region:** {worst_region}  
🟢 **Best Region:** {best_region}  

🚚 **Least Reliable Mode:** {worst_mode}  
⚡ **Most Reliable Mode:** {best_mode}  

📌 Recommendations:
• Improve logistics in high-delay regions  
• Reduce dependency on slower shipping modes  
• Improve planning accuracy  
""")

# ================================
# 🚨 ALERTS
# ================================
st.subheader("🚨 Operational Alerts")

if avg_gap > 1:
    st.error("🚨 High delay gap — immediate action needed")
elif avg_gap > 0.3:
    st.warning("⚠ Moderate delays — monitor closely")
else:
    st.success("✅ Efficient operations")

# ================================
# 📊 FOOTER
# ================================
st.markdown("---")
st.caption("Operational efficiency drives supply chain performance ⚙️")