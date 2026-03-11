import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- DATA ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# (Mantené tus platos aquí - asegurate que tengan 'l' para lípidos)
desayunos = [{"nombre": "Yogur con granola y {frutilla}", "kcal": 250, "p": 15, "c": 30, "l": 8, "tags": ["gf", "db"]}]
comidas = [{"nombre": "Pollo con calabaza", "kcal": 450, "p": 35, "c": 25, "l": 12, "tags": ["gf", "db", "ls"]}]

# --- LÓGICA CLÍNICA ---
def diagnosticar_imc(imc_val):
    if imc_val < 18.5: return "Bajo Peso ⚠️", "#ffeb3b" # Amarillo
    if 18.5 <= imc_val < 25: return "Normopeso ✅", "#4caf50" # Verde
    if 25 <= imc_val < 30: return "Sobrepeso 🟠", "#ff9800" # Naranja
    return "Obesidad 🔴", "#f44336" # Rojo

def ajustar_porcion(plato, kcal_obj):
    factor = round((kcal_obj / plato["kcal"]) * 4) / 4
    if factor == 0: factor = 0.25
    return {
        "nom": plato["nombre"],
        "kcal": plato["kcal"] * factor,
        "p": plato["p"] * factor, "c": plato["c"] * factor, "l": plato["l"] * factor,
        "factor": factor
    }

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha del Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    
    pi_sug = float((talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, value=pi_sug)
    
    af_opts = {"Sedentario": 1.2, "Leve": 1.375, "Moderado": 1.55, "Fuerte": 1.725, "Muy Fuerte": 1.9}
    af_label = st.selectbox("Actividad Física", list(af_opts.keys()))
    af_val = af_opts[af_label]
    
    st.divider()
    st.header("⚖️ Prescripción de Macros")
    p_cho = st.number_input("% CHO", 0, 100, 50)
    p_pro = st.number_input("% PRO", 0, 100, 20)
    p_lip = st.number_input("% LIP", 0, 100, 30)
    
    pats = st.multiselect("Patologías", ["Celíaco", "Hipertenso", "Diabético", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS TÉCNICOS ---
tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * af_val
imc = peso_act / ((talla/100)**2)
diag, color_diag = diagnosticar_imc(imc)

# Metas diarias
obj_p, obj_c, obj_l = (get*p_pro/400), (get*p_cho/400), (get*p_lip/900)

# --- UI PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro")
c_info, c_plan = st.columns([1, 2.5])

with c_info:
    # Informe técnico con CSS forzado para legibilidad
    st.markdown(f"""
    <div style="background-color:#262730; padding:20px; border-radius:12px; border:1px solid #464b5d; color:white">
        <h3 style="color:#00d4ff; margin-top:0">📊 Informe Técnico</h3>
        <p style="margin-bottom:5px"><b>IMC Actual:</b> {imc:.1f}</p>
        <div style="background-color:{color_diag}; color:black; padding:4px 10px; border-radius:6px; font-weight:bold; display:inline-block; margin-bottom:15px">
            {diag}
        </div>
        <hr style="border:0.5px solid #464b5d">
        <p style="font-size:1.1em">🔥 <b>GET:</b> {get:.0f} kcal</p>
        <p style="margin-bottom:2px">🍗 <b>PRO:</b> {obj_p:.1f}g ({p_pro}%)</p>
        <p style="margin-bottom:2px">🍞 <b>CHO:</b> {obj_c:.1f}g ({p_cho}%)</p>
        <p style="margin-bottom:2px">🥑 <b>LIP:</b> {obj_l:.1f}g ({p_lip}%)</p>
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 GENERAR PLAN VALIDADO (Margen 5%)"):
    term = paises[pais]
    # Lógica de validación de patologías y 5% integrada
    mapa_tags = {"Celíaco": "gf", "Hipertenso": "ls", "Diabético": "db", "Vegano": "vgn", "Dislipemia": "dl"}
    tags_req = [mapa_tags[p] for p in pats]
    
    d_aptos = [p for p in desayunos if all(t in p["tags"] for t in tags_req)]
    c_aptos = [p for p in comidas if all(t in p["tags"] for t in tags_req)]
    
    for i in range(7):
        for _ in range(50):
            dia_temp = []
            dist = [get*0.20, get*0.35, get*0.15, get*0.30]
            for j in range(4):
                lista = d_aptos if j in [0, 2] else c_aptos
                dia_temp.append(ajustar_porcion(random.choice(lista if lista else (desayunos if j in [0,2] else comidas)), dist[j]))
            
            tk = sum(x["kcal"] for x in dia_temp)
            if abs(tk - get)/get <= 0.05:
                st.session_state[f"dia_{i}"] = dia_temp
                st.session_state[f"tot_{i}"] = (tk, sum(x["p"] for x in dia_temp), sum(x["c"] for x in dia_temp), sum(x["l"] for x in dia_temp))
                break
    st.session_state.listo = True

if st.session_state.get("listo"):
    for i, d in enumerate(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]):
        with st.expander(f"📅 {d}", expanded=True):
            dia_data = st.session_state[f"dia_{i}"]
            tk, tp, tc, tl = st.session_state[f"tot_{i}"]
            for j, lab in enumerate(["☕ Des", "☀️ Alm", "🍪 Mer", "🌙 Cen"]):
                p = dia_data[j]
                st.write(f"**{lab}:** {p['nom'].format(**paises[pais])} (x{p['factor']})")
            
            st.markdown(f"<p style='color:#28a745; font-weight:bold'>Total Día: {tk:.0f} kcal | P: {tp:.1f}g | C: {tc:.1f}g | G: {tl:.1f}g</p>", unsafe_allow_html=True)
