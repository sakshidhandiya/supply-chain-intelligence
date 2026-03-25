import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=129igTuB5wySC4zGVs3mD8xLDjA0sqhhS"
    df = pd.read_csv(url, encoding='latin1')
    return df