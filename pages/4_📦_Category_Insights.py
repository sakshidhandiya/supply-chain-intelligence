# ================================
# 📦 CATEGORY INSIGHTS DASHBOARD
# ================================

import streamlit as st
import pandas as pd
import numpy as np

from utils.data_loader import load_data   # ✅ correct import

st.set_page_config(page_title="Category Insights", layout="wide")

st.title("📦 Category Performance & Risk Analysis")
st.markdown("Identify **high-risk product categories impacting delivery performance**")

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

market_filter = st.sidebar.multiselect(
    "Market",
    options=sorted(df["Market"].unique()),
    default=sorted(df["Market"].unique())
)

filtered_df = df[
    (df["Order Region"].isin(region_filter)) &
    (df["Market"].isin(market_filter))
]

# ================================
# 📊 CATEGORY METRICS
# ================================
category_stats = filtered_df.groupby("Category Name").agg(
    Delay_Rate=("Late_delivery_risk", "mean"),
    Total_Orders=("Order Id", "count"),
    Avg_Sales=("Sales", "mean")
).sort_values(by="Delay_Rate", ascending=False)

# ================================
# 📊 KPI SECTION
# ================================
st.subheader("📊 Key Category Metrics")

col1, col2, col3 = st.columns(3)

top_category = category_stats.index[0]
top_delay = category_stats.iloc[0]["Delay_Rate"]

best_category = category_stats.index[-1]
best_delay = category_stats.iloc[-1]["Delay_Rate"]

total_categories = len(category_stats)

col1.metric("Total Categories", total_categories)
col2.metric("Highest Risk Category", top_category)
col3.metric("Lowest Risk Category", best_category)

# ================================
# 📊 DELAY RATE CHART
# ================================
st.subheader("📊 Delay Rate by Category")
st.bar_chart(category_stats["Delay_Rate"])

# ================================
# 📦 ORDER VOLUME
# ================================
st.subheader("📦 Order Volume by Category")
st.bar_chart(category_stats["Total_Orders"])

# ================================
# 💰 SALES IMPACT
# ================================
st.subheader("💰 Average Sales by Category")
st.bar_chart(category_stats["Avg_Sales"])

# ================================
# 🧠 INSIGHTS
# ================================
st.subheader("🧠 Key Insights")

st.info(f"""
🔴 **Highest Risk Category:** {top_category} ({top_delay:.2%})

🟢 **Best Performing Category:** {best_category} ({best_delay:.2%})

📌 Business Implications:
• High-risk categories may need better inventory planning  
• Packaging/logistics issues may exist  
• Demand-supply mismatch possible  

📊 Recommendation:
Focus improvements on **{top_category}**
""")

# ================================
# 🚨 RISK SEGMENTATION
# ================================
st.subheader("🚨 Category Risk Segmentation")

def classify_risk(x):
    if x > 0.6:
        return "High Risk"
    elif x > 0.3:
        return "Medium Risk"
    else:
        return "Low Risk"

category_stats["Risk_Level"] = category_stats["Delay_Rate"].apply(classify_risk)

st.dataframe(category_stats)

# ================================
# 🔍 DRILL DOWN
# ================================
st.subheader("🔍 Drill Down")

selected_category = st.selectbox("Choose Category", category_stats.index)

category_df = filtered_df[filtered_df["Category Name"] == selected_category]

st.write(f"### Details for {selected_category}")
st.dataframe(category_df.head(100))

# ================================
# 📊 FOOTER
# ================================
st.markdown("---")
st.caption("Category intelligence enables smarter product strategy 📦")