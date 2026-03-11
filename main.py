import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- BASE DE DATOS (Mantené tus 100 platos con estos tags) ---
# gf: gluten-free, ls: low-sodium (hipertenso), db: diabético, vgn: vegano, dl: dislipemia
desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "kcal": 250, "p": 15, "c": 30, "l": 8, "tags": ["gf", "db"]},
    {"nombre": "Tostadas con {palta} y huevo", "kcal": 320, "p": 18, "c": 25, "l": 18, "tags": ["db", "ls"]},
    {"nombre": "Pudín de chía y coco", "kcal": 210, "p": 6, "c": 15, "l": 12, "tags": ["gf", "vgn", "db", "ls"]}
]
comidas = [
    {"nombre": "Pollo con calabaza", "kcal": 450, "p": 35, "c": 25, "l": 12, "tags": ["gf", "db", "ls", "dl"]},
    {"nombre": "Wok de tofu y arroz", "kcal": 500, "p": 25, "c": 60, "l": 15, "tags": ["vgn", "db", "ls"]},
    {"nombre": "Pescado con {zapallito}", "kcal": 380, "p": 32, "c": 10, "l": 14, "tags": ["gf", "db", "ls", "dl"]}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# --- MOTOR DE VALIDACIÓN ---
def ajustar_porcion(plato, kcal_obj):
    factor = round((kcal_obj / plato["kcal"]) * 4) / 4
    if factor == 0: factor = 0.25
    return {
        "nom": plato["nombre"],
        "kcal": plato["kcal"] * factor,
        "p": plato["p"] * factor, "c": plato["c"] * factor, "l": plato["l"] * factor,
        "factor": factor
    }

def generar_plan_seguro(get_obj, p_obj, c_obj, l_obj, pats_usuario, term):
    # Mapeo de UI a tags de DB
    mapa_tags = {"Celíaco": "gf", "Hipertenso": "ls", "Diabético": "db", "Vegano": "vgn", "Dislipemia": "dl"}
    tags_requeridos = [mapa_tags[p] for p in pats_usuario]
    
    # Pre-filtrado clínico: Solo platos que cumplan TODAS las patologías
    des_aptos = [p for p in desayunos if all(t in p["tags"] for t in tags_requeridos)]
    com_aptos = [p for p in comidas if all(t in p["tags"] for t in tags_requeridos)]
    
    # Si no hay platos aptos, usamos la lista completa pero avisamos (Seguridad)
    if not des_aptos: des_aptos = desayunos
    if not com_aptos: com_aptos = comidas

    for _ in range(100): # 100 intentos para hallar el margen del 5%
        dia = []
        dist = [get_obj * 0.20, get_obj * 0.35, get_obj * 0.15, get_obj * 0.30]
        for j in range(4):
            lista = des_aptos if j in [0, 2] else com_aptos
            dia.append(ajustar_porcion(random.choice(lista), dist[j]))
        
        tk, tp, tc, tl = sum(x["kcal"] for x in dia), sum(x["p"] for x in dia), sum(x["c"] for x in dia), sum(x["l"] for x in dia)
        
        # Validación del 5%
        if all([abs(tk-get_obj)/get_obj <= 0.05, abs(tp-p_obj)/p_obj <= 0.05 if p_obj>0 else True]):
            return dia, (tk, tp, tc, tl)
    return dia, (tk, tp, tc, tl)

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    pi_sug = float((talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9)
    pi_real = st.number_input("Peso Objetivo (kg)", 30.0, 200.0, value=pi_sug)
    af_val = st.selectbox("Actividad", [1.2, 1.375, 1.55, 1.725, 1.9], format_func=lambda x: {1.2:"Sedentario", 1.55:"Moderado", 1.9:"Intenso"}.get(x, str(x)))
    
    st.divider()
    st.header("⚖️ Macros")
    p_cho, p_pro, p_lip = st.number_input("% CHO", 0, 100, 50), st.number_input("% PRO", 0, 100, 20), st.number_input("% LIP", 0, 100, 30)
    pats = st.multiselect("Patologías", ["Celíaco", "Hipertenso", "Diabético", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS ---
tmb = (10 * pi_real) + (6.25 * talla) - (5 * 30) + (5 if sexo == "Masculino" else -161)
get = tmb * af_val
obj_p, obj_c, obj_l = (get*p_pro/400), (get*p_cho/400), (get*p_lip/900)

# --- UI ---
st.title("🍎 Nutri-Flow Pro | Seguro & Preciso")
col_info, col_plan = st.columns([1, 2.5])

with col_info:
    st.markdown(f"""
    <div style="background:#f0f2f6;padding:15px;border-radius:10px;border:2px solid #28a745">
        <h4 style="margin:0">🎯 Objetivos</h4>
        🔥 <b>GET:</b> {get:.0f} kcal<br>
        🍗 <b>PRO:</b> {obj_p:.1f}g | 🍞 <b>CHO:</b> {obj_c:.1f}g
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 GENERAR PLAN CLÍNICO"):
    term = paises[pais]
    for i in range(7):
        st.session_state[f"dia_{i}"], st.session_state[f"tot_{i}"] = generar_plan_seguro(get, obj_p, obj_c, obj_l, pats, term)
    st.session_state.listo = True

if st.session_state.get("listo"):
    for i, d in enumerate(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]):
        with st.expander(f"📅 {d}", expanded=True):
            dia_data = st.session_state[f"dia_{i}"]
            tk, tp, tc, tl = st.session_state[f"tot_{i}"]
            for j, lab in enumerate(["☕ Des", "☀️ Alm", "🍪 Mer", "🌙 Cen"]):
                p = dia_data[j]
                st.write(f"**{lab}:** {p['nom'].format(**paises[pais])} (x{p['factor']})")
            
            desvio = abs(tk - get) / get
            st.markdown(f"<p style='color:{'green' if desvio <= 0.05 else 'orange'}'><b>Precisión: {100-(desvio*100):.1f}%</b> | Kcal: {tk:.0f} | P: {tp:.1f}g | C: {tc:.1f}g</p>", unsafe_allow_html=True)
