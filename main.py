import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍏", layout="wide")

# --- CSS PROFESIONAL ---
st.markdown("""
    <style>
    h1, h2, h3, [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #1e1e1e !important; }
    .plan-card { padding: 30px; border-radius: 15px; background-color: #ffffff; border-left: 10px solid #2e7d32; margin-bottom: 20px; color: #1e1e1e !important; }
    .plan-card h2, .plan-card p, .plan-card b, .plan-card li { color: #1e1e1e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS DE RECETAS CON TAGS ---
# Tags: gf (Gluten Free), ls (Low Sodium), veg (Vegetariano), vgn (Vegano), lc (Low Carb)
base_recetas = [
    {"nombre": "Tarta de {zapallito} integral", "entorno": "Oficina", "tags": ["ls"]},
    {"nombre": "Ensalada de {porotos} y {choclo}", "entorno": "Oficina", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Wrap de pollo y {palta}", "entorno": "Oficina", "tags": ["ls"]},
    {"nombre": "Wok de vegetales y arroz integral", "entorno": "Oficina", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Milanesas con puré de calabaza", "entorno": "Hogar", "tags": ["ls"]},
    {"nombre": "Guiso de lentejas nutri", "entorno": "Hogar", "tags": ["gf", "ls", "veg", "vgn"]},
    {"nombre": "Pescado al papillote con vegetales", "entorno": "Hogar", "tags": ["gf", "ls", "lc"]},
    {"nombre": "Omelette de espinaca y queso", "entorno": "Hogar", "tags": ["gf", "ls", "veg", "lc"]},
    {"nombre": "Zapallitos rellenos de carne magra", "entorno": "Hogar", "tags": ["gf", "ls", "lc"]},
    {"nombre": "Hamburguesas de lentejas caseras", "entorno": "Oficina", "tags": ["ls", "veg", "vgn"]}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "desayuno": "Mate con tostadas"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "elote": "Elote", "frijoles": "Frijoles", "desayuno": "Café con molletes"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "maiz": "Maíz", "alubias": "Alubias", "desayuno": "Pan con tomate y oliva"}
}

# --- INTERFAZ / SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha Clínica")
    nombre = st.text_input("Nombre", value="Emanuel")
    peso = st.number_input("Peso (kg)", value=75.0)
    talla = st.number_input("Talla (cm)", value=175)
    
    imc = peso / ((talla/100)**2)
    st.metric("IMC", f"{imc:.1f}")
    
    st.divider()
    st.header("🏥 Condiciones")
    es_celiaco = st.checkbox("Celíaco (Sin TACC)")
    es_vege = st.checkbox("Vegetariano")
    es_vegano = st.checkbox("Vegano")
    es_hiper = st.checkbox("Hipertenso")

    st.divider()
    pais = st.selectbox("País", list(paises.keys()))
    entorno = st.radio("Logística", ["Oficina", "Hogar"])

# --- LÓGICA DE FILTRADO ---
st.title("🥗 Nutri-Flow: Gestión Profesional")

if st.button("🚀 GENERAR PLAN NUTRICIONAL"):
    term = paises[pais]
    
    # Filtrado Inteligente
    recetas_ok = [r for r in base_recetas if r["entorno"] == entorno]
    
    if es_celiaco:
        recetas_ok = [r for r in recetas_ok if "gf" in r["tags"]]
    if es_vege:
        recetas_ok = [r for r in recetas_ok if "veg" in r["tags"] or "vgn" in r["tags"]]
    if es_vegano:
        recetas_ok = [r for r in recetas_ok if "vgn" in r["tags"]]
    if es_hiper:
        recetas_ok = [r for r in recetas_ok if "ls" in r["tags"]]

    if not recetas_ok:
        st.error("⚠️ No hay recetas que cumplan todos los filtros clínicos seleccionados.")
    else:
        plato_data = random.choice(recetas_ok)
        plato_final = plato_data["nombre"].format(**term)
        
        # UI de Resultado
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="plan-card">
                <h2>📋 Plan para {nombre}</h2>
                <p><b>Estado Nutricional:</b> IMC {imc:.1f} ({'Normal' if 18.5 < imc < 25 else 'Ajustar'})</p>
                <hr>
                <p><b>🌅 Desayuno/Merienda:</b> {term['desayuno'] if not es_celiaco else 'Galletas de arroz con hummus'}</p>
                <p><b>🍱 Almuerzo ({entorno}):</b> {plato_final}</p>
                <p><i>Filtros aplicados: {', '.join([p for p, v in zip(['Celíaco', 'Vegetariano', 'Vegano', 'Hipertenso'], [es_celiaco, es_vege, es_vegano, es_hiper]) if v]) if any([es_celiaco, es_vege, es_vegano, es_hiper]) else 'Ninguno'}</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Exportación
            txt_export = f"PLAN NUTRI-FLOW\nPaciente: {nombre}\nIMC: {imc:.1f}\nAlmuerzo: {plato_final}"
            st.download_button("📥 Descargar Plan", txt_export, file_name=f"Plan_{nombre}.txt")
        
        with col2:
            st.markdown("### 📊 Objetivos")
            st.metric("Calorías Meta", "1950 kcal" if imc < 25 else "1750 kcal")
            st.progress(0.7)
            st.caption("Adherencia estimada: Alta")
