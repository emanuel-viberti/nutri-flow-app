import streamlit as st
from modules.config import paises
from modules.data_loader import cargar_datos, filtrar_platos
from modules.calculator import calcular_metricas
from modules.generator import generar_dia_estricto

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# 2. CARGA DE DATOS
desayunos_db, comidas_db = cargar_datos()

# 3. SIDEBAR
with st.sidebar:
    st.header("👤 Ficha del Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    
    pi_sugerido = float(talla - 100) if sexo == "Masculino" else float((talla - 100) * 0.9)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, value=pi_sugerido)
    
    af_opts = {1.2: "Sedentario", 1.375: "Leve", 1.55: "Moderado", 1.725: "Fuerte"}
    af_val = st.selectbox("Actividad Física", options=list(af_opts.keys()), format_func=lambda x: af_opts[x])
    
    st.divider()
    st.subheader("⚙️ Macros (%)")
    p_cho = st.number_input("% Carbohidratos", 0, 100, 50)
    p_pro = st.number_input("% Proteínas", 0, 100, 25)
    p_lip = st.number_input("% Lípidos", 0, 100, 25)
    
    total_macros = p_cho + p_pro + p_lip

    st.divider()
    st.subheader("📋 Perfil")
    opciones = st.multiselect("Filtros:", ["Celíaco (gf)", "Diabético (db)", "Bajo Sodio (ls)", "Vegano (vgn)", "Vegetariano (vgn)", "Dislipemia (dl)", "Almuerzo en Trabajo (tp)"])
    mapping = {"Celíaco (gf)": "gf", "Diabético (db)": "db", "Bajo Sodio (ls)": "ls", "Vegano (vgn)": "vgn", "Vegetariano (vgn)": "vgn", "Dislipemia (dl)": "dl", "Almuerzo en Trabajo (tp)": "tp"}
    tags_usuario = [mapping[o] for o in opciones]
    
    pais_sel = st.selectbox("País", list(paises.keys()))

# 4. CÁLCULOS
get, imc, obj_p, obj_c, obj_l = calcular_metricas(sexo, talla, peso_act, edad, pi_real, af_val, p_pro, p_cho, p_lip)
d_final = filtrar_platos(desayunos_db, tags_usuario)
c_final = filtrar_platos(comidas_db, tags_usuario)

# 5. INTERFAZ
st.title("🍎 Nutri-Flow Pro")
c_info, c_plan = st.columns([1, 2.5])

with c_info:
    st.markdown(f"""
    <div style="background-color:#1e1e1e; padding:20px; border-radius:10px; border:1px solid #00d4ff; color:white">
        <h3 style="color:#00d4ff; margin-top:0">📊 Informe</h3>
        <b>IMC:</b> {imc:.1f}<br>
        <b>GET:</b> {get:.0f} kcal<br><hr>
        <b>P:</b> {obj_p:.1f}g | <b>C:</b> {obj_c:.1f}g | <b>G:</b> {obj_l:.1f}g
    </div>
    """, unsafe_allow_html=True)
    
    if total_macros != 100:
        st.error(f"Suma: {total_macros}% (debe ser 100)")
    else:
        if st.button("🚀 GENERAR PLAN SEMANAL", use_container_width=True):
    historial = [] # Reiniciamos el historial de platos repetidos
    # Forzamos la limpieza de la memoria de Streamlit
    for i in range(7):
        st.session_state[f"d_{i}"] = None 
    
    # ... resto del código de generación ...
            
            # GENERACIÓN
            for i in range(7):
                resultado, totales = generar_dia_estricto(get, obj_p, obj_c, obj_l, d_final, c_final, historial, {})
                if resultado:
                    st.session_state[f"d_{i}"] = resultado
                else:
                    st.session_state[f"d_{i}"] = "ERROR" # Marca de fallo
            
            st.session_state.listo = True

# 6. RENDERIZADO (CORREGIDO PARA MOSTRAR LOS 7)
if st.session_state.get("listo"):
    with c_plan:
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for i, nombre_dia in enumerate(dias):
            with st.expander(f"📅 {nombre_dia}", expanded=True):
                datos = st.session_state.get(f"d_{i}")
                
                if datos == "ERROR" or datos is None:
                    st.warning("No se pudo generar este día. Reintentá.")
                else:
                    labels = ["☕ Desayuno", "☀️ Almuerzo", "🧉 Merienda", "🌙 Cena"]
                    for idx, lab in enumerate(labels):
                        p = datos[idx]
                        n_final = p['nom'].format(**paises[pais_sel])
                        st.write(f"**{lab}:** {n_final} (x{p['factor']:.2f})")
