# ================================
# 📍 GEO ANALYSIS DASHBOARD
# ================================

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

from utils.data_loader import load_data   # ✅ centralized loader

st.set_page_config(page_title="Geo Analysis", layout="wide")

st.title("📍 Geographic Delay Analysis")
st.markdown("Identify **regional bottlenecks and delay hotspots**")

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

# Drop missing coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# ================================
# 🎛️ SIDEBAR FILTERS
# ================================
st.sidebar.header("🌍 Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Order Region"].unique()),
    default=sorted(df["Order Region"].unique())
)

market_filter = st.sidebar.multiselect(
    "Select Market",
    options=sorted(df["Market"].unique()),
    default=sorted(df["Market"].unique())
)

filtered_df = df[
    (df["Order Region"].isin(region_filter)) &
    (df["Market"].isin(market_filter))
]

# ================================
# 📊 KPI SECTION
# ================================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

total_orders = len(filtered_df)
delay_rate = filtered_df["Late_delivery_risk"].mean()

if not filtered_df.empty:
    high_risk_region = (
        filtered_df.groupby("Order Region")["Late_delivery_risk"]
        .mean()
        .idxmax()
    )
else:
    high_risk_region = "N/A"

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Avg Delay Rate", f"{delay_rate:.2%}")
col3.metric("Highest Risk Region", high_risk_region)

# ================================
# 🗺️ MAP VISUALIZATION
# ================================
st.subheader("🗺️ Delay Hotspot Map")

# Sample for performance
map_df = filtered_df.sample(min(5000, len(filtered_df)), random_state=42)

# Color coding
map_df["color"] = map_df["Late_delivery_risk"].apply(
    lambda x: [255, 0, 0] if x == 1 else [0, 180, 0]
)

map_df["size"] = 50

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position='[Longitude, Latitude]',
    get_color='color',
    get_radius="size",
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1.2,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "text": "Region: {Order Region}\nDelay: {Late_delivery_risk}"
    }
)

st.pydeck_chart(deck)

# ================================
# 📊 REGION ANALYSIS
# ================================
st.subheader("📊 Delay Rate by Region")

region_delay = (
    filtered_df.groupby("Order Region")["Late_delivery_risk"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(region_delay)

# ================================
# 🧠 SMART INSIGHTS
# ================================
st.subheader("🧠 Key Insights")

if not region_delay.empty:
    top_region = region_delay.index[0]
    top_value = region_delay.iloc[0]

    low_region = region_delay.index[-1]
    low_value = region_delay.iloc[-1]

    st.info(f"""
🔴 **Highest Risk Region:** {top_region} ({top_value:.2%})

🟢 **Best Performing Region:** {low_region} ({low_value:.2%})

📌 Recommendations:
• Improve logistics in high-risk regions  
• Optimize delivery routes  
• Use faster shipping modes where needed  
""")

# ================================
# 🚨 TOP RISK TABLE
# ================================
st.subheader("🚨 Top Risk Regions")

top_table = region_delay.reset_index().head(5)
top_table.columns = ["Region", "Delay Rate"]

st.dataframe(top_table)

# ================================
# 📊 FOOTER
# ================================
st.markdown("---")
st.caption("Geo intelligence enables smarter supply chain decisions 🌍")