import streamlit as st
import random
import json
import os

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- CARGA DINÁMICA DE DATOS ---
# (Aquí asumo que ya tenés tu foods.json con los 500 platos)
if not os.path.exists("foods.json"):
    st.error("Archivo foods.json no encontrado. Asegúrate de haber guardado los 500 platos.")
    st.stop()

with open("foods.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    # Importante: El JSON debe tener estas dos listas
    desayunos_db = data.get("desayunos", [])
    comidas_db = data.get("comidas", [])

# --- DATA DE PAÍSES ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Corte Magro (Nalga/Peceto)", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# --- FUNCIONES DE LÓGICA ---
def filtrar_platos(lista, tags_usuario):
    if not tags_usuario:
        return lista
    # El plato debe cumplir con TODOS los tags seleccionados
    aptos = [p for p in lista if all(t in p.get("tags", []) for t in tags_usuario)]
    # Salvavidas: si el filtro es muy estricto y vacía la lista, devolvemos la lista original
    return aptos if aptos else lista

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    for _ in range(500): # Intentos para cuadrar macros
        dia = []
        nombres_dia = []
        dist = [get_obj * 0.20, get_obj * 0.35, get_obj * 0.15, get_obj * 0.30]
        
        for j in range(4):
            pool = desayunos_pool if j in [0, 2] else comidas_pool
            # Filtro de variedad (evitar repetición inmediata)
            pool_variedad = [p for p in pool if p["nombre"] not in historial_global[-8:]]
            seleccion = pool_variedad if pool_variedad else pool
            
            plato_base = random.choice(seleccion)
            factor = round((dist[j] / plato_base["kcal"]) * 4) / 4
            if factor <= 0: factor = 0.25
            
            dia.append({
                "nom": plato_base["nombre"],
                "kcal": plato_base["kcal"] * factor,
                "p": plato_base["p"] * factor,
                "c": plato_base["c"] * factor,
                "l": plato_base["l"] * factor,
                "factor": factor
            })
            nombres_dia.append(plato_base["nombre"])
        
        tk, tp, tc, tl = sum(x["kcal"] for x in dia), sum(x["p"] for x in dia), sum(x["c"] for x in dia), sum(x["l"] for x in dia)
        
        # Margen de error del 7% para los macros
        def check(r, o): return abs(r - o) / o <= 0.07 if o > 0 else True
        if all([check(tk, get_obj), check(tp, p_obj), check(tc, c_obj), check(tl, l_obj)]):
            historial_global.extend(nombres_dia)
            return dia, (tk, tp, tc, tl)
            
    return None, (0, 0, 0, 0)

# --- SIDEBAR (INTERFAZ) ---
with st.sidebar:
    st.header("👤 Ficha del Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, value=float(talla-100))
    
    af_opts = {1.2: "Sedentario", 1.375: "Leve", 1.55: "Moderado", 1.725: "Fuerte"}
    af_val = st.selectbox("Actividad Física", options=list(af_opts.keys()), format_func=lambda x: af_opts[x])
    
    st.divider()
    st.subheader("⚙️ Macros (%)")
    p_cho = st.slider("% Carbohidratos", 0, 100, 50)
    p_pro = st.slider("% Proteínas", 0, 100, 25)
    p_lip = 100 - p_cho - p_pro
    st.caption(f"Lípidos automáticos: {p_lip}%")

    st.divider()
    st.subheader("📋 Perfil Alimentario")
    opciones = st.multiselect(
        "Preferencias y Restricciones:",
        ["Celíaco (gf)", "Diabético (db)", "Bajo Sodio (ls)", "Vegano (vgn)", "Vegetariano (vgn)", "Dislipemia (dl)", "Almuerzo en Trabajo (tp)"]
    )
    
    mapping = {"Celíaco (gf)": "gf", "Diabético (db)": "db", "Bajo Sodio (ls)": "ls", "Vegano (vgn)": "vgn", "Vegetariano (vgn)": "vgn", "Dislipemia (dl)": "dl", "Almuerzo en Trabajo (tp)": "tp"}
    tags_usuario = [mapping[o] for o in opciones]
    
    pais_sel = st.selectbox("País de Residencia", list(paises.keys()))

# --- CÁLCULOS TÉCNICOS ---
tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * af_val
obj_p, obj_c, obj_l = (get*p_pro/400), (get*p_cho/400), (get*p_lip/900)

# --- FILTRADO DE BASE DE DATOS ---
d_final = filtrar_platos(desayunos_db, tags_usuario)
c_final = filtrar_platos(comidas_db, tags_usuario)

# --- GENERACIÓN Y DASHBOARD ---
c_info, c_plan = st.columns([1, 2.5])

with c_info:
    st.markdown(f"""
    <div style="background-color:#1e1e1e; padding:20px; border-radius:10px; border:1px solid #00d4ff">
        <h3 style="color:#00d4ff; margin-top:0">📊 Informe</h3>
        <b>GET:</b> {get:.0f} kcal<br>
        <b>P:</b> {obj_p:.1f}g | <b>C:</b> {obj_c:.1f}g | <b>G:</b> {obj_l:.1f}g
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 GENERAR MENÚ SEMANAL"):
    historial = []
    conteo = {}
    for i in range(7):
        st.session_state[f"d_{i}"], st.session_state[f"t_{i}"] = generar_dia_estricto(
            get, obj_p, obj_c, obj_l, d_final, c_final, historial, conteo
        )
    st.session_state.listo = True

if st.session_state.get("listo"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for i, d_nombre in enumerate(dias):
        with st.expander(f"📅 {d_nombre}"):
            dia_data = st.session_state.get(f"d_{i}")
            if dia_data:
                labels = ["☕ Desayuno", "☀️ Almuerzo", "🧉 Merienda", "🌙 Cena"]
                for j, lab in enumerate(labels):
                    p = dia_data[j]
                    # Traducción de términos según país
                    nombre_final = p['nom'].format(**paises[pais_sel])
                    st.write(f"**{lab}:** {nombre_final} (Cant: x{p['factor']})")
            else:
                st.warning("No se pudo cuadrar este día con los filtros actuales.")
