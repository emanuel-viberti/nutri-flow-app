import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍏", layout="wide")

# --- CSS DEFINITIVO PARA VISIBILIDAD (Corregido) ---
st.markdown("""
    <style>
    /* Cuerpo principal */
    h1, h2, h3, [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }
    
    /* Barra lateral - Forzamos TODO a ser legible */
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown { 
        color: #1e1e1e !important; 
    }
    
    /* Forzar visibilidad del multiselect y textos de ayuda */
    [data-baseweb="tag"] { background-color: #2e7d32 !important; color: white !important; }
    span[data-baseweb="tag"] { color: white !important; }

    /* Tarjeta del Plan */
    .plan-card { 
        padding: 30px; border-radius: 15px; background-color: #ffffff; 
        border-left: 10px solid #2e7d32; margin-bottom: 20px; 
    }
    .plan-card h2, .plan-card p, .plan-card b, .plan-card li, .plan-card hr { 
        color: #1e1e1e !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS (Mantenemos la lógica de tags) ---
base_recetas = [
    {"nombre": "Tarta de {zapallito} integral", "entorno": "Oficina", "tags": ["ls"]},
    {"nombre": "Ensalada de {porotos} y {choclo}", "entorno": "Oficina", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Wrap de pollo y {palta}", "entorno": "Oficina", "tags": ["ls"]},
    {"nombre": "Wok de vegetales y arroz integral", "entorno": "Oficina", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Milanesas con puré de calabaza", "entorno": "Hogar", "tags": ["ls"]},
    {"nombre": "Guiso de lentejas nutri", "entorno": "Hogar", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Pescado al papillote con vegetales", "entorno": "Hogar", "tags": ["gf", "ls", "lc"]},
    {"nombre": "Omelette de espinaca y queso", "entorno": "Hogar", "tags": ["gf", "ls", "veg", "lc"]},
    {"nombre": "Zapallitos rellenos de carne magra", "entorno": "Hogar", "tags": ["gf", "ls", "lc"]}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "desayuno": "Mate con tostadas"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "desayuno": "Café con molletes"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "desayuno": "Pan con tomate y oliva"}
}

# --- INTERFAZ / SIDEBAR (Corregida) ---
with st.sidebar:
    st.header("👤 Ficha Clínica")
    nombre = st.text_input("Nombre", value="Emanuel")
    peso = st.number_input("Peso (kg)", value=75.0)
    talla = st.number_input("Talla (cm)", value=175)
    
    imc = peso / ((talla/100)**2)
    st.metric("IMC", f"{imc:.1f}")
    
    st.divider()
    # Volvemos al desplegable (Multiselect) que es más prolijo
    st.subheader("🏥 Condiciones")
    patologias_seleccionadas = st.multiselect(
        "Marcar patologías o alergias:",
        ["Celíaco (Sin TACC)", "Hipertenso (Bajo Sodio)", "Vegetariano", "Vegano"]
    )

    st.divider()
    pais = st.selectbox("País", list(paises.keys()))
    entorno = st.radio("Logística Almuerzo", ["Oficina", "Hogar"])

# --- LÓGICA DE FILTRADO ---
st.title("🥗 Nutri-Flow: Gestión Profesional")

if st.button("🚀 GENERAR PLAN NUTRICIONAL"):
    term = paises[pais]
    
    # Mapeo de selección a tags del sistema
    recetas_ok = [r for r in base_recetas if r["entorno"] == entorno]
    
    if "Celíaco (Sin TACC)" in patologias_seleccionadas:
        recetas_ok = [r for r in recetas_ok if "gf" in r["tags"]]
    if "Vegetariano" in patologias_seleccionadas:
        recetas_ok = [r for r in recetas_ok if "veg" in r["tags"] or "vgn" in r["tags"]]
    if "Vegano" in patologias_seleccionadas:
        recetas_ok = [r for r in recetas_ok if "vgn" in r["tags"]]
    if "Hipertenso (Bajo Sodio)" in patologias_seleccionadas:
        recetas_ok = [r for r in recetas_ok if "ls" in r["tags"]]

    if not recetas_ok:
        st.error("⚠️ No hay recetas que cumplan todos los filtros clínicos.")
    else:
        plato_data = random.choice(recetas_ok)
        plato_final = plato_data["nombre"].format(**term)
        
        st.markdown(f"""
        <div class="plan-card">
            <h2>📋 Plan para {nombre}</h2>
            <p><b>Resumen:</b> IMC {imc:.1f} | {', '.join(patologias_seleccionadas) if patologias_seleccionadas else 'Sin restricciones'}</p>
            <hr>
            <p><b>🌅 Desayuno/Merienda:</b> {term['desayuno'] if "Celíaco (Sin TACC)" not in patologias_seleccionadas else 'Galletas de arroz con hummus'}</p>
            <p><b>🍱 Almuerzo:</b> {plato_final}</p>
        </div>
        """, unsafe_allow_html=True)
