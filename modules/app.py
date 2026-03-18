import streamlit as st
import json
import os
from modules.generator import generar_dia_estricto

# Configuración de página
st.set_page_config(page_title="Nutri-Flow Pro", layout="wide")

# 1. CARGA DE DATOS
def cargar_datos():
    with open('data/alimentos.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = cargar_datos()

# 2. INTERFAZ DE USUARIO (Sidebar)
st.sidebar.header("⚙️ Configuración del Plan")
get_diaria = st.sidebar.number_input("Kcal Objetivo Diaria", value=1584)

st.sidebar.subheader("Macros (%)")
c_pct = st.sidebar.slider("Carbohidratos", 10, 70, 55)
p_pct = st.sidebar.slider("Proteínas", 10, 50, 25)
l_pct = st.sidebar.slider("Lípidos", 10, 50, 20)

# Validación de suma de macros
if (c_pct + p_pct + l_pct) != 100:
    st.sidebar.error("⚠️ La suma debe ser 100%")

# Objetivos en gramos
p_g = (get_diaria * (p_pct/100)) / 4
c_g = (get_diaria * (c_pct/100)) / 4
l_g = (get_diaria * (l_pct/100)) / 9

# Filtros de Dieta
st.sidebar.subheader("Filtros")
tags_activos = st.sidebar.multiselect("Restricciones", ["gf", "vgn", "db", "ls"], format_func=lambda x: {
    "gf": "Sin TACC", "vgn": "Vegano", "db": "Diabético", "ls": "Bajo en Sodio"
}.get(x))

# 3. LÓGICA DE FILTRADO
def filtrar_pool(pool, filtros):
    if not filtros: return pool
    return [p for p in pool if all(tag in p.get("tags", []) for tag in filtros)]

desayunos_f = filtrar_pool(data["desayunos"], tags_activos)
comidas_f = filtrar_pool(data["comidas"], tags_activos)

# 4. ESTADO DE LA SESIÓN (Session State)
if 'dieta_semanal' not in st.session_state:
    st.session_state.dieta_semanal = {}
if 'historial_semanal' not in st.session_state:
    st.session_state.historial_semanal = []

# 5. BOTÓN GENERAR SEMANA COMPLETA
if st.sidebar.button("🚀 Generar Plan Semanal"):
    st.session_state.dieta_semanal = {}
    st.session_state.historial_semanal = []
    
    for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]:
        dia_res, macros_res = generar_dia_estricto(
            get_diaria, p_g, c_g, l_g, 
            desayunos_f, comidas_f, 
            st.session_state.historial_semanal, {}
        )
        if dia_res:
            st.session_state.dieta_semanal[dia] = (dia_res, macros_res)
    st.rerun()

# 6. VISUALIZACIÓN Y BOTONES DE INTERCAMBIO (REEMPLAZO TOTAL SECCIÓN 6)
st.title("🍎 Tu Plan Nutricional Personalizado")

# Verificamos si hay una dieta generada
if st.session_state.dieta_semanal:
    dias_ordenados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    
    for dia in dias_ordenados:
        if dia in st.session_state.dieta_semanal:
            platos, macros = st.session_state.dieta_semanal[dia]
            
            # Contenedor para cada día para que sea visualmente separado
            with st.container():
                col_info, col_btn = st.columns([0.8, 0.2])
                
                with col_info:
                    st.markdown(f"### 📅 {dia}")
                    st.write(f"**Objetivo:** {int(macros[0])} kcal | **Logrado:** {int(sum(p['kcal'] for p in platos))} kcal")
                
                with col_btn:
                    # El botón de intercambio con un estilo más llamativo
                    if st.button(f"🔄 Cambiar {dia}", key=f"btn_intercambio_{dia}"):
                        nuevo_dia, nuevos_macros = generar_dia_estricto(
                            get_diaria, p_g, c_g, l_g, 
                            desayunos_f, comidas_f, 
                            st.session_state.historial_semanal, {}
                        )
                        if nuevo_dia:
                            st.session_state.dieta_semanal[dia] = (nuevo_dia, nuevos_macros)
                            st.rerun()

                # Armado de la tabla de comidas
                tabla_data = []
                momentos = ["Desayuno", "Almuerzo", "Merienda", "Cena"]
                for i, p in enumerate(platos):
                    tabla_data.append({
                        "Momento": momentos[i],
                        "Plato": p["nom"],
                        "Porción": f"x{p['factor']}",
                        "Kcal": f"{int(p['kcal'])}",
                        "Prot (g)": f"{int(p['p'])}",
                        "Carb (g)": f"{int(p['c'])}",
                        "Grasa (g)": f"{int(p['l'])}"
                    })
                
                st.table(tabla_data)
                
                # Resumen de macros al pie de la tabla
                st.info(f"📊 **Resumen {dia}:** P: {int(macros[1])}g | C: {int(macros[2])}g | L: {int(macros[3])}g")
                st.divider()
else:
    st.warning("⚠️ Todavía no hay un plan generado. Ajustá los valores en la barra lateral y dale a 'Generar Plan Semanal'.")
