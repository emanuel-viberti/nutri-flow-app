import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- BASE DE DATOS MEJORADA (Con más proteína en desayunos para equilibrar) ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db"], "kcal": 250, "p": 15, "c": 30, "l": 8},
    {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "veg"], "kcal": 320, "p": 18, "c": 25, "l": 18},
    {"nombre": "Omelette de espinaca y queso", "tags": ["gf", "db"], "kcal": 280, "p": 22, "c": 5, "l": 15}
]
comidas = [
    {"nombre": "Pollo al grill con calabaza", "tags": ["gf", "db"], "kcal": 450, "p": 35, "c": 25, "l": 12},
    {"nombre": "Wok de tofu y arroz integral", "tags": ["vgn", "db"], "kcal": 500, "p": 25, "c": 60, "l": 15},
    {"nombre": "Pescado con {zapallito}", "tags": ["gf", "db"], "kcal": 380, "p": 32, "c": 10, "l": 14}
]

# --- LÓGICA DE REDONDEO Y AJUSTE ---
def redondear_porcion(valor):
    # Redondea a incrementos de 0.25 (1/4 de porción)
    return round(valor * 4) / 4

def ajustar_plato_pro(plato, kcal_obj):
    factor_crudo = kcal_obj / plato["kcal"]
    factor = redondear_porcion(factor_crudo)
    if factor == 0: factor = 0.25 # Evitar porciones cero
    
    return {
        "nom": plato["nombre"],
        "p": round(plato["p"] * factor, 1),
        "c": round(plato["c"] * factor, 1),
        "l": round(plato["l"] * factor, 1),
        "kcal": round(plato["kcal"] * factor),
        "factor": factor
    }

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, 72.0)
    
    opciones_af = {"Sedentario (1.2)": 1.2, "Leve (1.375)": 1.375, "Moderado (1.55)": 1.55, "Fuerte (1.725)": 1.725, "Muy Fuerte (1.9)": 1.9}
    af_label = st.selectbox("Actividad Física (AF)", list(opciones_af.keys()))
    af_valor = opciones_af[af_label]
    
    st.divider()
    st.header("⚖️ Prescripción de Macros")
    p_cho = st.number_input("% CHO", 0, 100, 50)
    p_pro = st.number_input("% PRO", 0, 100, 25) # Subimos default de PRO para mejor distribución
    p_lip = st.number_input("% LIP", 0, 100, 25)
    
    pats = st.multiselect("Patologías", ["Celíaco", "Hipertenso", "Diabético", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS ---
tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * af_valor
# Metas diarias en gramos
g_cho_obj = (get * p_cho / 400)
g_pro_obj = (get * p_pro / 400)
g_lip_obj = (get * p_lip / 900)

# Distribución calórica profesional: 25% - 30% - 15% - 30% (Más balanceado)
dist_kcal = [get * 0.25, get * 0.30, get * 0.15, get * 0.30]

# --- UI PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro | Clinical Edition")
c_info, c_plan = st.columns([1, 2.5])

with c_info:
    imc = peso_act / ((talla/100)**2)
    st.markdown(f"""
    <div style="background:#f8f9fa;padding:15px;border-radius:10px;border:1px solid #ddd;color:#333">
        <h4 style="margin-top:0">📊 Informe Técnico</h4>
        <b>GET:</b> {get:.0f} kcal<br>
        <b>IMC:</b> {imc:.1f}<hr>
        <b>Objetivos:</b><br>
        🍞 CHO: {g_cho_obj:.1f}g<br>
        🍗 PRO: {g_pro_obj:.1f}g<br>
        🥑 LIP: {g_lip_obj:.1f}g
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 GENERAR PLAN NUTRICIONAL PROFESIONAL"):
    term = paises[pais]
    for i in range(7):
        for j in range(4):
            lista = desayunos if j in [0, 2] else comidas
            # Buscamos plato que se acerque a la distribución de kcal
            st.session_state[f"d{i}_m{j}"] = ajustar_plato_pro(random.choice(lista), dist_kcal[j])
    st.session_state.listo = True

if st.session_state.get("listo"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    term = paises[pais]
    for i, d in enumerate(dias):
        with st.expander(f"📅 {d}", expanded=True):
            tot_k, tot_p, tot_c, tot_l = 0, 0, 0, 0
            for j, lab in enumerate(["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]):
                p = st.session_state[f"d{i}_m{j}"]
                st.markdown(f"**{lab}:** {p['nom'].format(**term)} (x{p['factor']})")
                st.caption(f"🔥 {p['kcal']} kcal | P: {p['p']}g | C: {p['c']}g | G: {p['l']}g")
                tot_k += p['kcal']; tot_p += p['p']; tot_c += p['c']; tot_l += p['l']
            
            # --- RESUMEN DIARIO DE CONTROL ---
            st.divider()
            st.markdown(f"**📊 Resumen del {d}**")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Kcal", f"{tot_k}", f"{tot_k - get:.0f} vs Obj", delta_color="inverse")
            col2.metric("PRO", f"{tot_p:.1f}g", f"{tot_p - g_pro_obj:.1f}g")
            col3.metric("CHO", f"{tot_c:.1f}g", f"{tot_c - g_cho_obj:.1f}g")
            col4.metric("LIP", f"{tot_l:.1f}g", f"{tot_l - g_lip_obj:.1f}g")
