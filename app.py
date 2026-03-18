import streamlit as st
import json
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Nutri-Flow Pro", layout="wide")

# 2. MOTOR DE CÁLCULO INTEGRADO
def generar_dia(get_obj, p_obj, c_obj, l_obj, desayunos, comidas, historial):
    best_day = None
    min_error = float('inf')
    
    # Intentamos 3000 veces para encontrar el match perfecto
    for i in range(3000):
        try:
            platos_base = [
                random.choice(desayunos), random.choice(comidas),
                random.choice(desayunos), random.choice(comidas)
            ]
            
            kcal_base = sum(p['kcal'] for p in platos_base)
            if kcal_base == 0: continue
            
            factor_teorico = get_obj / kcal_base
            # Si hay muchos intentos, permitimos porciones más grandes (hasta x3.5)
            max_f = 3.5 if i > 1500 else 2.5
            f = max(0.4, min(factor_teorico, max_f))
            
            dia_actual = []
            nombres = []
            for p in platos_base:
                nom_limpio = p["nombre"].replace("{", "").replace("}", "")
                dia_actual.append({
                    "nom": nom_limpio, "kcal": p["kcal"] * f,
                    "p": p["p"] * f, "c": p["c"] * f, "l": p["l"] * f,
                    "factor": round(f * 4) / 4
                })
                nombres.append(nom_limpio)

            tk, tp, tc, tl = [sum(x[k] for x in dia_actual) for k in ['kcal', 'p', 'c', 'l']]
            error = (abs(tk-get_obj)/get_obj) + (abs(tp-p_obj)/p_obj) + (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
            
            if any(n in historial[-12:] for n in nombres): error += 0.4

            if error < min_error:
                min_error = error
                best_day = (dia_actual, (tk, tp, tc, tl), nombres)
            
            if error < (0.08 if i < 2000 else 0.15): break
        except: continue

    if best_day:
        historial.extend(best_day[2])
        return best_day[0], best_day[1]
    return None, (0,0,0,0)

# 3. CARGA DE DATOS (Asegurate que el archivo se llame foods.json)
try:
    with open('foods.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    st.error("Archivo 'foods.json' no encontrado.")
    st.stop()

# 4. SIDEBAR - PARÁMETROS
st.sidebar.header("📊 Configuración")
kcal_target = st.sidebar.number_input("Kcal Objetivo", value=1584)
c_p = st.sidebar.slider("Carbohidratos %", 10, 70, 55)
p_p = st.sidebar.slider("Proteínas %", 10, 50, 25)
l_p = st.sidebar.slider("Lípidos %", 10, 50, 20)

target_p, target_c, target_l = (kcal_target*p_p/100/4), (kcal_target*c_p/100/4), (kcal_target*l_p/100/9)

# 5. SESSION STATE
if 'semana' not in st.session_state: st.session_state.semana = {}
if 'historial' not in st.session_state: st.session_state.historial = []

if st.sidebar.button("🚀 GENERAR MENÚ SEMANAL"):
    st.session_state.semana = {}
    st.session_state.historial = []
    for d in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]:
        res, m = generar_dia(kcal_target, target_p, target_c, target_l, data["desayunos"], data["comidas"], st.session_state.historial)
        if res: st.session_state.semana[d] = (res, m)
    st.rerun()

# 6. RENDERIZADO
st.title("🍎 Nutri-Flow Pro")

if st.session_state.semana:
    for dia, (platos, macros) in st.session_state.semana.items():
        with st.expander(f"📅 {dia}", expanded=True):
            c1, c2 = st.columns([0.8, 0.2])
            c1.write(f"**Total:** {int(macros[0])} kcal | P: {int(macros[1])}g | C: {int(macros[2])}g | L: {int(macros[3])}g")
            
            # BOTÓN DE INTERCAMBIO
            if c2.button(f"🔄 Intercambiar", key=f"btn_{dia}"):
                nuevo_res, nuevo_m = generar_dia(kcal_target, target_p, target_c, target_l, data["desayunos"], data["comidas"], st.session_state.historial)
                if nuevo_res:
                    st.session_state.semana[dia] = (nuevo_res, nuevo_m)
                    st.rerun()

            for p in platos:
                st.write(f"- **{p['nom']}** (Cant: x{p['factor']})")
else:
    st.info("Hacé clic en 'GENERAR MENÚ SEMANAL' para empezar.")
