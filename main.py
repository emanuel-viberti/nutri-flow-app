import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- CSS PROFESIONAL ---
st.markdown("""
    <style>
    h1, h2, h3 { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label { color: #1e1e1e !important; font-weight: bold; }
    .day-card { 
        background-color: #ffffff; padding: 15px; border-radius: 12px; 
        border-left: 8px solid #2e7d32; margin-bottom: 18px; color: #1e1e1e !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .macro-tag { font-size: 0.75em; background: #e8f5e9; color: #2e7d32; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    .metric-box { background: #f0f2f6; padding: 15px; border-radius: 10px; color: #333; border: 1px solid #ccc; }
    .pi-box { background: #fff3e0; border: 1px solid #ff9800; padding: 8px; border-radius: 8px; color: #e65100; margin-top: 5px;}
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db"], "rec": "200g yogur + 3 cdas granola", "p": 8, "c": 30},
    {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "ls"], "rec": "1 tostada + 1/2 palta + 1 huevo", "p": 12, "c": 20},
    {"nombre": "Panqueque de avena y banana", "tags": ["veg"], "rec": "1 huevo + 3 cdas avena + 1/2 banana", "p": 10, "c": 25}
]

comidas = [
    {"nombre": "Pollo al horno con calabaza", "tags": ["gf", "ls"], "rec": "150g pechuga + 200g calabaza", "p": 30, "c": 25},
    {"nombre": "Wok de vegetales y arroz", "tags": ["vgn"], "rec": "Vegetales + 1 taza arroz cocido", "p": 8, "c": 45},
    {"nombre": "Pescado con {zapallito}", "tags": ["gf", "db"], "rec": "Filete blanco + 2 {zapallito}", "p": 28, "c": 10}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "frutilla": "Frutilla"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "frutilla": "Fresa"}
}

# --- FUNCIONES ---
def seleccionar_plato(lista, filtros, term):
    res = [r for r in lista]
    if "Celíaco" in filtros: res = [r for r in res if "gf" in r["tags"]]
    if "Diabético" in filtros: res = [r for r in res if "db" in r["tags"]]
    plato = random.choice(res if res else lista)
    return {"nom": plato["nombre"].format(**term), "rec": plato["rec"].format(**term), "p": plato["p"], "c": plato["c"]}

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 50, 250, 175)
    peso_act = st.number_input("Peso (kg)", 10.0, 200.0, 75.0)
    pi = (talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9
    st.markdown(f'<div class="pi-box"><b>Sugerencia PI:</b> {pi:.1f} kg</div>', unsafe_allow_html=True)
    peso_obj = st.number_input("Peso Objetivo (kg)", 10.0, 200.0, float(pi))
    pats = st.multiselect("Patologías", ["Celíaco", "Diabético", "Hipertenso"])
    pais = st.selectbox("País", list(paises.keys()))

# --- LÓGICA MÉDICA (IMC) ---
imc = peso_act / ((talla/100)**2)
def obtener_diagnostico(v):
    if v < 18.5: return "Bajo Peso", "#ffeb3b"
    if v < 25: return "Normopeso", "#4caf50"
    if v < 30: return "Sobrepeso", "#ff9800"
    return "Obesidad", "#f44336"

txt_imc, col_imc = obtener_diagnostico(imc)

# --- UI PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro")
c_info, c_plan = st.columns([1, 2.2])

with c_info:
    st.markdown(f"""
    <div class="metric-box">
        <h4>📊 Informe</h4>
        <b>IMC Actual:</b> {imc:.1f} <br>
        <span style="background-color:{col_imc}; color:black; padding:2px 6px; border-radius:4px; font-weight:bold;">{txt_imc}</span>
        <hr>
        <b>Peso Ref:</b> {peso_obj} kg
    </div>
    """, unsafe_allow_html=True)

with c_plan:
    if st.button("🚀 GENERAR PLAN SEMANAL"):
        term = paises[pais]
        for i in range(7):
            st.session_state[f"d{i}_m0"] = seleccionar_plato(desayunos, pats, term)
            st.session_state[f"d{i}_m1
