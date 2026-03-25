
# ================================
# 🚀 SUPPLY CHAIN INTELLIGENCE APP
# ================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import xgboost as xgb

# ================================
# 🎯 PAGE CONFIG
# ================================
st.set_page_config(page_title="Supply Chain Intelligence", layout="wide")

# ================================
# ⚡ LOAD MODEL (CACHED)
# ================================
@st.cache_resource
def load_model():
    model = joblib.load("models/xgb_model.pkl")
    features = joblib.load("models/features.pkl")
    return model, features

model, features = load_model()

# ================================
# 🏷️ TITLE
# ================================
st.title("🚚 Supply Chain Intelligence Platform")
st.markdown("### Predict delay risk • Optimize decisions • Improve profitability")

# ================================
# 📥 SIDEBAR INPUTS
# ================================
st.sidebar.header("📊 Input Parameters")

shipping_mode = st.sidebar.selectbox(
    "Shipping Mode",
    ["Standard Class", "Second Class", "First Class", "Same Day"]
)

region = st.sidebar.selectbox(
    "Order Region",
    [
        "Western Europe", "Eastern Europe", "South Asia",
        "Southeast Asia", "West Africa", "Central Africa",
        "North Africa", "South America", "Central America",
        "US Center", "West of USA", "East of USA"
    ]
)

market = st.sidebar.selectbox(
    "Market",
    ["Europe", "LATAM", "Pacific Asia", "USCA", "Africa"]
)

category = st.sidebar.selectbox(
    "Category",
    ["Apparel", "Electronics", "Sports", "Home", "Water Sports"]
)

planned_time = st.sidebar.slider("Planned Delivery Days", 1, 10, 3)
sales = st.sidebar.number_input("Sales Amount", value=200.0)
quantity = st.sidebar.number_input("Order Quantity", value=2)
discount_rate = st.sidebar.slider("Discount Rate", 0.0, 1.0, 0.1)

# ================================
# 🔧 FEATURE ENGINEERING
# ================================
profit_margin = 0.2
discount_impact = discount_rate * quantity
avg_price_per_item = sales / (quantity + 1)

input_dict = {
    'Planned_Time': planned_time,
    'Sales': sales,
    'Order Item Quantity': quantity,
    'Order Item Discount Rate': discount_rate,
    'Order Item Profit Ratio': profit_margin,
    'Profit_Margin': profit_margin,
    'Discount_Impact': discount_impact,
    'Avg_Price_per_Item': avg_price_per_item,
    'Order_Month': 6,
    'Order_DayOfWeek': 2
}

input_df = pd.DataFrame([input_dict])

# ================================
# 🧠 ENCODING
# ================================
for col in features:
    if col not in input_df.columns:
        input_df[col] = 0

def safe_set(col):
    if col in input_df.columns:
        input_df[col] = 1

safe_set(f"Shipping Mode_{shipping_mode}")
safe_set(f"Order Region_{region}")
safe_set(f"Market_{market}")
safe_set(f"Category Name_{category}")

input_df = input_df[features]
input_df = input_df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(float)

# ================================
# 🔮 PREDICTION
# ================================
prob = model.predict_proba(input_df)[0][1]

# ================================
# 🎯 MAIN DASHBOARD
# ================================
st.subheader("📊 Risk Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Delay Probability", f"{prob:.2%}")

with col2:
    if prob > 0.7:
        risk = "🔴 High Risk"
    elif prob > 0.4:
        risk = "🟡 Medium Risk"
    else:
        risk = "🟢 Low Risk"
    st.metric("Risk Level", risk)

with col3:
    st.metric("Planned Time", f"{planned_time} days")

st.progress(int(prob * 100))

# ================================
# 🚨 ALERT SYSTEM
# ================================
if prob > 0.7:
    st.error("🚨 High Risk: Immediate action required!")
elif prob > 0.5:
    st.warning("⚠ Medium Risk: Monitor closely")
else:
    st.success("✅ Low Risk: System operating efficiently")

# ================================
# 💡 ACTION ENGINE
# ================================
st.subheader("💡 Smart Recommendations")

actions = []

if planned_time > 5:
    actions.append("Reduce planned delivery time")

if shipping_mode == "Standard Class":
    actions.append("Switch to faster shipping mode")

if discount_rate > 0.3:
    actions.append("Optimize discount strategy")

if quantity > 3:
    actions.append("Split shipment")

if actions:
    for a in actions:
        st.write(f"✔ {a}")
else:
    st.success("No action needed 🚀")

# ================================
# 🧠 SHAP EXPLAINABILITY
# ================================
st.subheader("🧠 AI Explanation")

try:
    dmatrix = xgb.DMatrix(input_df, feature_names=input_df.columns.tolist())
    booster = model.get_booster()
    shap_values = booster.predict(dmatrix, pred_contribs=True)

    shap_array = shap_values[:, :-1]

    shap_df = pd.DataFrame({
        "Feature": input_df.columns,
        "Impact": shap_array[0]
    })

    shap_df["Abs Impact"] = shap_df["Impact"].abs()
    shap_df = shap_df.sort_values(by="Abs Impact", ascending=False).head(5)

    st.markdown("### 🔍 Key Drivers")

    for _, row in shap_df.iterrows():
        sign = "➕" if row["Impact"] > 0 else "➖"
        st.write(f"{sign} {row['Feature']}")

    fig, ax = plt.subplots()
    shap_df.set_index("Feature")["Impact"].plot(kind="barh", ax=ax)
    st.pyplot(fig)

except Exception as e:
    st.error("SHAP failed")
    st.write(str(e))

# ================================
# 💰 BUSINESS IMPACT
# ================================
st.subheader("💰 Business Impact")

if prob > 0.7:
    st.write("• High risk of revenue loss")
    st.write("• Customer dissatisfaction likely")
elif prob > 0.4:
    st.write("• Moderate operational risk")
else:
    st.write("• Efficient supply chain performance")

# ================================
# 📊 FOOTER
# ================================
st.markdown("---")
st.markdown("Built by Sakshi Dhandiya 🚀")