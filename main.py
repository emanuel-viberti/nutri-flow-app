import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro | Consultorio", page_icon="🍎", layout="wide")

# --- CSS PROFESIONAL ---
st.markdown("""
    <style>
    h1, h2, h3 { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #1e1e1e !important; font-weight: bold; }
    .day-card { 
        background-color: #ffffff; padding: 20px; border-radius: 12px; 
        border-left: 10px solid #2e7d32; margin-bottom: 20px; color: #1e1e1e !important;
    }
    .meal-box { margin-bottom: 10px; padding: 5px; border-bottom: 1px solid #eee; }
    .receta-text { font-size: 0.85em; color: #555; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS EXTENDIDA ---
desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db", "ls"], "receta": "Mezclar 200g de yogur descremado con 3 cdas de granola."},
    {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "veg", "ls"], "receta": "1 tostada integral con media palta pisada y 1 huevo revuelto."},
    {"nombre": "Panqueque de avena y banana", "tags": ["db", "veg", "ls"], "receta": "Mezclar 1 huevo, 3 cdas de avena y media banana. A la sartén."},
    {"nombre": "Bowl de frutas de estación y nueces", "tags": ["gf", "vgn", "db", "ls"], "receta": "Corta frutas variadas y agrega 3 mariposas de nuez."}
]

comidas = [
    {"nombre": "Pollo al horno con calabaza", "tags": ["gf", "db", "ls", "dl"], "receta": "150g de pechuga con 200g de calabaza asada con romero.", "pro": 30, "cho": 25},
    {"nombre": "Wok de vegetales y arroz integral", "tags": ["vgn", "db", "ls"], "receta": "Saltear brócoli, zanahoria y zuchini con 1 taza de arroz cocido.", "pro": 8, "cho": 45},
    {"nombre": "Pescado con {zapallito} grillado", "tags": ["gf", "db", "ls", "dl"], "receta": "Filete a la plancha con 2 {zapallito} en rodajas.", "pro": 28, "cho": 10},
    {"nombre": "Ensalada de quinoa y {choclo}", "tags": ["gf", "vgn", "ls", "db"], "receta": "1 taza de quinoa, medio {choclo} desgranado, tomate y albahaca.", "pro": 10, "cho": 50},
    {"nombre": "Tarta de {zapallito} integral", "tags": ["veg", "db", "ls"], "receta": "Masa integral, relleno de {zapallito}, cebolla y ligue de claras.", "pro": 12, "cho": 35}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "d": "Mate con tostadas"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "d": "Café con molletes"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "d": "Tostada con tomate y aceite de oliva"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    nombre = st.text_input("Nombre", "Emanuel")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    peso = st.number_input("Peso (kg)", 75.0)
    talla = st.number_input("Talla (cm)", 175)
    actividad = st.select_slider("Actividad Física", options=[1.2, 1.375, 1.55, 1.725])
    
    st.divider()
    pats = st.multiselect("Patologías:", ["Celíaco", "Hipertenso", "Diabético", "Vegetariano", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- LÓGICA DE CÁLCULO ---
tmb = (10 * peso) + (6.25 * talla) - (5 * 30) + (5 if sexo == "Masculino" else -161)
get = tmb * actividad
imc = peso / ((talla/100)**2)

# --- FUNCION DE FILTRADO ---
def obtener_menu(lista, filtros, term):
    res = lista.copy()
    if "Celíaco" in filtros: res = [r for r in res if "gf" in r["tags"]]
    if "Hipertenso" in filtros: res = [r for r in res if "ls" in r["tags"]]
    if "Diabético" in filtros: res = [r for r in res if "db" in r["tags"]]
    if "Vegano" in filtros: res = [r for r in res if "vgn" in r["tags"]]
    
    plato = random.choice(res if res else lista)
    nombre_f = plato["nombre"].format(**term)
    return nombre_f, plato.get("receta", ""), plato.get("pro", 0), plato.get("cho", 0)

# --- CUERPO PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro")

if st.button("🚀 GENERAR PLAN SEMANAL COMPLETO"):
    st.session_state.generado = True
    term = paises[pais]
    for i in range(7):
        st.session_state[f"dia_{i}"] = [obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term), 
                                        obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term)]

if "generado" in st.session_state:
    dias_n = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    term = paises[pais]
    
    for i, d_nombre in enumerate(dias_n):
        with st.container():
            col_t, col_b = st.columns([5, 1])
            with col_t:
                st.markdown(f'<div class="day-card"><div class="day-title">📅 {d_nombre}</div>', unsafe_allow_html=True)
                comidas_labels = ["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]
                for idx, label in enumerate(comidas_labels):
                    m_nom, m_rec, m_p, m_c = st.session_state[f"dia_{i}"][idx]
                    st.markdown(f"**{label}:** {m_nom}<br><span class='receta-text'>Prep: {m_rec}</span>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_b:
                if st.button("🔄", key=f"btn_{i}"):
                    st.session_state[f"dia_{i}"] = [obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term), 
                                                    obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term)]
                    st.rerun()
