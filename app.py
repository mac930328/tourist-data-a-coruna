import streamlit as st
import pandas as pd

from services.api_data import fetch_diva_data
from processing.cleaning import clean_diva_data
from analysis.eda import basic_stats

st.set_page_config(
    page_title="DIVA Data Analysis",
    layout="wide"
)

st.title("📊 Análisis DIVA – Galicia (A Coruña)")

@st.cache_data(ttl=3600)
def load_data():
    raw_df = fetch_diva_data()
    clean_df = clean_diva_data(raw_df)
    return raw_df, clean_df

with st.sidebar:
    st.header("⚙️ Opciones")
    refresh = st.button("🔄 Refrescar datos")

if refresh:
    st.cache_data.clear()

with st.spinner("Consultando API y procesando datos..."):
    raw_df, clean_df = load_data()

# ---------------- RAW DATA ----------------
st.subheader("📥 Datos originales")
st.dataframe(raw_df.head(100), width='stretch')

# ---------------- CLEAN DATA ----------------
st.subheader("🧹 Datos limpios")
st.dataframe(clean_df.head(100), width='stretch')

# ---------------- STATS ----------------
st.subheader("📈 Estadísticas descriptivas")
st.dataframe(basic_stats(clean_df), width='stretch')

# ---------------- SIMPLE VIS ----------------
num_cols = clean_df.select_dtypes(include="number").columns

if len(num_cols) > 0:
    st.subheader("📊 Visualización")
    col = st.selectbox("Columna numérica", num_cols)
    st.bar_chart(clean_df[[col]].reset_index(drop=True), width="stretch")
