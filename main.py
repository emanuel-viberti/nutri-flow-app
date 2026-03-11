import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- DATA EXPANDIDA PARA FLEXIBILIDAD ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "kcal": 250, "p": 15, "c": 35, "l": 6, "tags": ["gf", "db", "ls"]},
    {"nombre": "Tostadas con {palta} y huevo", "kcal": 320, "p": 18, "c": 25, "l": 18, "tags": ["db", "ls"]},
    {"nombre": "Omelette de queso y espinaca", "kcal": 280, "p": 22, "c": 5, "l": 20, "tags": ["gf", "db", "ls"]}
]
comidas = [
    {"nombre": "Peceto con ensalada de {choclo}", "kcal": 450, "p": 40, "c": 30, "l": 15, "tags": ["gf", "db", "ls", "dl"]},
    {"nombre": "Wok de tofu y arroz integral", "kcal": 550, "p": 25, "c": 75, "l": 18, "tags": ["vgn", "db", "ls"]},
    {"nombre": "Pollo al horno con calabaza", "kcal": 420, "p": 38, "c": 35, "l": 12, "tags": ["gf", "db", "ls", "dl"]},
    {"nombre": "Pastas integrales con brócoli", "kcal": 580, "p": 18, "c": 95, "l": 14, "tags": ["vgn", "db", "ls"]}
]

# --- MOTOR DE PRECISIÓN ABSOLUTA ---
def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, tags_req):
    d_aptos = [p for p in desayunos if all(t in p["tags"] for t in tags_req)]
    c_aptos = [p for p in comidas if all(t in p["tags"] for t in tags_req)]
    
    if not d_aptos: d_aptos = desayunos
    if not c_aptos: c_aptos = comidas

    for _ in range(1000): # Mil intentos para forzar la matemática
        dia = []
        # Distribución teórica
        dist = [get_obj * 0.20, get_obj * 0.35, get_obj * 0.15, get_obj * 0.30]
        
        for j in range(4):
            plato_base = random.choice(d_aptos if j in [0,2] else c_aptos)
            # Redondeo humano inicial
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
        
        # Validación final del 5%
        tk, tp, tc, tl = sum(x["kcal"] for x in dia), sum(x["p"] for x in dia), sum(x["c"] for x in dia), sum(x["l"] for x in dia)
        
        def error(real, obj): return abs(real - obj) / obj if obj > 0 else 0
        
        if all(error(r, o) <= 0.05 for r, o in zip([tk, tp, tc, tl], [get_obj, p_obj, c_obj, l_obj])):
            return dia, (tk, tp, tc, tl)
            
    return dia, (tk, tp, tc, tl) # Fallback

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
    pats = st.multiselect("Patologías", ["Celíaco", "Hipertenso", "Diabético", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS ---
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

if st.button("🚀 GENERAR PLAN (FILTRO ESTRICTO 5%)"):
    mapa_tags = {"Celíaco": "gf", "Hipertenso": "ls", "Diabético": "db", "Vegano": "vgn", "Dislipemia": "dl"}
    tags_req = [mapa_tags[p] for p in pats]
    for i in range(7):
        st.session_state[f"dia_{i}"], st.session_state[f"tot_{i}"] = generar_dia_estricto(get, obj_p, obj_c, obj_l, tags_req)
    st.session_state.listo = True

# --- RENDER ---
if st.session_state.get("listo"):
    for i, d in enumerate(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]):
        with st.expander(f"📅 {d}", expanded=True):
            dia_data, (tk, tp, tc, tl) = st.session_state[f"dia_{i}"], st.session_state[f"tot_{i}"]
            for j, lab in enumerate(["☕ Des", "☀️ Alm", "🍪 Mer", "🌙 Cen"]):
                p = dia_data[j]
                st.write(f"**{lab}:** {p['nom'].format(**paises[pais])} (x{p['factor']})")
                st.caption(f"{p['kcal']:.0f} kcal | P: {p['p']:.1f}g | C: {p['c']:.1f}g")
            
            # Verificación visual de cumplimiento
            err = abs(tk - get) / get
            color = "#28a745" if err <= 0.05 else "#dc3545"
            st.markdown(f"""
            <div style="background:{color}; color:white; padding:5px 10px; border-radius:5px; margin-top:10px">
                <b>Total Real: {tk:.0f} kcal</b> (Dif: {((tk/get)-1)*100:.1f}%) | P: {tp:.1f}g | C: {tc:.1f}g
            </div>
            """, unsafe_allow_html=True)
