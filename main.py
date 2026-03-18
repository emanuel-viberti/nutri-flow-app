import streamlit as st
import json
import random
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Nutri-Flow Pro", layout="wide")

# 2. CARGA DE DATOS (foods.json)
def cargar_datos():
    archivo = 'foods.json'
    if not os.path.exists(archivo):
        st.error(f"No se encuentra el archivo {archivo}")
        st.stop()
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

data = cargar_datos()

# 3. INICIALIZAR MEMORIA (Session State)
# Esto evita que los datos se borren al tocar botones
if 'paciente' not in st.session_state:
    st.session_state.paciente = {"nombre": "", "peso": 70.0, "objetivo": ""}
if 'dieta' not in st.session_state:
    st.session_state.dieta = {}
if 'hist' not in st.session_state:
    st.session_state.hist = []

# 4. SIDEBAR - DATOS DEL PACIENTE Y MACROS
st.sidebar.header("👤 Datos del Paciente")
# Guardamos directamente en el session_state
st.session_state.paciente["nombre"] = st.sidebar.text_input("Nombre", st.session_state.paciente["nombre"])
st.session_state.paciente["peso"] = st.sidebar.number_input("Peso (kg)", value=st.session_state.paciente["peso"])

st.sidebar.header("📊 Configuración Plan")
kcal_target = st.sidebar.number_input("Kcal Objetivo", value=1584)
c_p = st.sidebar.slider("Carbohidratos %", 10, 70, 55)
p_p = st.sidebar.slider("Proteínas %", 10, 50, 25)
l_p = st.sidebar.slider("Lípidos %", 10, 50, 20)

# Gramos objetivo
t_p, t_c, t_l = (kcal_target*p_p/100/4), (kcal_target*c_p/100/4), (kcal_target*l_p/100/9)

# MOTOR DE CÁLCULO (Simplificado para que no falle)
def generar_dia(kcal_obj, p_obj, c_obj, l_obj, desayunos, comidas, historial):
    for i in range(2000):
        try:
            p_base = [random.choice(desayunos), random.choice(comidas), random.choice(desayunos), random.choice(comidas)]
            kb = sum(p['kcal'] for p in p_base)
            f = max(0.4, min(kcal_obj / kb, 3.5))
            dia = []
            noms = []
            for p in p_base:
                n = p["nombre"].replace("{", "").replace("}", "")
                dia.append({"nom": n, "kcal": p["kcal"]*f, "p": p["p"]*f, "c": p["c"]*f, "l": p["l"]*f, "factor": round(f*4)/4})
                noms.append(n)
            tk, tp, tc, tl = [sum(x[k] for x in dia) for k in ['kcal', 'p', 'c', 'l']]
            err = (abs(tk-kcal_obj)/kcal_obj) + (abs(tp-p_obj)/p_obj) + (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
            if err < 0.12:
                historial.extend(noms)
                return dia, (tk, tp, tc, tl)
        except: continue
    return None, (0,0,0,0)

# BOTÓN GENERAR
if st.sidebar.button("🚀 GENERAR PLAN SEMANAL"):
    nueva_dieta = {}
    st.session_state.hist = []
    for d in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]:
        res, m = generar_dia(kcal_target, t_p, t_c, t_l, data["desayunos"], data["comidas"], st.session_state.hist)
        if res: nueva_dieta[d] = (res, m)
    st.session_state.dieta = nueva_dieta
    st.rerun()

# 5. INTERFAZ PRINCIPAL
st.title("🍎 Nutri-Flow Pro")

# Mostramos datos del paciente siempre que estén cargados
if st.session_state.paciente["nombre"]:
    st.info(f"📋 **Paciente:** {st.session_state.paciente['nombre']} | **Peso:** {st.session_state.paciente['peso']} kg")

if st.session_state.dieta:
    for dia, (platos, macros) in st.session_state.dieta.items():
        with st.container():
            c1, c2 = st.columns([0.85, 0.15])
            c1.subheader(f"📅 {dia}")
            
            if c2.button("🔄", key=f"btn_{dia}"):
                n_res, n_m = generar_dia(kcal_target, t_p, t_c, t_l, data["desayunos"], data["comidas"], st.session_state.hist)
                if n_res:
                    st.session_state.dieta[dia] = (n_res, n_m)
                    st.rerun()

            filas = []
            moms = ["Desayuno", "Almuerzo", "Merienda", "Cena"]
            for i, p in enumerate(platos):
                filas.append({"Momento": moms[i], "Plato": p["nom"], "Porción": f"x{p['factor']}", "Kcal": int(p['kcal'])})
            st.table(filas)
            st.caption(f"Totales: {int(macros[0])} kcal | P: {int(macros[1])}g | C: {int(macros[2])}g | L: {int(macros[3])}g")
            st.divider()
else:
    st.warning("Escribí el nombre del paciente y dale a 'GENERAR PLAN SEMANAL'.")
