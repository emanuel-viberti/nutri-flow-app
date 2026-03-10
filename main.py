import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Nutri-Flow Pro | Plan 4 Comidas", page_icon="🍎", layout="wide")

# --- CSS PROFESIONAL ---
st.markdown("""
    <style>
    h1, h2, h3, [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #1e1e1e !important; font-weight: bold; }
    .plan-card { padding: 25px; border-radius: 12px; background-color: #ffffff; border-left: 10px solid #2e7d32; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .plan-card h2, .plan-card p, .plan-card b { color: #1e1e1e !important; }
    .day-container { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; color: #1e1e1e !important; }
    .day-title { color: #2e7d32 !important; font-size: 1.2em; font-weight: bold; border-bottom: 2px solid #2e7d32; margin-bottom: 10px; }
    .meal-text { color: #333 !important; font-size: 0.95em; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASES DE DATOS ---
# TAGS: gf (sin tacc), ls (bajo sodio), db (diabetes), veg (vegetariano), vgn (vegano)

desayunos_meriendas = [
    {"nombre": "Yogur natural con granola y {frutilla}", "tags": ["gf", "ls", "db"]},
    {"nombre": "Tostadas integrales con queso untable y {palta}", "tags": ["ls", "db", "veg"]},
    {"nombre": "Galletas de arroz con mantequilla de maní y banana", "tags": ["gf", "ls", "vgn"]},
    {"nombre": "Omelette de claras con semillas de chía", "tags": ["gf", "ls", "db", "veg"]},
    {"nombre": "Bowl de avena con leche de almendras y nueces", "tags": ["ls", "vgn", "db"]},
    {"nombre": "Panqueques de avena y clara de huevo con {frutilla}", "tags": ["ls", "db", "veg"]},
    {"nombre": "Mate/Café con pan integral de masa madre y ricota", "tags": ["ls", "db", "veg"]}
]

almuerzos_cenas = [
    {"nombre": "Tarta de {zapallito} integral con mix de verdes", "tags": ["ls", "veg", "db"]},
    {"nombre": "Ensalada de quinoa, {porotos} y {choclo}", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Pollo al horno con calabaza y romero", "tags": ["gf", "ls", "db"]},
    {"nombre": "Wok de vegetales salteados con arroz integral", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Pescado al limón con {zapallito} grillado", "tags": ["gf", "ls", "db"]},
    {"nombre": "Milanesas de soja con puré de zanahoria", "tags": ["ls", "vgn", "db"]},
    {"nombre": "Hamburguesas de mijo y espinaca", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Zapallitos rellenos de carne magra y queso", "tags": ["gf", "ls", "db"]}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "frutilla": "Frutilla"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "frutilla": "Fresa"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "frutilla": "Fresa"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha del Paciente")
    nombre = st.text_input("Paciente", "Emanuel")
    peso = st.number_input("Peso (kg)", 75.0)
    talla = st.number_input("Talla (cm)", 175)
    imc = peso / ((talla/100)**2)
    st.metric("IMC", f"{imc:.1f}")
    
    st.divider()
    st.subheader("🏥 Patologías")
    pats = st.multiselect("Filtros:", ["Celíaco", "Hipertenso", "Diabético", "Vegetariano", "Vegano"])
    pais = st.selectbox("País", list(paises.keys()))

# --- FUNCION DE FILTRADO ---
def filtrar_recetas(lista, filtros):
    resultado = lista.copy()
    if "Celíaco" in filtros: resultado = [r for r in resultado if "gf" in r["tags"]]
    if "Hipertenso" in filtros: resultado = [r for r in resultado if "ls" in r["tags"]]
    if "Diabético" in filtros: resultado = [r for r in resultado if "db" in r["tags"]]
    if "Vegetariano" in filtros: resultado = [r for r in resultado if "veg" in r["tags"] or "vgn" in r["tags"]]
    if "Vegano" in filtros: resultado = [r for r in resultado if "vgn" in r["tags"]]
    return resultado

# --- LÓGICA DE GENERACIÓN ---
st.title("🍎 Nutri-Flow Pro: Planificador Semanal")

if st.button("🚀 GENERAR SEMANA COMPLETA (4 COMIDAS)"):
    st.session_state.plan_generado = True
    term = paises[pais]
    dm_ok = filtrar_recetas(desayunos_meriendas, pats)
    ac_ok = filtrar_recetas(almuerzos_cenas, pats)

    for i in range(7):
        st.session_state[f"d_{i}"] = random.choice(dm_ok)["nombre"].format(**term)
        st.session_state[f"a_{i}"] = random.choice(ac_ok)["nombre"].format(**term)
        st.session_state[f"m_{i}"] = random.choice(dm_ok)["nombre"].format(**term)
        st.session_state[f"c_{i}"] = random.choice(ac_ok)["nombre"].format(**term)

if "plan_generado" in st.session_state:
    st.markdown(f"""<div class="plan-card">
        <h2>Reporte Nutricional: {nombre}</h2>
        <p><b>Diagnóstico:</b> {', '.join(pats) if pats else 'General'} | <b>IMC:</b> {imc:.1f}</p>
    </div>""", unsafe_allow_html=True)

    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    term = paises[pais]
    dm_ok = filtrar_recetas(desayunos_meriendas, pats)
    ac_ok = filtrar_recetas(almuerzos_cenas, pats)

    for i, dia in enumerate(dias):
        with st.container():
            col_txt, col_btn = st.columns([5, 1])
            with col_txt:
                st.markdown(f"""
                <div class="day-container">
                    <div class="day-title">{dia}</div>
                    <div class="meal-text">☕ <b>Desayuno:</b> {st.session_state[f'd_{i}']}</div>
                    <div class="meal-text">☀️ <b>Almuerzo:</b> {st.session_state[f'a_{i}']}</div>
                    <div class="meal-text">🍪 <b>Merienda:</b> {st.session_state[f'm_{i}']}</div>
                    <div class="meal-text">🌙 <b>Cena:</b> {st.session_state[f'c_{i}']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                st.write("") # Espacio
                if st.button(f"🔄", key=f"btn_{i}"):
                    st.session_state[f"d_{i}"] = random.choice(dm_ok)["nombre"].format(**term)
                    st.session_state[f"a_{i}"] = random.choice(ac_ok)["nombre"].format(**term)
                    st.session_state[f"m_{i}"] = random.choice(dm_ok)["nombre"].format(**term)
                    st.session_state[f"c_{i}"] = random.choice(ac_ok)["nombre"].format(**term)
                    st.rerun()
