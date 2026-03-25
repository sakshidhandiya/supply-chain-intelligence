# ================================
# 🚀 INTRODUCTION PAGE (ENHANCED)
# ================================

import streamlit as st

st.set_page_config(page_title="Introduction", layout="wide")

# ================================
# 🏷️ HEADER
# ================================
st.title("🚚 AI-Powered Supply Chain Intelligence Platform")

st.markdown("""
### 📊 Transforming Supply Chain Decisions with Data & AI
""")

st.info("""
🔍 Predict delays • 🧠 Understand causes • 💰 Optimize decisions  
This platform combines **Machine Learning + Analytics + Business Intelligence**
""")

st.markdown("---")

# ================================
# 🎬 GIF / VISUAL WALKTHROUGH
# ================================
st.header("🎬 Platform Walkthrough")

st.markdown("""
👉 This demo shows how the system predicts risk and provides insights:
""")

st.image(
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdW1mZ3F6bGJ1M2l5dW8xNmN2Y3l3b2V2YzZpZ3R5eTNqZ3R2Y2d6dCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3o7btPCcdNniyf0ArS/giphy.gif",
    use_container_width=True
)

st.markdown("---")

# ================================
# 🎯 WHAT THIS PLATFORM DOES
# ================================
st.header("🎯 What This Platform Does")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='padding:20px; border-radius:12px; background-color:#f0f9ff'>
    <h4>🔮 Predict Delays</h4>
    Estimate delivery delay probability using ML models.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='padding:20px; border-radius:12px; background-color:#fff7ed'>
    <h4>🧠 Explain Causes</h4>
    Understand why delays happen using SHAP insights.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='padding:20px; border-radius:12px; background-color:#f0fdf4'>
    <h4>💰 Measure Impact</h4>
    Quantify profit loss and business impact.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ================================
# 🧭 HOW TO USE
# ================================
st.header("🧭 How to Use This Platform")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔹 Step 1: Predict
    - Enter order details  
    - Get delay probability  

    ### 🔹 Step 2: Understand
    - View AI explanations  
    - Identify key drivers  
    """)

with col2:
    st.markdown("""
    ### 🔹 Step 3: Explore
    - 📍 Geo analysis  
    - ⏱ Lead time insights  
    - 📦 Category risks  

    ### 🔹 Step 4: Optimize
    - Use simulator  
    - Test scenarios  
    """)

st.markdown("---")

# ================================
# 🧱 ARCHITECTURE
# ================================
st.header("🧱 Platform Architecture")

col1, col2, col3 = st.columns(3)

col1.info("🔮 **Prediction Layer**\nML model estimates delay risk")
col2.warning("🧠 **Explainability Layer**\nSHAP identifies key drivers")
col3.success("📊 **Analytics Layer**\nInsights across regions, products, profit")

st.markdown("---")

# ================================
# ✨ KEY FEATURES (CARDS)
# ================================
st.header("✨ Key Features")

col1, col2, col3 = st.columns(3)

col1.success("🚀 Real-time Predictions\n\nInstant delay risk estimation")
col2.warning("📊 Interactive Dashboards\n\nExplore data visually")
col3.error("💡 Smart Recommendations\n\nActionable insights")

st.markdown("---")

# ================================
# 🎯 BUSINESS VALUE
# ================================
st.header("🎯 Business Value")

st.markdown("""
- 🚚 Improve delivery performance  
- 📉 Reduce operational inefficiencies  
- 💰 Minimize revenue loss  
- 📊 Enable data-driven decisions  
- ⚡ Optimize logistics strategies  
""")

st.markdown("---")

# ================================
# 🧠 ANALYST THINKING
# ================================
st.header("🧠 How to Use This Like an Analyst")

st.markdown("""
🔍 Identify Risk → Understand Cause → Analyze Context → Simulate Changes → Take Action  

This platform supports **end-to-end decision making**
""")

st.markdown("---")

# ================================
# 🚀 FINAL MESSAGE
# ================================
st.success("""
🚀 This is not just a dashboard — it is a **Decision Intelligence System** built to bridge AI and business strategy.
""")

# ================================
# 📊 FOOTER
# ================================
st.markdown("---")
st.caption("Built by Sakshi Dhandiya 🚀 | AI Supply Chain Intelligence Platform")