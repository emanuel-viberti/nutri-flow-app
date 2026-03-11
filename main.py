import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- TRADUCCIONES Y DATA ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# (Base de datos con valores base por porción estándar)
desayunos = [{"nombre": "Yogur con granola y {frutilla}", "tags": ["gf"], "kcal": 250, "p": 12, "c": 35, "l": 6},
             {"nombre": "Tostadas con {palta} y huevo", "tags": ["db"], "kcal": 320, "p": 15, "c": 25, "l": 18}]
comidas = [{"nombre": "Pechuga con calabaza", "tags": ["gf"], "kcal": 450, "p": 35, "c": 30, "l": 10},
           {"nombre": "Wok de tofu y arroz", "tags": ["vgn"], "kcal": 500, "p": 20, "c": 65, "l": 12}]

# --- NUEVA LÓGICA DE COMPENSACIÓN ---
def generar_dia_balanceado(get_objetivo, g_pro_obj, g_cho_obj, g_lip_obj, pats, term):
    dia = []
    # Distribución de Kcal: Des 20%, Alm 35%, Mer 15%, Cen 30%
    dist_kcal = [get_objetivo * 0.20, get_objetivo * 0.35, get_objetivo * 0.15, get_objetivo * 0.30]
    
    for j in range(4):
        lista = desayunos if j in [0, 2] else comidas
        plato_base = random.choice(lista)
        
        # 1. Calculamos factor teórico exacto
        factor_teorico = dist_kcal[j] / plato_base["kcal"]
        # 2. Redondeamos a porción humana (cuartos)
        factor_humano = round(factor_teorico * 4) / 4
        if factor_humano == 0: factor_humano = 0.25
        
        # Guardamos el plato con valores reales según la porción redondeada
        dia.append({
            "nom": plato_base["nombre"].format(**term),
            "kcal": round(plato_base["kcal"] * factor_humano),
            "p": round(plato_base["p"] * factor_humano, 1),
            "c": round(plato_base["c"] * factor_humano, 1),
            "l": round(plato_base["l"] * factor_humano, 1),
            "factor": factor_humano
        })
    return dia

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Perfil Profesional")
    sexo = st.radio("Sexo", ["M", "F"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, 72.0)
    
    opciones_af = {"Sedentario": 1.2, "Leve": 1.375, "Moderado": 1.55, "Fuerte": 1.725, "Muy Fuerte": 1.9}
    af_label = st.selectbox("Actividad Física", list(opciones_af.keys()))
    af_valor = opciones_af[af_label]
    
    st.divider()
    st.header("⚖️ Macros Prescriptos")
    p_cho = st.number_input("% CHO", 0, 100, 50)
    p_pro = st.number_input("% PRO", 0, 100, 20)
    p_lip = st.number_input("% LIP", 0, 100, 30)
    total_pct = p_cho + p_pro + p_lip
    
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS ---
tmb = (10 * pi_real) + (6.25 * talla) - (5 * 30) + (5 if sexo == "M" else -161)
get = tmb * af_valor
g_cho_obj = (get * p_cho / 400)
g_pro_obj = (get * p_pro / 400)
g_lip_obj = (get * p_lip / 900)

# --- UI ---
st.title("🍎 Nutri-Flow Pro | Precisión Clínica")

if total_pct != 100:
    st.error(f"⚠️ La suma de macros es {total_pct}%. Debe ser 100% para calcular.")

col_info, col_plan = st.columns([1, 2.5])

with col_info:
    st.markdown(f"""
    <div style="background:#f0f2f6;padding:15px;border-radius:10px;color:black;border:1px solid #ccc">
        <h4>📊 Objetivos a cumplir:</h4>
        <b>Energía:</b> {get:.0f} kcal<br>
        <b>Proteína:</b> {g_pro_obj:.1f}g<br>
        <b>Carbo:</b> {g_cho_obj:.1f}g<br>
        <b>Grasas:</b> {g_lip_obj:.1f}g
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 GENERAR PLAN Y VALIDAR"):
    if total_pct == 100:
        term = paises[pais]
        for i in range(7):
            st.session_state[f"dia_{i}"] = generar_dia_balanceado(get, g_pro_obj, g_cho_obj, g_lip_obj, [], term)
        st.session_state.listo = True

if st.session_state.get("listo"):
    dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for i, d_nom in enumerate(dias_nombres):
        with st.expander(f"📅 {d_nom}", expanded=True):
            dia_data = st.session_state[f"dia_{i}"]
            tk, tp, tc, tl = 0, 0, 0, 0
            
            for j, lab in enumerate(["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]):
                p = dia_data[j]
                st.write(f"**{lab}:** {p['nom']} (x{p['factor']})")
                st.caption(f"🔥 {p['kcal']} kcal | P: {p['p']}g | C: {p['c']}g | G: {p['l']}g")
                tk += p['kcal']; tp += p['p']; tc += p['c']; tl += p['l']
            
            # --- VALIDACIÓN FINAL DEL
