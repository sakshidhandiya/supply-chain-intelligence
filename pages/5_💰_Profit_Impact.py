# ================================
# 💰 PROFIT IMPACT DASHBOARD
# ================================

import streamlit as st
import pandas as pd
import numpy as np

from utils.data_loader import load_data   # ✅ correct import

st.set_page_config(page_title="Profit Impact", layout="wide")

st.title("💰 Profit Impact of Delivery Delays")
st.markdown("Measure how **delays affect revenue and profitability**")

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

# ================================
# 🎛️ FILTERS
# ================================
st.sidebar.header("📊 Filters")

region_filter = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Order Region"].unique()),
    default=sorted(df["Order Region"].unique())
)

category_filter = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category Name"].unique()),
    default=sorted(df["Category Name"].unique())
)

filtered_df = df[
    (df["Order Region"].isin(region_filter)) &
    (df["Category Name"].isin(category_filter))
]

# ================================
# 📊 SPLIT DATA
# ================================
on_time_df = filtered_df[filtered_df["Late_delivery_risk"] == 0]
delayed_df = filtered_df[filtered_df["Late_delivery_risk"] == 1]

# ================================
# 📊 KPI SECTION
# ================================
st.subheader("📊 Profit Comparison")

col1, col2, col3 = st.columns(3)

avg_profit_on_time = on_time_df["Order Profit Per Order"].mean()
avg_profit_delayed = delayed_df["Order Profit Per Order"].mean()

# Avoid division error
if avg_profit_on_time != 0:
    profit_loss_pct = (
        (avg_profit_on_time - avg_profit_delayed) / abs(avg_profit_on_time)
    ) * 100
else:
    profit_loss_pct = 0

col1.metric("Avg Profit (On-Time)", f"${avg_profit_on_time:.2f}")
col2.metric("Avg Profit (Delayed)", f"${avg_profit_delayed:.2f}")
col3.metric("Profit Loss %", f"{profit_loss_pct:.2f}%")

# ================================
# 💸 TOTAL IMPACT
# ================================
st.subheader("💸 Total Business Impact")

total_profit_on_time = on_time_df["Order Profit Per Order"].sum()
total_profit_delayed = delayed_df["Order Profit Per Order"].sum()

total_loss = total_profit_on_time - total_profit_delayed

col1, col2 = st.columns(2)

col1.metric("Total Profit (On-Time)", f"${total_profit_on_time:,.0f}")
col2.metric("Total Profit (Delayed)", f"${total_profit_delayed:,.0f}")

st.error(f"💥 Estimated Profit Leakage: ${total_loss:,.0f}")

# ================================
# 📉 FUNNEL
# ================================
st.subheader("📉 Revenue Leakage Funnel")

total_orders = len(filtered_df)
delayed_orders = len(delayed_df)

funnel_df = pd.DataFrame({
    "Stage": ["Total Orders", "Delayed Orders"],
    "Count": [total_orders, delayed_orders]
})

st.bar_chart(funnel_df.set_index("Stage"))

# ================================
# 📊 PROFIT DISTRIBUTION
# ================================
st.subheader("📊 Profit Distribution")

st.line_chart(filtered_df["Order Profit Per Order"])

# ================================
# 🧠 INSIGHTS
# ================================
st.subheader("🧠 Key Insights")

st.info(f"""
📉 Delayed orders generate lower profit  

💰 Profit drops by ~{profit_loss_pct:.1f}% due to delays  

📦 Delays impact revenue + customer experience  

📌 Recommendations:
• Improve delivery timelines  
• Prioritize high-value orders  
• Reduce delays in critical categories  
""")

# ================================
# 🚨 ALERT
# ================================
st.subheader("🚨 Financial Risk Alert")

if profit_loss_pct > 20:
    st.error("🚨 High financial risk due to delays!")
elif profit_loss_pct > 10:
    st.warning("⚠ Moderate profit impact")
else:
    st.success("✅ Low financial impact")

# ================================
# 📊 FOOTER
# ================================
st.markdown("---")
st.caption("Profit intelligence connects operations with business outcomes 💰")