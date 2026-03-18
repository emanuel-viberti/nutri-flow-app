import streamlit as st
import json
import random
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Nutri-Flow Pro", layout="wide")

# 2. CARGA DE DATOS
def cargar_datos():
    archivo = 'foods.json'
    if not os.path.exists(archivo):
        st.error(f"No se encuentra el archivo {archivo}")
        st.stop()
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

data = cargar_datos()

# 3. MOTOR DE CÁLCULO
def generar_dia(kcal_obj, p_obj, c_obj, l_obj, desayunos, comidas, historial):
    best_day = None
    min_error = float('inf')
    for i in range(2500):
        try:
            p_base = [random.choice(desayunos), random.choice(comidas), 
                      random.choice(desayunos), random.choice(comidas)]
            kb = sum(p['kcal'] for p in p_base)
            if kb == 0: continue
            f = max(0.4, min(kcal_obj / kb, 3.5))
            dia_actual = []
            nombres = []
            for p in p_base:
                nom = p["nombre"].replace("{", "").replace("}", "")
                dia_actual.append({"nom": nom, "kcal": p["kcal"]*f, "p": p["p"]*f, "c": p["c"]*f, "l": p["l"]*f, "factor": round(f*4)/4})
                nombres.append(nom)
            tk, tp, tc, tl = [sum(x[k] for x in dia_actual) for k in ['kcal', 'p', 'c', 'l']]
            err = (abs(tk-kcal_obj)/kcal_obj) + (abs(tp-p_obj)/p_obj) + (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
            if any(n in historial[-12:] for n in nombres): err += 0.5
            if err < min_error:
                min_error = err
                best_day = (dia_actual, (tk, tp, tc, tl), nombres)
            if err < 0.10: break
        except: continue
    if best_day:
        historial.extend(best_day[2])
        return best_day[0], best_day[1]
    return None, (0,0,0,0)

# 4. SIDEBAR - PARÁMETROS
st.sidebar.header("📊 Configuración")
kcal_target = st.sidebar.number_input("Kcal Objetivo", value=1584)
c_p = st.sidebar.slider("Carbohidratos %", 10, 70, 55)
p_p = st.sidebar.slider("Proteínas %", 10, 50, 25)
l_p = st.sidebar.slider("Lípidos %", 10, 50, 20)

t_p, t_c, t_l = (kcal_target*p_p/100/4), (kcal_target*c_p/100/4), (kcal_target*l_p/100/9)

# 5. MANEJO DE ESTADO (SESSION STATE)
if 'dieta' not in st.session_state:
    st.session_state.dieta = {}
if 'hist' not in st.session_state:
    st.session_state.hist = []

# EL BOTÓN: Solo genera, no dibuja
if st.sidebar.button("🚀 GENERAR PLAN"):
    nueva_dieta = {}
    st.session_state.hist = []
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for d in dias:
        res, m = generar_dia(kcal_target, t_p, t_c, t_l, data["desayunos"], data["comidas"], st.session_state.hist)
        if res: nueva_dieta[d] = (res, m)
    st.session_state.dieta = nueva_dieta
    st.rerun()

# 6. DIBUJO DE LA INTERFAZ
st.title("🍎 Nutri-Flow Pro")

if st.session_state.dieta:
    for dia, (platos, macros) in st.session_state.dieta.items():
        with st.container():
            c1, c2 = st.columns([0.85, 0.15])
            c1.subheader(f"📅 {dia}")
            
            # BOTÓN INTERCAMBIO
            if c2.button("🔄", key=f"btn_{dia}"):
                n_res, n_m = generar_dia(kcal_target, t_p, t_c, t_l, data["desayunos"], data["comidas"], st.session_state.hist)
                if n_res:
                    st.session_state.dieta[dia] = (n_res, n_m)
                    st.rerun()

            # TABLA
            filas = []
            moms = ["Desayuno", "Almuerzo", "Merienda", "Cena"]
            for i, p in enumerate(platos):
                filas.append({"Momento": moms[i], "Plato": p["nom"], "Porción": f"x{p['factor']}", "Kcal": int(p['kcal'])})
            st.table(filas)
            st.caption(f"Totales: {int(macros[0])} kcal | P: {int(macros[1])}g | C: {int(macros[2])}g | L: {int(macros[3])}g")
            st.divider()
else:
    st.info("Ajustá los valores y dale a 'GENERAR PLAN'.")
