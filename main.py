import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍏", layout="wide")

# --- CSS PARA LEGIBILIDAD (Mantenemos tus mejoras) ---
st.markdown("""
    <style>
    h1, h2, h3, [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }
    [data-testid="stMetricLabel"] p { color: #E0E0E0 !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #1e1e1e !important; }
    .plan-card { padding: 30px; border-radius: 15px; background-color: #ffffff; border-left: 10px solid #2e7d32; margin-bottom: 20px; }
    .plan-card h2, .plan-card p, .plan-card b { color: #1e1e1e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS CON TAGS CLÍNICOS ---
# Tags: gf = gluten free, ls = low sodium, veg = vegetariano
base_recetas = [
    {"nombre": "Tarta de {zapallito} integral", "entorno": "Oficina", "tags": ["ls"]},
    {"nombre": "Ensalada de {porotos} y {choclo}", "entorno": "Oficina", "tags": ["gf", "ls", "veg"]},
    {"nombre": "Wrap de pollo y {palta}", "entorno": "Oficina", "tags": ["ls"]},
    {"nombre": "Wok de vegetales y arroz", "entorno": "Oficina", "tags": ["gf", "ls", "veg"]},
    {"nombre": "Milanesas con puré", "entorno": "Hogar", "tags": ["ls"]},
    {"nombre": "Guiso de lentejas y calabaza", "entorno": "Hogar", "tags": ["gf", "ls", "veg"]},
    {"nombre": "Pescado al horno con vegetales", "entorno": "Hogar", "tags": ["gf", "ls"]},
    {"nombre": "Omelette de espinaca y queso", "entorno": "Hogar", "tags": ["gf", "ls", "veg"]}
]

diccionario = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "desayuno": "Mate con tostadas"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "desayuno": "Café con molletes"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "desayuno": "Pan con tomate"}
}

# --- INTERFAZ ---
st.title("🥗 Nutri-Flow: Gestión Profesional")

with st.sidebar:
    st.header("⚙️ Configuración")
    nombre = st.text_input("Paciente", value="Emanuel")
    pais = st.selectbox("País", list(diccionario.keys()))
    entorno = st.radio("Logística", ["Oficina", "Hogar"])
    
    st.divider()
    st.header("🏥 Filtros Clínicos")
    es_celiaco = st.checkbox("Celíaco (Sin TACC)")
    es_hipertenso = st.checkbox("Hipertenso (Bajo Sodio)")

# --- LÓGICA DE FILTRADO ---
if st.button("🚀 GENERAR PLAN NUTRICIONAL"):
    term = diccionario[pais]
    
    # Filtrar recetas por entorno y luego por patología
    recetas_posibles = [r for r in base_recetas if r["entorno"] == entorno]
    
    if es_celiaco:
        recetas_posibles = [r for r in recetas_posibles if "gf" in r["tags"]]
    if es_hipertenso:
        recetas_posibles = [r for r in recetas_posibles if "ls" in r["tags"]]

    if not recetas_posibles:
        st.error("No hay recetas que cumplan todos los filtros. ¡Expandamos la base!")
    else:
        plato_data = random.choice(recetas_posibles)
        plato_final = plato_data["nombre"].format(**term)
        
        # Renderizado del Plan
        st.markdown(f"""
        <div class="plan-card">
            <h2>📋 Plan Adaptado</h2>
            <p><b>Paciente:</b> {nombre} {'⚠️ (Celíaco)' if es_celiaco else ''}</p>
            <hr>
            <p><b>🌅 Desayuno:</b> {term['desayuno'] if not es_celiaco else 'Galletas de arroz con queso'}</p>
            <p><b>🍱 Almuerzo:</b> {plato_final}</p>
        </div>
        """, unsafe_allow_html=True)
