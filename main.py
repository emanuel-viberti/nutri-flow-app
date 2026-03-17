import streamlit as st
import random
import json
import os

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- CARGA DINÁMICA DE DATOS CON AUTO-CREACIÓN ---
# Datos iniciales para que la app no falle la primera vez
base_de_datos_semilla = {
    "desayunos": [
        {"nombre": "Yogur con granola y {frutilla}", "kcal": 250, "p": 15, "c": 35, "l": 6, "tags": ["gf", "db", "ls"]},
        {"nombre": "Tostadas con {palta} y huevo", "kcal": 320, "p": 18, "c": 25, "l": 18, "tags": ["db", "ls"]},
        {"nombre": "Omelette de queso y espinaca", "kcal": 280, "p": 22, "c": 5, "l": 20, "tags": ["gf", "db", "ls"]}
    ],
    "comidas": [
        {"nombre": "Peceto con ensalada de {choclo}", "kcal": 450, "p": 40, "c": 30, "l": 15, "tags": ["gf", "db", "ls", "dl"]},
        {"nombre": "Wok de tofu y arroz integral", "kcal": 550, "p": 25, "c": 75, "l": 18, "tags": ["vgn", "db", "ls"]},
        {"nombre": "Pollo al horno con calabaza", "kcal": 420, "p": 38, "c": 35, "l": 12, "tags": ["gf", "db", "ls", "dl"]},
        {"nombre": "Pastas integrales con brócoli", "kcal": 580, "p": 18, "c": 95, "l": 14, "tags": ["vgn", "db", "ls"]}
    ]
}

if not os.path.exists("foods.json"):
    with open("foods.json", "w", encoding="utf-8") as f:
        json.dump(base_de_datos_semilla, f, indent=4, ensure_ascii=False)

with open("foods.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    desayunos = data["desayunos"]
    comidas = data["comidas"]

# --- DATA DE PAÍSES ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# Límites de variedad semanal
LIMITES_SEMANALES = {
    "Pollo al horno con calabaza": 3,
    "Yogur con granola y {frutilla}": 4,
    "Wok de tofu y arroz integral": 2,
    "Tostadas con {palta} y huevo": 4,
    "Peceto con ensalada de {choclo}": 3
}

# --- MOTOR DE PRECISIÓN Y VARIEDAD ---
def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, tags_req, historial_global, conteo_uso):
    # 1. Intentar filtrar por patologías (si hay alguna seleccionada)
    d_aptos_base = [p for p in desayunos if all(t in p["tags"] for t in tags_req)]
    c_aptos_base = [p for p in comidas if all(t in p["tags"] for t in tags_req)]
    
    # SALVAVIDAS 1: Si no hay platos con esos tags, ignorar patologías y usar todo
    if not d_aptos_base:
        d_aptos_base = desayunos
    if not c_aptos_base:
        c_aptos_base = comidas

    # SALVAVIDAS 2: Si las listas siguen vacías (error en el JSON), evitar el crash
    if not d_aptos_base or not c_aptos_base:
        st.error("⚠️ Error crítico: Las listas de alimentos están vacías. Revisa el formato de tu foods.json.")
        return None, (0, 0, 0, 0)

    for _ in range(1000):
        dia = []
        nombres_dia = []
        dist = [get_obj * 0.20, get_obj * 0.35, get_obj * 0.15, get_obj * 0.30]
        
        for j in range(4):
            pool = d_aptos_base if j in [0,2] else c_aptos_base
            
            # Filtro variedad: Límite semanal y 48hs
            pool_filtrado = [p for p in pool if conteo_uso.get(p["nombre"], 0) < LIMITES_SEMANALES.get(p["nombre"], 7)]
            pool_filtrado = [p for p in pool_filtrado if p["nombre"] not in historial_global[-8:]]
            
            # SALVAVIDAS 3: Si los filtros de variedad vacían la lista, usar el pool sin filtrar
            seleccion_final = pool_filtrado if pool_filtrado else pool
            
            plato_base = random.choice(seleccion_final)
            factor = round((dist[j] / plato_base["kcal"]) * 4) / 4
            if factor == 0: factor = 0.25
            
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
        def error(r, o): return abs(r - o) / o if o > 0 else 0
        
        if all(error(r, o) <= 0.05 for r, o in zip([tk, tp, tc, tl], [get_obj, p_obj, c_obj, l_obj])):
            for n in nombres_dia:
                conteo_uso[n] = conteo_uso.get(n, 0) + 1
                historial_global.append(n)
            return dia, (tk, tp, tc, tl)
            
    return dia, (tk, tp, tc, tl)
# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, value=float((talla-100) if sexo=="Masculino" else (talla-100)*0.9))
    af_opts = {1.2: "Sedentario", 1.375: "Leve", 1.55: "Moderado", 1.725: "Fuerte", 1.9: "Muy Fuerte"}
    af_val = st.selectbox("Actividad Física", options=list(af_opts.keys()), format_func=lambda x: af_opts[x])
    
    st.divider()
    st.header("⚖️ Macros")
    p_cho, p_pro, p_lip = st.number_input("% CHO", 0, 100, 50), st.number_input("% PRO", 0, 100, 20), st.number_input("% LIP", 0, 100, 30)
    # Reemplazo de la sección de patologías por Perfil del Paciente
st.sidebar.subheader("Perfil del Paciente")

opciones_perfil = st.sidebar.multiselect(
    "Preferencias y Restricciones:",
    options=[
        "Celíaco (gf)", 
        "Diabético (db)", 
        "Hipertenso/Bajo Sodio (ls)", 
        "Vegano (vgn)", 
        "Vegetariano (vgn)", 
        "Dislipemia (dl)",
        "Almuerzo en el Trabajo (tp)" 
    ],
    help="Seleccione las condiciones médicas o el estilo de vida del paciente."
)

# Diccionario para traducir el texto del multiselect a los tags del JSON
mapping = {
   def filtrar_platos(base_datos, tags_usuario):
    """
    Filtra la lista de platos. 
    Si el usuario no elige nada, devuelve todo.
    Si elige algo, el plato debe contener TODOS los tags seleccionados.
    """
    if not tags_usuario:
        return base_datos
    
    # Solo entran los platos que tienen cada uno de los tags pedidos
    platos_filtrados = [
        plato for plato in base_datos 
        if all(tag in plato['tags'] for tag in tags_usuario)
    ]
    return platos_filtrados

# Aplicamos el filtro a tu base de datos (reemplazá 'base_datos_500' por el nombre de tu variable)
platos_aptos = filtrar_platos(base_datos_500, pats_tags)

# Mensaje de control por si se pasan de filtros y no queda nada
if not platos_aptos:
    st.warning("⚠️ No se encontraron platos que cumplan con todas las condiciones. Probá quitando algún filtro.")
}

# Creamos la lista de tags corta (ej: ['gf', 'tp'])
pats_tags = [mapping[opt] for opt in opciones_perfil]
    pais = st.selectbox("País", list(paises.keys()))

# --- CALCULOS ---
tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * af_val
obj_p, obj_c, obj_l = (get*p_pro/400), (get*p_cho/400), (get*p_lip/900)
imc = peso_act / ((talla/100)**2)

# --- UI DASHBOARD ---
c_info, c_plan = st.columns([1, 2.5])
with c_info:
    st.markdown(f"""
    <div style="background-color:#1e1e1e; padding:15px; border-radius:10px; color:white; border:1px solid #00d4ff">
        <h4 style="color:#00d4ff; margin:0">📊 Informe Técnico</h4>
        <b>IMC:</b> {imc:.1f}<hr style="border:0.1px solid #464b5d">
        🔥 <b>GET:</b> {get:.0f} kcal<br>
        🍗 <b>P:</b> {obj_p:.1f}g | 🍞 <b>C:</b> {obj_c:.1f}g | 🥑 <b>G:</b> {obj_l:.1f}g
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 GENERAR PLAN SEMANAL (VARIEDAD+)"):
    mapa_tags = {"Celíaco": "gf", "Hipertenso": "ls", "Diabético": "db", "Vegano": "vgn", "Dislipemia": "dl"}
    tags_req = [mapa_tags[p] for p in pats]
    
    historial_global = []
    conteo_uso = {}

    for i in range(7):
        st.session_state[f"dia_{i}"], st.session_state[f"tot_{i}"] = generar_dia_estricto(
            get, obj_p, obj_c, obj_l, tags_req, historial_global, conteo_uso
        )
    st.session_state.listo = True

# --- RENDER ---
if st.session_state.get("listo"):
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for i, nombre_dia in enumerate(dias_semana):
        with st.expander(f"📅 {nombre_dia}", expanded=True):
            dia_data, (tk, tp, tc, tl) = st.session_state[f"dia_{i}"], st.session_state[f"tot_{i}"]
            labels = ["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]
            
            for j, lab in enumerate(labels):
                p = dia_data[j]
                st.write(f"**{lab}:** {p['nom'].format(**paises[pais])} (Cant: x{p['factor']})")
                st.caption(f"{p['kcal']:.0f} kcal | P: {p['p']:.1f}g | C: {p['c']:.1f}g")
            
            err = abs(tk - get) / get
            color = "#28a745" if err <= 0.05 else "#dc3545"
            st.markdown(f"""
            <div style="background:{color}; color:white; padding:8px; border-radius:5px; margin-top:10px">
                <b>Total: {tk:.0f} kcal</b> (Error: {((tk/get)-1)*100:.1f}%)
            </div>
            """, unsafe_allow_html=True)
