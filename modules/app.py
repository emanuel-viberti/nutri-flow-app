import streamlit as st
import json
from modules.generator import generar_dia_estricto

# 1. Configuración y Carga
st.set_page_config(page_title="Nutri-Flow Pro", layout="wide")

def cargar_datos():
    with open('data/alimentos.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = cargar_datos()

# 2. Sidebar - Configuración
st.sidebar.header("⚙️ Parámetros")
get_diaria = st.sidebar.number_input("Kcal Objetivo", value=1584)

# Macros
c_pct = st.sidebar.slider("Carbohidratos %", 10, 70, 55)
p_pct = st.sidebar.slider("Proteínas %", 10, 50, 25)
l_pct = st.sidebar.slider("Lípidos %", 10, 50, 20)

# Cálculo de gramos
p_g = (get_diaria * (p_pct/100)) / 4
c_g = (get_diaria * (c_pct/100)) / 4
l_g = (get_diaria * (l_pct/100)) / 9

# 3. Inicializar Session State
if 'dieta_semanal' not in st.session_state:
    st.session_state.dieta_semanal = {}
if 'historial_semanal' not in st.session_state:
    st.session_state.historial_semanal = []

# 4. Botón Principal
if st.sidebar.button("🚀 Generar Plan Completo"):
    st.session_state.dieta_semanal = {}
    st.session_state.historial_semanal = []
    
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for d in dias:
        res_platos, res_macros = generar_dia_estricto(
            get_diaria, p_g, c_g, l_g, 
            data["desayunos"], data["comidas"], 
            st.session_state.historial_semanal, {}
        )
        if res_platos:
            st.session_state.dieta_semanal[d] = (res_platos, res_macros)
    st.rerun()

# 5. Renderizado de la Dieta
st.title("🍎 Planificador Nutri-Flow")

if st.session_state.dieta_semanal:
    for dia, (platos, macros) in st.session_state.dieta_semanal.items():
        st.write("---")
        # Usamos columnas para poner el título y el botón en la misma línea
        c1, c2 = st.columns([0.8, 0.2])
        
        with c1:
            st.subheader(f"📅 {dia}")
        
        with c2:
            # BOTÓN DE INTERCAMBIO
            if st.button(f"🔄 Cambiar", key=f"btn_{dia}"):
                nuevo_p, nuevo_m = generar_dia_estricto(
                    get_diaria, p_g, c_g, l_g, 
                    data["desayunos"], data["comidas"], 
                    st.session_state.historial_semanal, {}
                )
                if nuevo_p:
                    st.session_state.dieta_semanal[dia] = (nuevo_p, nuevo_m)
                    st.rerun()

        # Tabla de alimentos
        filas = []
        momentos = ["Desayuno", "Almuerzo", "Merienda", "Cena"]
        for i, p in enumerate(platos):
            filas.append({
                "Momento": momentos[i],
                "Plato": p["nom"],
                "Porción": f"x{p['factor']}",
                "Kcal": int(p['kcal'])
            })
        st.table(filas)
        st.caption(f"Totales: {int(macros[0])} kcal | P: {int(macros[1])}g | C: {int(macros[2])}g | L: {int(macros[3])}g")
else:
    st.info("Presioná 'Generar Plan Completo' en el menú lateral.")
