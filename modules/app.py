# app.py
import streamlit as st
from modules.config import paises
from modules.data_loader import cargar_datos, filtrar_platos
from modules.calculator import calcular_metricas
from modules.generator import generar_dia_estricto

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# 1. Carga de datos
desayunos_db, comidas_db = cargar_datos()

# 2. Sidebar
with st.sidebar:
    st.header("👤 Datos del Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, value=float(talla-105))
    
    af_opts = {1.2:"Sedentario", 1.375:"Leve", 1.55:"Moderado", 1.725:"Fuerte"}
    af_val = st.selectbox("Actividad Física", options=list(af_opts.keys()), format_func=lambda x: af_opts[x])
    
    st.divider()
    st.subheader("⚙️ Distribución de Macros")
    p_cho = st.number_input("% Carbohidratos", 0, 100, 55)
    p_pro = st.number_input("% Proteínas", 0, 100, 25)
    p_lip = st.number_input("% Lípidos", 0, 100, 20)
    
    pais_sel = st.selectbox("País de Residencia", list(paises.keys()))

# 3. Procesamiento
get, imc, obj_p, obj_c, obj_l = calcular_metricas(sexo, talla, peso_act, edad, pi_real, af_val, p_pro, p_cho, p_lip)

# IMPORTANTE: Desactivamos filtros de tags temporalmente para asegurar que siempre haya platos
d_final = desayunos_db
c_final = comidas_db

# 4. Interfaz Principal (Como la de tu captura)
st.title("🍎 Nutri-Flow Pro")
col_inf, col_plan = st.columns([1, 2.5])

with col_inf:
    # Card de Informe con CSS para que se vea como en tu imagen
    st.markdown(f"""
    <div style="background-color:#0e1117; padding:20px; border-radius:10px; border:1px solid #00d4ff; color:white">
        <h3 style="color:#00d4ff; margin-top:0">📊 Informe</h3>
        <b>GET:</b> {get:.0f} kcal<br>
        <b>P:</b> {obj_p:.1f}g | <b>C:</b> {obj_c:.1f}g | <b>G:</b> {obj_l:.1f}g
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if (p_cho + p_pro + p_lip) != 100:
        st.error("La suma de macros debe ser 100%")
    else:
        if st.button("🚀 GENERAR MENÚ SEMANAL", use_container_width=True):
            hist = []
            for i in range(7):
                res, tot = generar_dia_estricto(get, obj_p, obj_c, obj_l, d_final, c_final, hist, {})
                st.session_state[f"dia_{i}"] = res
            st.session_state.listo = True

with col_plan:
    if st.session_state.get("listo"):
        nombres_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for i, nombre in enumerate(nombres_dias):
            with st.expander(f"📅 {nombre}", expanded=(i==0)):
                data = st.session_state.get(f"dia_{i}")
                if data:
                    labels = ["☕ Desayuno", "☀️ Almuerzo", "🧉 Merienda", "🌙 Cena"]
                    for idx, lab in enumerate(labels):
                        p = data[idx]
                        nom_f = p['nom'].format(**paises[pais_sel])
                        st.write(f"**{lab}:** {nom_f} (Cant: x{p['factor']})")
                else:
                    st.error("No se pudo generar este día.")
