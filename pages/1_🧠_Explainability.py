# ================================
# 🧠 EXPLAINABILITY DASHBOARD
# ================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import xgboost as xgb

from utils.data_loader import load_data  # ✅ centralized loader
st.set_page_config(page_title="Explainability", layout="wide")

st.title("🧠 Explainability Dashboard")
st.markdown("Understand **why delays happen across the entire supply chain**")

# ================================
# ⚡ LOAD DATA & MODEL
# ================================
df = load_data()   # ✅ ONLY ONCE

@st.cache_resource
def load_model():
    model = joblib.load("models/xgb_model.pkl")
    features = joblib.load("models/features.pkl")
    return model, features

model, features = load_model()

# ================================
# 🧪 SAFETY CHECK
# ================================
if df is None or df.empty:
    st.error("Dataset not loaded properly")
    st.stop()

# ================================
# 🎯 PREPARE DATA FOR SHAP
# ================================
sample_df = df.sample(min(1000, len(df)), random_state=42)

X = sample_df.copy()
X = X.reindex(columns=features, fill_value=0)
X = X.apply(pd.to_numeric, errors='coerce').fillna(0).astype(float)

# ================================
# 🧠 SHAP CALCULATION
# ================================
st.subheader("🔍 Key Drivers of Delay Risk")

shap_df = None  # ✅ initialize

try:
    dmatrix = xgb.DMatrix(X, feature_names=X.columns.tolist())
    booster = model.get_booster()

    shap_values = booster.predict(dmatrix, pred_contribs=True)
    shap_array = shap_values[:, :-1]

    shap_mean = np.abs(shap_array).mean(axis=0)

    shap_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": shap_mean
    })

    shap_df = shap_df.sort_values(by="Importance", ascending=False).head(10)

    # ================================
    # 📊 VISUALIZATION
    # ================================
    col1, col2 = st.columns([2, 1])

    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(shap_df["Feature"], shap_df["Importance"])
        ax.invert_yaxis()
        ax.set_title("Top Features Driving Delay Risk")
        st.pyplot(fig)

    with col2:
        st.markdown("### 📌 Top Insights")
        for _, row in shap_df.head(5).iterrows():
            st.write(f"🔹 {row['Feature']} strongly impacts delays")

except Exception as e:
    st.error("SHAP calculation failed")
    st.write(str(e))

# ================================
# 📊 FEATURE INTERPRETATION
# ================================
st.subheader("📖 Business Interpretation")

st.info("""
• Shipping mode and planned delivery time are major drivers of delay  
• High discount and large quantity orders increase risk  
• Certain regions consistently show higher delay probability  
""")

# ================================
# 🎯 DRIVER CARDS
# ================================
if shap_df is not None and not shap_df.empty:
    st.subheader("🚀 Top Delay Drivers")

    col1, col2, col3 = st.columns(3)

    col1.metric("Top Driver", shap_df.iloc[0]["Feature"])
    col2.metric("2nd Driver", shap_df.iloc[1]["Feature"])
    col3.metric("3rd Driver", shap_df.iloc[2]["Feature"])

# ================================
# 📊 FOOTER
# ================================
st.markdown("---")
st.caption("Explainability builds trust in AI predictions 🚀")