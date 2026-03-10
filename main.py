import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Nutri-Flow Pro | Gestión Semanal", page_icon="🍎", layout="wide")

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
    .meal-text { color: #333 !important; font-size: 0.95em; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS MAESTRA ---
# Tags: gf(sin tacc), ls(bajo sodio), db(diabetes), dl(dislipemia), veg(vegetariano), vgn(vegano)
recetas = [
    {"nombre": "Tarta de {zapallito} con masa de semillas", "tags": ["ls", "veg", "db"]},
    {"nombre": "Ensalada de quinoa, {porotos} y {choclo}", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Pollo al horno con calabaza asada", "tags": ["gf", "ls", "dl", "db"]},
    {"nombre": "Wok de vegetales y arroz integral", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Pescado al limón con {zapallito} al vapor", "tags": ["gf", "ls", "dl", "db"]},
    {"nombre": "Omelette de espinaca y ricota magra", "tags": ["gf", "ls", "veg", "db"]},
    {"nombre": "Guiso de lentejas nutri", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Berenjenas rellenas de carne magra", "tags": ["gf", "ls", "dl", "db"]},
    {"nombre": "Hamburguesas de quinoa y espinaca", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Soufflé de calabaza y queso light", "tags": ["gf", "ls", "veg", "db"]},
    {"nombre": "Suprema de pollo con puré de zanahoria", "tags": ["gf", "ls", "dl"]},
    {"nombre": "Zapallitos rellenos de mijo y vegetales", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Filete de merluza con ensalada de {palta}", "tags": ["gf", "ls", "dl", "db"]}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "desayuno": "Mate con tostadas integrales y queso magro"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "desayuno": "Café con molletes integrales y frijol"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "desayuno": "Tostada con oliva y tomate"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha Clínica")
    nombre = st.text_input("Paciente", "Emanuel")
    peso = st.number_input("Peso (kg)", 75.0)
    talla = st.number_input("Talla (cm)", 175)
    imc = peso / ((talla/100)**2)
    st.metric("IMC", f"{imc:.1f}")
    
    st.divider()
    st.subheader("🏥 Patologías")
    pats = st.multiselect("Seleccionar:", ["Celíaco", "Hipertenso", "Diabético", "Dislipemia", "Vegetariano", "Vegano"])
    
    st.divider()
    pais = st.selectbox("País", list(paises.keys()))
    st.info("El plan generará 7 días con 4 comidas.")

# --- LÓGICA DE FILTRADO ---
term = paises[pais]
recetas_ok = recetas.copy()
if "Celíaco" in pats: recetas_ok = [r for r in recetas_ok if "gf" in r["tags"]]
if "Hipertenso" in pats: recetas_ok = [r for r in recetas_ok if "ls" in r["tags"]]
if "Diabético" in pats: recetas_ok = [r for r in recetas_ok if "db" in r["tags"]]
if "Dislipemia" in pats: recetas_ok = [r for r in recetas_ok if "dl" in r["tags"]]
if "Vegetariano" in pats: recetas_ok = [r for r in recetas_ok if "veg" in r["tags"] or "vgn" in r["tags"]]
if "Vegano" in pats: recetas_ok = [r for r in recetas_ok if "vgn" in r["tags"]]

# --- INTERFAZ PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro: Planificador Semanal")

if st.button("🚀 GENERAR / REFRESCAR SEMANA COMPLETA"):
    st.session_state.plan_generado = True
    # Inicializar o resetar los 7 días
    for d in range(7):
        st.session_state[f"almuerzo_{d}"] = random.choice(recetas_ok)["nombre"].format(**term)
        st.session_state[f"cena_{d}"] = random.choice(recetas_ok)["nombre"].format(**term)

if "plan_generado" in st.session_state:
    st.markdown(f"""
    <div class="plan-card">
        <h2>Reporte Nutricional: {nombre}</h2>
        <p><b>Diagnóstico:</b> {', '.join(pats) if pats else 'Sin patologías'} | <b>IMC:</b> {imc:.1f}</p>
        <p><b>☕ Desayuno y Merienda:</b> {term['desayuno'] if 'Celíaco' not in pats else 'Galletas de arroz con hummus o palta'}</p>
    </div>
    """, unsafe_allow_html=True)

    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    
    for i, dia in enumerate(dias):
        with st.container():
            col_txt, col_btn = st.columns([4, 1])
            with col_txt:
                st.markdown(f"""
                <div class="day-container">
                    <div class="day-title">{dia}</div>
                    <div class="meal-text">☀️ <b>Almuerzo:</b> {st.session_state[f'almuerzo_{i}']}</div>
                    <div class="meal-text">🌙 <b>Cena:</b> {st.session_state[f'cena_{i}']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                st.write("") # Espaciado
                if st.button(f"🔄 Cambiar", key=f"btn_{i}"):
                    st.session_state[f"almuerzo_{i}"] = random.choice(recetas_ok)["nombre"].format(**term)
                    st.session_state[f"cena_{i}"] = random.choice(recetas_ok)["nombre"].format(**term)
                    st.rerun()

    # Botón final de descarga
    st.download_button("📥 Descargar Plan Semanal", "Resumen de plan semanal Nutri-Flow Pro", file_name=f"Plan_Semanal_{nombre}.txt")
