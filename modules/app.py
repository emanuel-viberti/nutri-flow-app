# app.py
import streamlit as st
from modules.config import paises
from modules.data_loader import cargar_datos, filtrar_platos
from modules.calculator import calcular_metricas
from modules.generator import generar_dia_estricto

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# 1. Carga de datos
desayunos_db, comidas_db = cargar_datos()

# 2. Sidebar de entrada
with st.sidebar:
    st.header("👤 Datos del Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, value=float(talla-105))
    af_val = st.selectbox("Actividad Física", options=[1.2, 1.375, 1.55, 1.725], 
                          format_func=lambda x: {1.2:"Sedentario", 1.375:"Leve", 1.55:"Moderado", 1.725:"Fuerte"}[x])
    
    st.divider()
    st.subheader("⚙️ Configuración de Macros")
    p_cho = st.number_input("% Carbohidratos", 0, 100, 55)
    p_pro = st.number_input("% Proteínas", 0, 100, 25)
    p_lip = st.number_input("% Lípidos", 0, 100, 20)
    
    pais_sel = st.selectbox("País del Paciente", list(paises.keys()))

# 3. Cálculos y Filtrado
get, imc, obj_p, obj_c, obj_l = calcular_metricas(sexo, talla, peso_act, edad, pi_real, af_val, p_pro, p_cho, p_lip)

# Mantenemos el pool completo para asegurar que el generador siempre tenga platos
d_final = desayunos_db
c_final = comidas_db

# 4. Interfaz Principal
st.title("🍎 Nutri-Flow Pro")
col_info, col_plan = st.columns([1, 2.5])

with col_info:
    st.success(f"**GET Estimado:** {get:.0f} kcal")
    st.info(f"**Objetivos Diarios:**\n\n**P:** {obj_p:.1f}g | **C:** {obj_c:.1f}g | **G:** {obj_l:.1f}g")
    
    if (p_cho + p_pro + p_lip) != 100:
        st.error("⚠️ La suma de macros debe ser 100%")
    else:
        if st.button("🚀 GENERAR MENÚ SEMANAL", use_container_width=True):
            historial = []
            for i in range(7):
                resultado, totales = generar_dia_estricto(get, obj_p, obj_c, obj_l, d_final, c_final, historial, {})
                st.session_state[f"dia_{i}"] = resultado
            st.session_state.listo = True

with col_plan:
    if st.session_state.get("listo"):
        nombres_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for i, nombre in enumerate(nombres_dias):
            with st.expander(f"📅 {nombre}", expanded=(i==0)):
                dia_data = st.session_state.get(f"dia_{i}")
                if dia_data:
                    labels = ["☕ Desayuno", "☀️ Almuerzo", "🧉 Merienda", "🌙 Cena"]
                    for idx, lab in enumerate(labels):
                        plato = dia_data[idx]
                        nombre_final = plato['nom'].format(**paises[pais_sel])
                        st.write(f"**{lab}:** {nombre_final} (Cant: x{plato['factor']})")
                else:
                    st.error("Error al generar este día.")
