import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍏", layout="wide")

# --- CSS DEFINITIVO ---
st.markdown("""
    <style>
    h1, h2, h3, [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #1e1e1e !important; }
    .plan-card { padding: 30px; border-radius: 15px; background-color: #ffffff; border-left: 10px solid #2e7d32; margin-bottom: 20px; }
    .plan-card h2, .plan-card p, .plan-card b, .plan-card li { color: #1e1e1e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS MAESTRA (50+ VARIANTES) ---
# gf: sin tacc | ls: bajo sodio | veg: vegetariano | vgn: vegano | lc: bajo carb
base_recetas = [
    # ALMUERZOS DE OFICINA (Fáciles de recalentar o comer fríos)
    {"nombre": "Tarta de {zapallito} con masa de semillas", "entorno": "Oficina", "tags": ["ls", "veg"]},
    {"nombre": "Ensalada de {porotos}, quinoa y {choclo}", "entorno": "Oficina", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Wrap integral de pollo, {palta} y tomate", "entorno": "Oficina", "tags": ["ls"]},
    {"nombre": "Wok de arroz yamani con vegetales de estación", "entorno": "Oficina", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Buddha Bowl: Garbanzos, {palta} y arroz", "entorno": "Oficina", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Penne integral con pesto de brócoli y nueces", "entorno": "Oficina", "tags": ["ls", "veg", "vgn"]},
    {"nombre": "Hamburguesas de lentejas con ensalada mixta", "entorno": "Oficina", "tags": ["ls", "veg", "vgn"]},
    {"nombre": "Ensalada de atún, arroz y {choclo}", "entorno": "Oficina", "tags": ["gf", "ls"]},
    {"nombre": "Rollitos de berenjena rellenos de mijo", "entorno": "Oficina", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Cuscús con vegetales asados y almendras", "entorno": "Oficina", "tags": ["ls", "veg", "vgn"]},
    
    # ALMUERZOS DE HOGAR (Requieren cocción o armado al momento)
    {"nombre": "Milanesas de peceto al horno con puré mixto", "entorno": "Hogar", "tags": ["ls"]},
    {"nombre": "Guiso de lentejas con cubos de calabaza", "entorno": "Hogar", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Pescado a la plancha con rodajas de {zapallito}", "entorno": "Hogar", "tags": ["gf", "ls", "lc"]},
    {"nombre": "Omelette de espinaca, champiñones y queso", "entorno": "Hogar", "tags": ["gf", "ls", "veg", "lc"]},
    {"nombre": "Zapallitos rellenos con carne magra y queso", "entorno": "Hogar", "tags": ["gf", "ls", "lc"]},
    {"nombre": "Pechuga al limón con batatas asadas", "entorno": "Hogar", "tags": ["gf", "ls"]},
    {"nombre": "Risotto de champiñones y parmesano", "entorno": "Hogar", "tags": ["gf", "ls", "veg"]},
    {"nombre": "Berenjenas a la parmesana (sin rebozar)", "entorno": "Hogar", "tags": ["gf", "ls", "veg", "lc"]},
    {"nombre": "Cazuela de pollo con puerros y zanahoria", "entorno": "Hogar", "tags": ["gf", "ls", "lc"]},
    {"nombre": "Canelones de verdura con salsa blanca light", "entorno": "Hogar", "tags": ["ls", "veg"]}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "desayuno": "Mate con tostadas"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "desayuno": "Café con molletes"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "desayuno": "Pan con tomate"}
}

# --- SIDEBAR / FICHA ---
with st.sidebar:
    st.header("👤 Ficha del Paciente")
    nombre = st.text_input("Nombre", value="Emanuel")
    peso = st.number_input("Peso (kg)", value=75.0)
    talla = st.number_input("Talla (cm)", value=175)
    imc = peso / ((talla/100)**2)
    st.metric("IMC", f"{imc:.1f}")
    
    st.divider()
    st.subheader("🏥 Condiciones Clínicas")
    patologias = st.multiselect("Filtros:", ["Celíaco", "Hipertenso", "Vegetariano", "Vegano"])
    
    st.divider()
    pais = st.selectbox("Mercado", list(paises.keys()))
    entorno = st.radio("Logística", ["Oficina", "Hogar"])

# --- LÓGICA Y RESULTADO ---
st.title("🥗 Nutri-Flow: Gestión Profesional")

if st.button("🚀 GENERAR PLAN"):
    term = paises[pais]
    recetas_ok = [r for r in base_recetas if r["entorno"] == entorno]
    
    if "Celíaco" in patologias: recetas_ok = [r for r in recetas_ok if "gf" in r["tags"]]
    if "Vegetariano" in patologias: recetas_ok = [r for r in recetas_ok if "veg" in r["tags"] or "vgn" in r["tags"]]
    if "Vegano" in patologias: recetas_ok = [r for r in recetas_ok if "vgn" in r["tags"]]
    if "Hipertenso" in patologias: recetas_ok = [r for r in recetas_ok if "ls" in r["tags"]]

    if not recetas_ok:
        st.error("No hay platos que coincidan con todos los filtros. Intentá quitar alguna restricción.")
    else:
        plato = random.choice(recetas_ok)
        plato_nom = plato["nombre"].format(**term)
        
        st.markdown(f"""
        <div class="plan-card">
            <h2>📋 Plan Personalizado</h2>
            <p><b>Paciente:</b> {nombre} | <b>IMC:</b> {imc:.1f}</p>
            <p><b>Condiciones:</b> {', '.join(patologias) if patologias else 'General'}</p>
            <hr>
            <p><b>🌅 Desayuno/Merienda:</b> {term['desayuno'] if 'Celíaco' not in patologias else 'Galletas de arroz con palta'}</p>
            <p><b>🍱 Almuerzo Sugerido:</b> {plato_nom}</p>
        </div>
        """, unsafe_allow_html=True)
