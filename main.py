import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro | Consultorio", page_icon="🍎", layout="wide")

# --- CSS MEJORADO PARA VISIBILIDAD ---
st.markdown("""
    <style>
    h1, h2, h3 { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #1e1e1e !important; font-weight: bold; }
    .metric-box { background: #f0f2f6; padding: 20px; border-radius: 12px; color: #1e1e1e !important; border: 2px solid #2e7d32; }
    .day-card { 
        background-color: #ffffff; padding: 20px; border-radius: 10px; 
        border-left: 8px solid #2e7d32; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .day-title { color: #2e7d32 !important; font-size: 1.3em; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #eee; }
    .meal-row { color: #333 !important; font-size: 1em; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
desayunos = [
    {"nombre": "Yogur natural con granola y {frutilla}", "tags": ["gf", "db"]},
    {"nombre": "Tostadas integrales con queso y {palta}", "tags": ["db", "veg"]},
    {"nombre": "Omelette de claras y espinaca", "tags": ["gf", "db", "lc"]},
    {"nombre": "Bowl de avena y nueces", "tags": ["vgn", "db"]}
]

comidas = [
    {"nombre": "Pollo al horno con calabaza", "tags": ["gf", "db", "ls"]},
    {"nombre": "Ensalada de quinoa y {choclo}", "tags": ["gf", "vgn", "ls"]},
    {"nombre": "Pescado con {zapallito} grillado", "tags": ["gf", "db", "ls", "lc"]},
    {"nombre": "Wok de vegetales y arroz integral", "tags": ["vgn", "db", "ls"]},
    {"nombre": "Tarta de {zapallito} integral", "tags": ["veg", "db", "ls"]}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Paciente")
    nombre = st.text_input("Nombre", "Emanuel")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    edad = st.number_input("Edad", 18, 100, 30)
    peso = st.number_input("Peso (kg)", 40.0, 200.0, 75.0)
    talla = st.number_input("Talla (cm)", 120, 220, 175)
    actividad = st.selectbox("Actividad", [1.2, 1.375, 1.55, 1.725])
    
    st.divider()
    st.header("⚖️ Macros %")
    p_carb = st.slider("Carbohidratos", 0, 100, 50)
    p_prot = st.slider("Proteínas", 0, 100, 20)
    p_gras = st.slider("Grasas", 0, 100, 30)
    
    st.divider()
    pats = st.multiselect("Patologías:", ["Celíaco", "Hipertenso", "Diabético", "Vegetariano"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS ---
tmb = (10 * peso) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * actividad
imc = peso / ((talla/100)**2)

# --- INTERFAZ PRINCIPAL ---
st.title("🍎 Nutri-Flow: Panel de Control")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <h3>Informe Metabólico</h3>
        <b>IMC:</b> {imc:.1f}<br>
        <b>GET:</b> {get:.0f} kcal<br><br>
        <b>Macros en gramos:</b><br>
        🍞 CHO: {(get * p_carb / 400):.1f}g<br>
        🍗 PRO: {(get * p_prot / 400):.1f}g<br>
        🥑 LIP: {(get * p_gras / 900):.1f}g
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("🚀 GENERAR PLAN SEMANAL"):
        st.session_state.ver_plan = True
        term = paises[pais]
        
        # Filtrado simple para la demo
        d_ok = [r for r in desayunos if "db" in r["tags"]] if "Diabético" in pats else desayunos
        c_ok = [r for r in comidas if "ls" in r["tags"]] if "Hipertenso" in pats else comidas

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        for dia in dias:
            st.markdown(f"""
            <div class="day-card">
                <div class="day-title">📅 {dia}</div>
                <div class="meal-row">☕ <b>Desayuno:</b> {random.choice(d_ok)["nombre"].format(**term)}</div>
                <div class="meal-row">☀️ <b>Almuerzo:</b> {random.choice(c_ok)["nombre"].format(**term)}</div>
                <div class="meal-row">🍪 <b>Merienda:</b> {random.choice(d_ok)["nombre"].format(**term)}</div>
                <div class="meal-row">🌙 <b>Cena:</b> {random.choice(c_ok)["nombre"].format(**term)}</div>
            </div>
            """, unsafe_allow_html=True)
