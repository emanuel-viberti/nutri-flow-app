import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro | Gestión Clínica", page_icon="🍎", layout="wide")

# --- CSS PROFESIONAL ---
st.markdown("""
    <style>
    h1, h2, h3 { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #1e1e1e !important; font-weight: bold; }
    .day-card { 
        background-color: #ffffff; padding: 20px; border-radius: 12px; 
        border-left: 10px solid #2e7d32; margin-bottom: 20px; color: #1e1e1e !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .meal-box { margin-bottom: 12px; padding: 8px; border-bottom: 1px solid #eee; }
    .receta-text { font-size: 0.85em; color: #555; font-style: italic; display: block; margin-top: 2px; }
    .macro-tag { font-size: 0.75em; background: #e8f5e9; color: #2e7d32; padding: 2px 6px; border-radius: 4px; }
    .metric-box { background: #f0f2f6; padding: 15px; border-radius: 10px; color: #333; border: 2px solid #ccc; margin-bottom: 10px;}
    .pi-box { background: #e3f2fd; border: 1px solid #2196f3; padding: 10px; border-radius: 8px; color: #0d47a1; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS --- (Se mantiene igual)
desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db", "ls"], "receta": "200g yogur descremado + 3 cdas granola.", "pro": 8, "cho": 30},
    {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "veg", "ls"], "receta": "1 tostada integral + 1/2 palta + 1 huevo revuelto.", "pro": 12, "cho": 20},
    {"nombre": "Panqueque de avena y banana", "tags": ["db", "veg", "ls"], "receta": "1 huevo + 3 cdas avena + 1/2 banana a la sartén.", "pro": 10, "cho": 25},
    {"nombre": "Bowl de frutas y nueces", "tags": ["gf", "vgn", "db", "ls"], "receta": "Frutilla/Fresa picada + 3 nueces mariposa.", "pro": 4, "cho": 22}
]

comidas = [
    {"nombre": "Pollo al horno con calabaza", "tags": ["gf", "db", "ls", "dl"], "receta": "150g pechuga + 200g calabaza asada.", "pro": 30, "cho": 25},
    {"nombre": "Wok de vegetales y arroz integral", "tags": ["vgn", "db", "ls"], "receta": "Vegetales salteados + 1 taza arroz cocido.", "pro": 8, "cho": 45},
    {"nombre": "Pescado con {zapallito} grillado", "tags": ["gf", "db", "ls", "dl"], "receta": "Filete blanco + 2 {zapallito} en rodajas.", "pro": 28, "cho": 10},
    {"nombre": "Ensalada de quinoa y {choclo}", "tags": ["gf", "vgn", "ls", "db"], "receta": "1 taza quinoa + 1/2 {choclo} + tomate.", "pro": 10, "cho": 50},
    {"nombre": "Tarta de {zapallito} integral", "tags": ["veg", "db", "ls"], "receta": "Masa integral + relleno de {zapallito} y claras.", "pro": 12, "cho": 35}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa"}
}

# --- SIDEBAR: FICHA ANTROPOMÉTRICA ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    nombre = st.text_input("Nombre", "Emanuel")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    edad = st.number_input("Edad", 1, 110, 30)
    peso_actual = st.number_input("Peso Actual (kg)", 10.0, 300.0, 75.0)
    talla = st.number_input("Talla (cm)", 50, 250, 175)
    
    # Sugerencia de Peso Ideal (Fórmula de Lorentz simplificada)
    pi_sugerido = (talla - 100) - ((talla - 150) / (4 if sexo == "Masculino" else 2))
    
    st.markdown(f"""<div class="pi-box">💡 <b>Sugerencia PI:</b> {pi_sugerido:.1f} kg</div>""", unsafe_allow_html=True)
    
    peso_objetivo = st.number_input("Peso Objetivo (para cálculo kcal)", 10.0, 300.0, float(pi_sugerido))

    actividad_desc = st.selectbox("Actividad Física", [
        "Sedentario (1.2)", "Leve (1.375)", 
        "Moderado (1.55)", "Fuerte (1.725)", "Muy Fuerte (1.9)"
    ])
    naf = float(actividad_desc.split("(")[1].replace(")", ""))

    st.divider()
    st.header("⚖️ Macros (%)")
    col_c, col_p, col_g = st.columns(3)
    with col_c: p_carb = st.number_input("CHO", 0, 100, 50)
    with col_p: p_prot = st.number_input("PRO", 0, 100, 20)
    with col_g: p_gras = st.number_input("LIP", 0, 100, 30)
    
    st.divider()
    pats = st.multiselect("Patologías:", ["Celíaco", "Hipertenso", "Diabético", "Vegetariano", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- LÓGICA MÉDICA ---
# Cálculo basado en PESO OBJETIVO
tmb = (10 * peso_objetivo) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * naf
imc_actual = peso_actual / ((talla/100)**2)

def obtener_menu(lista, filtros, term):
    res = lista.copy()
    if "Celíaco" in filtros: res = [r for r in res if "gf" in r["tags"]]
    if "Hipertenso" in filtros: res = [r for r in res if "ls" in r["tags"]]
    if "Diabético" in filtros: res = [r for r in res if "db" in r["tags"]]
    if "Vegano" in filtros: res = [r for r in res if "vgn" in r["tags"]]
    if "Dislipemia" in filtros: res = [r for r in res if "dl" in r["tags"]]
    plato = random.choice(res if res else lista)
    return {"nom": plato["nombre"].format(**term), "rec": plato["receta"].format(**term), "p": plato.get("pro", 0), "c": plato.get("cho", 0)}

# --- MAIN UI ---
st.title("🍎 Nutri-Flow Pro")

col_m, col_p = st.columns([1, 2])

with col_m:
    st.markdown(f"""
    <div class="metric-box">
        <h4>📊 Informe de Consultorio</h4>
        <b>IMC Actual:</b> {imc_actual:.1f}<br>
        <b>Peso Objetivo:</b> {peso_objetivo:.1f} kg<br>
        <b>GET (basado en Objetivo):</b> {get:.0f} kcal/día<br>
        <hr>
        <b>Distribución:</b><br>
        🍞 CHO: {(get * p_carb / 400):.1f}g<br>
        🍗 PRO: {(get * p_prot / 400):.1f}g<br>
        🥑 LIP: {(get * p_gras / 900):.1f}g
    </div>
    """, unsafe_allow_html=True)

with col_p:
    if (p_carb + p_prot + p_gras) == 100:
        if st.button("🚀 GENERAR PLAN SEMANAL"):
            st.session_state.listo = True
            term = paises[pais]
            for i in range(7):
                st.session_state[f"d_{i}"] = [obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term), 
                                              obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term)]
    else:
        st.error("La suma de macros debe ser 100%.")

if "listo" in st.session_state:
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    term = paises[pais]
    for i, d_nom in enumerate(dias):
        with st.container():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f'<div class="day-card"><div style="color:#2e7d32; font-weight:bold; font-size:1.2em; border-bottom:1px solid #eee; margin-bottom:10px;">📅 {d_nom}</div>', unsafe_allow_html=True)
                labels = ["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]
                for j, lab in enumerate(labels):
                    item = st.session_state[f"d_{i}"][j]
                    st.markdown(f'<div class="meal-box"><b>{lab}:</b> {item["nom"]} <span class="macro-tag">P: {item["p"]}g | C: {item["c"]}g</span><span class="receta-text">📖 {item["rec"]}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.write(" ")
                if st.button("🔄", key=f"re_{i}"):
                    st.session_state[f"d_{i}"] = [obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term), 
                                                  obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term)]
                    st.rerun()
