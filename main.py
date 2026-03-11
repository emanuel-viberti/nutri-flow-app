import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- BASE DE DATOS ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# Ejemplo de platos (asegurate de cargar tus 100 aquí)
desayunos = [{"nombre": "Yogur con granola y {frutilla}", "kcal": 250, "p": 15, "c": 30, "l": 8, "tags": ["gf", "db", "ls"]}]
comidas = [{"nombre": "Pollo con calabaza", "kcal": 450, "p": 35, "c": 25, "l": 12, "tags": ["gf", "db", "ls", "dl"]},
           {"nombre": "Wok de tofu y arroz", "kcal": 500, "p": 25, "c": 60, "l": 15, "tags": ["vgn", "db", "ls"]}]

# --- LÓGICA DE PRECISIÓN ---
def ajustar_porcion(plato, kcal_obj):
    factor = round((kcal_obj / plato["kcal"]) * 4) / 4
    if factor == 0: factor = 0.25
    return {
        "nom": plato["nombre"],
        "kcal": plato["kcal"] * factor,
        "p": plato["p"] * factor, "c": plato["c"] * factor, "l": plato["l"] * factor,
        "factor": factor, "tags": plato["tags"]
    }

def validar_5_porciento(dia, get_obj, p_obj, c_obj, l_obj):
    tk, tp, tc, tl = sum(x["kcal"] for x in dia), sum(x["p"] for x in dia), sum(x["c"] for x in dia), sum(x["l"] for x in dia)
    def check(real, obj): return abs(real - obj) / obj <= 0.05 if obj > 0 else True
    return all([check(tk, get_obj), check(tp, p_obj), check(tc, c_obj), check(tl, l_obj)]), (tk, tp, tc, tl)

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha del Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    
    pi_sug = float((talla-100) if sexo=="Masculino" else (talla-100)*0.9)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, value=pi_sug)
    
    opciones_af = {1.2: "Sedentario", 1.375: "Leve", 1.55: "Moderado", 1.725: "Fuerte", 1.9: "Muy Fuerte"}
    af_val = st.selectbox("Actividad Física", options=list(opciones_af.keys()), format_func=lambda x: opciones_af[x])
    
    st.divider()
    st.header("⚖️ Prescripción de Macros")
    p_cho, p_pro, p_lip = st.number_input("% CHO", 0, 100, 50), st.number_input("% PRO", 0, 100, 20), st.number_input("% LIP", 0, 100, 30)
    pats = st.multiselect("Patologías", ["Celíaco", "Hipertenso", "Diabético", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS ---
tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * af_val
obj_p, obj_c, obj_l = (get*p_pro/400), (get*p_cho/400), (get*p_lip/900)
imc = peso_act / ((talla/100)**2)

def get_diag(i):
    if i < 18.5: return "Bajo Peso", "#ffeb3b"
    if i < 25: return "Normopeso", "#4caf50"
    if i < 30: return "Sobrepeso", "#ff9800"
    return "Obesidad", "#f44336"
diag, color_diag = get_diag(imc)

# --- UI DASHBOARD ---
c_info, c_plan = st.columns([1, 2.5])
with c_info:
    st.markdown(f"""
    <div style="background-color:#262730; padding:15px; border-radius:10px; color:white; border:1px solid #464b5d">
        <h4 style="color:#00d4ff; margin:0">📊 Informe Técnico</h4>
        <b>IMC:</b> {imc:.1f} <br>
        <div style="background-color:{color_diag}; color:black; padding:2px 8px; border-radius:4px; display:inline-block; font-weight:bold; margin:5px 0">
            {diag}
        </div><hr style="border:0.1px solid #464b5d">
        🔥 <b>GET:</b> {get:.0f} kcal<br>
        🍗 <b>P:</b> {obj_p:.1f}g | 🍞 <b>C:</b> {obj_c:.1f}g | 🥑 <b>G:</b> {obj_l:.1f}g
    </div>
    """, unsafe_allow_html=True)

# --- MOTOR DE BÚSQUEDA ---
mapa_tags = {"Celíaco": "gf", "Hipertenso": "ls", "Diabético": "db", "Vegano": "vgn", "Dislipemia": "dl"}
tags_req = [mapa_tags[p] for p in pats]

def buscar_plato_seguro(lista, kcal_target):
    aptos = [p for p in lista if all(t in p["tags"] for t in tags_req)]
    return ajustar_porcion(random.choice(aptos if aptos else lista), kcal_target)

if st.button("🚀 GENERAR PLAN NUTRICIONAL"):
    for i in range(7):
        for _ in range(100):
            dia_temp = [buscar_plato_seguro(desayunos, get*0.20), buscar_plato_seguro(comidas, get*0.35),
                        buscar_plato_seguro(desayunos, get*0.15), buscar_plato_seguro(comidas, get*0.30)]
            ok, tot = validar_5_porciento(dia_temp, get, obj_p, obj_c, obj_l)
            if ok:
                st.session_state[f"dia_{i}"], st.session_state[f"tot_{i}"] = dia_temp, tot
                break
    st.session_state.listo = True

# --- RENDERIZADO ---
if st.session_state.get("listo"):
    for i, d in enumerate(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]):
        with st.expander(f"📅 {d}", expanded=True):
            dia_data, (tk, tp, tc, tl) = st.session_state[f"dia_{i}"], st.session_state[f"tot_{i}"]
            for j, lab in enumerate(["☕ Des", "☀️ Alm", "🍪 Mer", "🌙 Cen"]):
                c_t, c_b = st.columns([0.85, 0.15])
                p = dia_data[j]
                with c_t:
                    st.write(f"**{lab}:** {p['nom'].format(**paises[pais])} (x{p['factor']})")
                    st.caption(f"{p['kcal']:.0f} kcal | P: {p['p']:.1f}g | C: {p['c']:.1f}g | G: {p['l']:.1f}g")
                with c_b:
                    if st.button("🔄", key=f"sw_{i}_{j}"):
                        st.session_state[f"dia_{i}"][j] = buscar_plato_seguro(desayunos if j in [0,2] else comidas, (get * [0.2, 0.35, 0.15, 0.3][j]))
                        d_n = st.session_state[f"dia_{i}"]
                        st.session_state[f"tot_{i}"] = (sum(x["kcal"] for x in d_n), sum(x["p"] for x in d_n), sum(x["c"] for x in d_n), sum(x["l"] for x in d_n))
                        st.rerun()
            st.markdown(f"**Total Real:** {tk:.0f} kcal | P: {tp:.1f}g | C: {tc:.1f}g | G: {tl:.1f}g")
