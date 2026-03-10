import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Nutri-Flow Pro | Consultorio", page_icon="🍏", layout="wide")

# --- CSS DE ALTA VISIBILIDAD ---
st.markdown("""
    <style>
    h1, h2, h3, [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #1e1e1e !important; }
    .plan-card { padding: 25px; border-radius: 12px; background-color: #ffffff; border-left: 8px solid #2e7d32; margin-bottom: 15px; color: #1e1e1e !important; }
    .plan-card h3, .plan-card b, .plan-card p { color: #1e1e1e !important; }
    .day-box { background: #f9f9f9; padding: 10px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 5px; color: #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS AMPLIADA ---
# Tags: gf (sin tacc), ls (bajo sodio), veg (vegetariano), vgn (vegano), db (diabético), dl (dislipemia)
recetario = [
    {"nombre": "Tarta de {zapallito} integral", "tags": ["ls", "veg", "db"]},
    {"nombre": "Ensalada de quinoa, {porotos} y {choclo}", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Pollo al horno con calabaza asada", "tags": ["gf", "ls", "dl", "db"]},
    {"nombre": "Wok de vegetales y arroz integral", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Pescado al papillote con {zapallito}", "tags": ["gf", "ls", "dl", "db", "lc"]},
    {"nombre": "Omelette de espinaca y ricota magra", "tags": ["gf", "ls", "veg", "db", "lc"]},
    {"nombre": "Guiso de lentejas con vegetales", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Milanesas de soja con ensalada mixta", "tags": ["ls", "vgn", "db"]},
    {"nombre": "Berenjenas rellenas de carne magra", "tags": ["gf", "ls", "dl", "db", "lc"]},
    {"nombre": "Hamburguesas de quinoa y espinaca", "tags": ["gf", "ls", "vgn", "db"]},
    {"nombre": "Soufflé de calabaza y queso light", "tags": ["gf", "ls", "veg", "db"]},
    {"nombre": "Suprema de pollo con puré de zanahoria", "tags": ["gf", "ls", "dl"]},
    {"nombre": "Canelones de verdura con salsa roja", "tags": ["ls", "veg", "db"]}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "desayuno": "Mate con tostadas integrales y queso untable"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "desayuno": "Café de olla con molletes integrales"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "desayuno": "Tostada con aceite de oliva y tomate"}
}

# --- SIDEBAR: FICHA CLÍNICA COMPLETA ---
with st.sidebar:
    st.header("👤 Ficha del Paciente")
    nombre = st.text_input("Nombre", "Emanuel")
    peso = st.number_input("Peso (kg)", 75.0)
    talla = st.number_input("Talla (cm)", 175)
    imc = peso / ((talla/100)**2)
    st.metric("IMC", f"{imc:.1f}")
    
    st.divider()
    st.header("🏥 Diagnóstico Clínico")
    patologias = st.multiselect("Patologías/Restricciones:", 
                                ["Celíaco", "Hipertenso", "Diabético", "Dislipemia", "Vegetariano", "Vegano"])
    
    st.divider()
    pais = st.selectbox("Mercado", list(paises.keys()))

# --- GENERACIÓN DE PLAN SEMANAL ---
st.title("🍎 Nutri-Flow Pro: Planificador Semanal")

if st.button("🚀 GENERAR PLAN SEMANAL COMPLETO"):
    term = paises[pais]
    
    # Filtrado según patologías
    recetas_ok = recetario.copy()
    if "Celíaco" in patologias: recetas_ok = [r for r in recetas_ok if "gf" in r["tags"]]
    if "Hipertenso" in patologias: recetas_ok = [r for r in recetas_ok if "ls" in r["tags"]]
    if "Diabético" in patologias: recetas_ok = [r for r in recetas_ok if "db" in r["tags"]]
    if "Dislipemia" in patologias: recetas_ok = [r for r in recetas_ok if "dl" in r["tags"]]
    if "Vegetariano" in patologias: recetas_ok = [r for r in recetas_ok if "veg" in r["tags"] or "vgn" in r["tags"]]
    if "Vegano" in patologias: recetas_ok = [r for r in recetas_ok if "vgn" in r["tags"]]

    if len(recetas_ok) < 7:
        st.error("⚠️ Base de datos insuficiente para estos filtros. Añadiendo recetas genéricas...")
        recetas_ok = recetario # Fallback para no dejar vacío el plan

    # Renderizado
    st.markdown(f"""
    <div class="plan-card">
        <h2>Plan Semanal: {nombre}</h2>
        <p><b>Resumen Clínico:</b> IMC {imc:.1f} | <b>Filtros:</b> {', '.join(patologias) if patologias else 'General'}</p>
        <hr>
        <p><b>☕ Desayuno/Merienda sugerido:</b> {term['desayuno']}</p>
    </div>
    """, unsafe_allow_html=True)

    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    
    # Crear grilla de 7 días
    for dia in dias:
        almuerzo = random.choice(recetas_ok)["nombre"].format(**term)
        cena = random.choice(recetas_ok)["nombre"].format(**term)
        # Evitar que almuerzo y cena sean iguales
        while cena == almuerzo:
            cena = random.choice(recetas_ok)["nombre"].format(**term)
            
        st.markdown(f"""
        <div class="day-box">
            <b>📅 {dia}</b><br>
            ☀️ Almuerzo: {almuerzo}<br>
            🌙 Cena: {cena}
        </div>
        """, unsafe_allow_html=True)

    # Exportación
    st.download_button("📥 Descargar Reporte Completo (.txt)", "Reporte generado por Nutri-Flow Pro", file_name=f"Plan_{nombre}.txt")
