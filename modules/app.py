# app.py
import streamlit as st
from modules.config import paises
from modules.data_loader import cargar_datos, filtrar_platos
from modules.calculator import calcular_metricas
from modules.generator import generar_dia_estricto

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# Carga de datos
desayunos_db, comidas_db = cargar_datos()

# Sidebar
with st.sidebar:
    st.header("👤 Ficha del Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, value=float(talla-100))
    af_val = st.selectbox("Actividad Física", options=[1.2, 1.375, 1.55, 1.725], format_func=lambda x: {1.2:"Sedentario", 1.375:"Leve", 1.55:"Moderado", 1.725:"Fuerte"}[x])
    
    st.divider()
    st.subheader("⚙️ Macros (%)")
    p_cho = st.number_input("% Carbohidratos", 0, 100, 50)
    p_pro = st.number_input("% Proteínas", 0, 100, 25)
    p_lip = st.number_input("% Lípidos", 0, 100, 25)
    
    st.divider()
    pais_sel = st.selectbox("País", list(paises.keys()))

# Lógica
get, imc, obj_p, obj_c, obj_l = calcular_metricas(sexo, talla, peso_act, edad, pi_real, af_val, p_pro, p_cho, p_lip)
d_final = filtrar_platos(desayunos_db, [])
c_final = filtrar_platos(comidas_db, [])

# Interfaz Principal
st.title("🍎 Nutri-Flow Pro")
c1, c2 = st.columns([1, 2.5])

with c1:
    st.info(f"**GET:** {get:.0f} kcal | **IMC:** {imc:.1f}")
    st.write(f"**Objetivos:** P:{obj_p:.0f}g C:{obj_c:.0f}g G:{obj_l:.0f}g")
    
    if (p_cho + p_pro + p_lip) != 100:
        st.error("⚠️ Macros deben sumar 100%")
    else:
        if st.button("🚀 GENERAR PLAN SEMANAL", use_container_width=True):
            historial = []
            for i in range(7):
                res, tot = generar_dia_estricto(get, obj_p, obj_c, obj_l, d_final, c_final, historial, {})
                st.session_state[f"plan_{i}"] = res
            st.session_state.listo = True

with c2:
    if st.session_state.get("listo"):
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for i, nombre in enumerate(dias):
            with st.expander(f"📅 {nombre}", expanded=(i==0)):
                plan_dia = st.session_state.get(f"plan_{i}")
                if plan_dia:
                    for idx, lab in enumerate(["☕ Des", "☀️ Alm", "🧉 Mer", "🌙 Cen"]):
                        p = plan_dia[idx]
                        nombre_p = p['nom'].format(**paises[pais_sel])
                        st.write(f"**{lab}:** {nombre_p} (x{p['factor']})")
