import streamlit as st
import json
import random
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Nutri-Flow Pro", layout="wide")

# 2. CARGA DE DATOS
def cargar_datos():
    archivo = 'foods.json'
    if not os.path.exists(archivo):
        st.error(f"No se encuentra el archivo {archivo} en la raíz del proyecto.")
        st.stop()
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error al leer el archivo JSON: {e}")
        st.stop()

data = cargar_datos()

# 3. MOTOR DE GENERACIÓN
def generar_dia(kcal_obj, p_obj, c_obj, l_obj, desayunos, comidas, historial):
    best_day = None
    min_error = float('inf')
    
    for i in range(3000):
        try:
            # Selección aleatoria
            p_base = [random.choice(desayunos), random.choice(comidas), 
                      random.choice(desayunos), random.choice(comidas)]
            
            kb = sum(p['kcal'] for p in p_base)
            if kb == 0: continue
            
            # Ajuste de porción (factor)
            f_teorico = kcal_obj / kb
            max_f = 3.5 if i > 1500 else 2.5
            f = max(0.4, min(f_teorico, max_f))
            
            dia_actual = []
            nombres_dia = []
            for p in p_base:
                nom = p["nombre"].replace("{", "").replace("}", "")
                dia_actual.append({
                    "nom": nom, "kcal": p["kcal"]*f, "p": p["p"]*f, 
                    "c": p["c"]*f, "l": p["l"]*f, "factor": round(f*4)/4
                })
                nombres_dia.append(nom)

            # Cálculo de error
            tk, tp, tc, tl = [sum(x[k] for x in dia_actual) for k in ['kcal', 'p', 'c', 'l']]
            err = (abs(tk-kcal_obj)/kcal_obj) + (abs(tp-p_obj)/p_obj) + \
                  (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
            
            # Penalizar si se repite mucho respecto al historial
            if any(n in historial[-12:] for n in nombres_dia):
                err += 0.5

            if err < min_error:
                min_error = err
                best_day = (dia_actual, (tk, tp, tc, tl), nombres_dia)
            
            if err < (0.08 if i < 2000 else 0.15): break
        except:
            continue

    if best_day:
        historial.extend(best_day[2])
        return best_day[0], best_day[1]
    return None, (0,0,0,0)

# 4. SIDEBAR
st.sidebar.header("Configuración")
kcal_target = st.sidebar.number_input("Kcal Objetivo", value=1584)
c_p = st.sidebar.slider("Carbohidratos %", 10, 70, 55)
p_p = st.sidebar.slider("Proteínas %", 10, 50, 25)
l_p = st.sidebar.slider("Lípidos %", 10, 50, 20)

t_p, t_c, t_l = (kcal_target*p_p/100/4), (kcal_target*c_p/100/4), (kcal_target*l_p/100/9)

# 5. ESTADO DE SESIÓN
if 'semana' not in st.session_state:
    st.session_state.semana = {}
if 'historial' not in st.session_state:
    st.session_state.historial = []

# Botón principal
if st.sidebar.button("GENERAR PLAN"):
    st.session_state.semana = {}
    st.session_state.historial = []
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for d in dias:
        res, m = generar_dia(kcal_target, t_p, t_c, t_l, data["desayunos"], data["comidas"], st.session_state.historial)
        if res:
            st.session_state.semana[d] = (res, m)
    st.rerun()

# 6. INTERFAZ PRINCIPAL
st.title("Nutri-Flow Pro")

if st.session_state.semana:
    for dia, (platos, macros) in st.session_state.semana.items():
        with st.container():
            col_t, col_b = st.columns([0.8, 0.2])
            col_t.subheader(f"📅 {dia}")
            
            # Botón de intercambio individual
            if col_b.button(f"🔄 Cambiar", key=f"btn_{dia}"):
                n_res, n_m = generar_dia(kcal_target, t_p, t_c, t_l, data["desayunos"], data["comidas"], st.session_state.historial)
                if n_res:
                    st.session_state.semana[dia] = (n_res, n_m)
                    st.rerun()

            # Tabla de alimentos
            filas = []
            moms = ["Desayuno", "Almuerzo", "Merienda", "Cena"]
            for i, p in enumerate(platos):
                filas.append({
                    "Momento": moms[i],
                    "Plato": p["nom"],
                    "Porción": f"x{p['factor']}",
                    "Kcal": int(p['kcal'])
                })
            st.table(filas)
            st.caption(f"Totales: {int(macros[0])} kcal | P: {int(macros[1])}g | C: {int(macros[2])}g | L: {int(macros[3])}g")
            st.divider()
else:
    st.info("Ajustá los valores en el panel izquierdo y hacé clic en 'GENERAR PLAN'.")
