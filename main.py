import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍏", layout="wide")

# --- CSS (Mantenemos tu diseño pro) ---
st.markdown("""
    <style>
    h1, h2, h3, [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #1e1e1e !important; }
    .plan-card { padding: 30px; border-radius: 15px; background-color: #ffffff; border-left: 10px solid #2e7d32; margin-bottom: 20px; color: #1e1e1e !important; }
    .plan-card h2, .plan-card p, .plan-card b, .plan-card li { color: #1e1e1e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE CLASIFICACIÓN (DICCIONARIOS) ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "desayuno": "Mate con tostadas"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "desayuno": "Café con molletes"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "desayuno": "Pan con tomate"}
}

# --- INTERFAZ ---
st.title("🥗 Nutri-Flow: Consultorio Digital")

with st.sidebar:
    st.header("👤 Ficha del Paciente")
    nombre = st.text_input("Nombre", value="Emanuel")
    edad = st.number_input("Edad", min_value=1, max_value=120, value=30)
    peso = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=75.0)
    talla = st.number_input("Talla (cm)", min_value=50, max_value=250, value=175)
    
    # Cálculo de IMC
    imc = peso / ((talla/100)**2)
    st.metric("IMC", f"{imc:.1f}")
    if imc < 18.5: st.caption("Bajo peso")
    elif imc < 25: st.caption("Peso Normal")
    elif imc < 30: st.caption("Sobrepeso")
    else: st.caption("Obesidad")

    st.divider()
    st.header("🏥 Condiciones Clínicas")
    patologias = st.multiselect("Seleccionar Patologías/Alergias", 
                                ["Celíaco", "Hipertenso", "Diabético", "Dislipemia", "Vegetariano", "Vegano"])
    
    st.divider()
    pais = st.selectbox("Mercado/País", list(paises.keys()))
    entorno = st.radio("Logística Almuerzo", ["Oficina", "Hogar"])

# --- ÁREA DE RESULTADOS ---
col_izq, col_der = st.columns([2, 1])

with col_izq:
    if st.button("🚀 GENERAR PLAN NUTRICIONAL COMPLETO"):
        term = paises[pais]
        
        # Aquí irá el filtrado de las 50 recetas (que haremos a continuación)
        st.markdown(f"""
        <div class="plan-card">
            <h2>📋 Plan para {nombre}</h2>
            <p><b>Resumen Clínico:</b> Edad {edad} | IMC {imc:.1f} | {', '.join(patologias) if patologias else 'Sin patologías'}</p>
            <hr>
            <p><b>🌅 Desayuno/Merienda:</b> {term['desayuno']}</p>
            <p><b>🍱 Almuerzo Sugerido:</b> Receta adaptada a {entorno} y {', '.join(patologias)}</p>
            <ul>
                <li>Control de porciones basado en IMC de {imc:.1f}</li>
                <li>Sugerencia de hidratación específica.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with col_der:
    st.markdown("### 📊 Objetivos")
    if imc > 25:
        st.info("Objetivo: Déficit Calórico Controlado")
        st.metric("Calorías Meta", "1800 kcal")
    else:
        st.info("Objetivo: Mantenimiento / Salud")
        st.metric("Calorías Meta", "2200 kcal")
