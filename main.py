import streamlit as st
import json
import random
import os

st.set_page_config(page_title="Nutri-Flow Pro", layout="wide")

def cargar_datos():
    archivo = 'foods.json'
    if not os.path.exists(archivo):
        st.error("Archivo foods.json no encontrado.")
        st.stop()
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

data = cargar_datos()

def generar_dia(get_obj, p_obj, c_obj, l_obj, desayunos, comidas, historial):
    best_day = None
    min_error = float('inf')
    for i in range(3000):
        platos_base = [random.choice(desayunos), random.choice(comidas), random.choice(desayunos), random.choice(comidas)]
        kcal_base = sum(p['kcal'] for p in platos_base)
        if kcal_base == 0: continue
        f_teorico = get_obj / kcal_base
        max_f = 3.5 if i > 1500 else 2.5
        f = max(0.4, min(f_teorico, max_f))
        dia_actual = []
        nombres = []
        for p in platos_base:
            nom = p["nombre"].replace("{", "").replace("}", "")
            dia_actual.append({"nom": nom, "kcal": p["kcal"]*f, "p": p["p"]*f, "c": p["c"]*f, "l": p["l"]*f, "factor": round(f*4)/4})
            nombres.append(nom)
        tk, tp, tc, tl = [sum(x[k] for x in dia_actual) for k in ['kcal', 'p', 'c', 'l']]
        error = (abs(tk-get_obj)/get_obj) + (abs(tp-p_obj)/p_obj) + (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
        if any(n in historial[-12:] for n in nombres): error += 0.4
        if error < min_error:
            min_error = error
            best_day = (dia_actual, (tk, tp, tc, tl), nombres)
        if error < (0.08 if i < 2000 else 0.12): break
    if best_day:
        historial.extend(best_day[2])
        return best_day[0], best_day[1]
    return None, (0,0,0,0)

st.sidebar.header("Configuración")
kcal_target = st.sidebar.number_input("Kcal Objetivo", value=1584)
c_p = st.sidebar.slider("Carbohidratos %", 10, 70, 55)
p_p = st.sidebar.slider("Proteínas %", 10, 50, 25)
l_p = st.sidebar.slider("Lípidos %", 10, 50, 20)

t_p, t_c, t_l = (kcal_target*p_p/100/4), (kcal_target*c_p/100/4), (kcal_target*l_p/100/9)

if 'semana' not in st.session_state: st.session_state.semana = {}
if 'historial' not in st.session_state: st.session_state.historial = []

if st.sidebar.button("GENERAR PLAN"):
    st.session_state.semana = {}
    st.session_state.historial = []
    for d in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]:
        res, m = generar_dia(kcal_target, t_p, t_c, t_l, data["desayunos"], data["comidas"], st.session_state.historial)
        if res: st.session_state.semana[d] = (res, m)
    st.rerun()

st.title("Nutri-Flow Pro")
if st.session_state.semana:
    for dia, (platos, macros) in st.session_state.semana.items():
        c1, c2 = st.columns([0.8, 0.2])
        c1.subheader(f"{dia}")
        if c2.button(f"🔄", key=f"btn_{dia}"):
            n_res, n_m = generar_dia(kcal_target, t_p, t_c, t_l, data["desayunos"], data["comidas"], st.session_state.historial)
            if n_res:
                st.session_state.semana[dia] = (n_res, n_m)
                st.rerun()
        tabla = []
        for i, mom in enumerate(["Desayuno", "Almuerzo", "Merienda", "Cena"]):
            p = platos[i]
            tabla.append({"Momento": mom, "Plato": p["nom"], "Cant": f"x{p['factor']}", "Kcal": int(p['kcal'])})
        st.table(tabla)
else:
    st.info("Dale a GENERAR PLAN.")
