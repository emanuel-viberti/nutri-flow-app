import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- DATA ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# Base de datos (asegurate de tener tus 100 platos aquí)
desayunos = [{"nombre": "Yogur con granola y {frutilla}", "kcal": 250, "p": 15, "c": 30, "l": 8, "tags": []}]
comidas = [{"nombre": "Pollo con calabaza", "kcal": 450, "p": 35, "c": 25, "l": 12, "tags": []},
           {"nombre": "Wok de tofu y arroz", "kcal": 500, "p": 25, "c": 60, "l": 15, "tags": []}]

# --- LÓGICA DE PRECISIÓN ---
def ajustar_con_redondeo(plato, kcal_obj):
    factor = round((kcal_obj / plato["kcal"]) * 4) / 4
    if factor == 0: factor = 0.25
    return {
        "nom": plato["nombre"],
        "kcal": plato["kcal"] * factor,
        "p": plato["p"] * factor,
        "c": plato["c"] * factor,
        "l": plato["l"] * factor,
        "factor": factor
    }

def generar_dia_validado(get_obj, p_obj, c_obj, l_obj, term):
    # Intentará hasta 50 combinaciones por día para hallar una que cumpla el margen del 5%
    for _ in range(50):
        dia = []
        dist = [get_obj * 0.20, get_obj * 0.35, get_obj * 0.15, get_obj * 0.30]
        for j in range(4):
            lista = desayunos if j in [0, 2] else comidas
            dia.append(ajustar_con_redondeo(random.choice(lista), dist[j]))
        
        # Validar totales del día
        t_k = sum(item["kcal"] for item in dia)
        t_p = sum(item["p"] for item in dia)
        t_c = sum(item["c"] for item in dia)
        t_l = sum(item["l"] for item in dia)
        
        # Comprobar si el desvío es menor al 5% en todos los macros
        def dentro_de_margen(real, objetivo):
            if objetivo == 0: return True
            return abs(real - objetivo) / objetivo <= 0.05

        if all([dentro_de_margen(t_k, get_obj), dentro_de_margen(t_p, p_obj), 
                dentro_de_margen(t_c, c_obj), dentro_de_margen(t_l, l_obj)]):
            return dia, (t_k, t_p, t_c, t_l)
            
    return dia, (t_k, t_p, t_c, t_l) # Retorna la última si no halló ideal (poco probable)

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso (kg)", 30.0, 200.0, 80.0)
    pi_sug = float((talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, value=pi_sug)
    af_val = st.selectbox("Actividad", [1.2, 1.375, 1.55, 1.725, 1.9], format_func=lambda x: {1.2:"Sedentario", 1.55:"Moderado", 1.9:"Intenso"}.get(x, str(x)))
    
    st.divider()
    st.header("⚖️ Macros")
    p_cho = st.number_input("% CHO", 0, 100, 50)
    p_pro = st.number_input("% PRO", 0, 100, 20)
    p_lip = st.number_input("% LIP", 0, 100, 30)
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS ---
tmb = (10 * pi_real) + (6.25 * talla) - (5 * 30) + (5 if sexo == "Masculino" else -161)
get = tmb * af_val
obj_p, obj_c, obj_l = (get*p_pro/400), (get*p_cho/400), (get*p_lip/900)

# --- UI ---
st.title("🍎 Nutri-Flow Pro | Control de Margen 5%")
c_info, c_plan = st.columns([1, 2.5])

with c_info:
    st.markdown(f"""
    <div style="background:#f0f2f6;padding:15px;border-radius:10px;color:black;border:2px solid #007bff">
        <h4 style="margin:0">🎯 Objetivos</h4>
        🔥 <b>Kcal:</b> {get:.0f}<br>
        🍗 <b>PRO:</b> {obj_p:.1f}g<br>
        🍞 <b>CHO:</b> {obj_c:.1f}g<br>
        🥑 <b>LIP:</b> {obj_l:.1f}g
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 GENERAR PLAN VALIDADO"):
    term = paises[pais]
    for i in range(7):
        st.session_state[f"dia_{i}"], st.session_state[f"tot_{i}"] = generar_dia_validado(get, obj_p, obj_c, obj_l, term)
    st.session_state.listo = True

if st.session_state.get("listo"):
    for i, d in enumerate(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]):
        with st.expander(f"📅 {d}", expanded=True):
            dia_data = st.session_state[f"dia_{i}"]
            t_k, t_p, t_c, t_l = st.session_state[f"tot_{i}"]
            
            for j, lab in enumerate(["☕ Des", "☀️ Alm", "🍪 Mer", "🌙 Cen"]):
                p = dia_data[j]
                st.write(f"**{lab}:** {p['nom'].format(**paises[pais])} (x{p['factor']})")
            
            # Semáforo de precisión
            desvio = abs(t_k - get) / get
            color = "green" if desvio <= 0.05 else "red"
            st.markdown(f"<p style='color:{color}; font-weight:bold'>Precisión: {100-(desvio*100):.1f}% | Kcal: {t_k:.0f} | P: {t_p:.1f}g | C: {t_c:.1f}g | L: {t_l:.1f}g</p>", unsafe_allow_html=True)
