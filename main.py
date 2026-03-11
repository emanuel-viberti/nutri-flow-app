import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro | Gestión Clínica", page_icon="🍎", layout="wide")

# --- CSS PROFESIONAL ---
st.markdown("""
    <style>
    h1, h2, h3 { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #1e1e1e !important; font-weight: bold; }
    .day-card { 
        background-color: #ffffff; padding: 15px; border-radius: 12px; 
        border-left: 8px solid #2e7d32; margin-bottom: 25px; color: #1e1e1e !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .receta-text { font-size: 0.85em; color: #666; font-style: italic; display: block; }
    .macro-tag { font-size: 0.75em; background: #e8f5e9; color: #2e7d32; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    .metric-box { background: #f0f2f6; padding: 15px; border-radius: 10px; color: #333; border: 1px solid #ccc; margin-bottom: 10px;}
    .pi-box { background: #fff3e0; border: 1px solid #ff9800; padding: 10px; border-radius: 8px; color: #e65100; margin-bottom: 10px;}
    .stButton>button { border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db", "ls"], "receta": "200g yogur descremado + 3 cdas granola.", "pro": 8, "cho": 30},
    {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "veg", "ls"], "receta": "1 tostada integral + 1/2 palta + 1 huevo revuelto.", "pro": 12, "cho": 20},
    {"nombre": "Panqueque de avena y banana", "tags": ["db", "veg", "ls"], "receta": "1 huevo + 3 cdas avena + 1/2 banana a la sartén.", "pro": 10, "cho": 25},
    {"nombre": "Bowl de frutas y nueces", "tags": ["gf", "vgn", "db", "ls"], "receta": "Frutilla/Fresa picada + 3 nueces mariposa.", "pro": 4, "cho": 22}
]

comidas = [
    {"nombre": "Pollo al horno con calabaza", "tags": ["gf", "db", "ls", "dl"], "receta": "150g pechuga + 200g calabaza asada.", "pro": 30, "cho": 25},
    {"nombre
