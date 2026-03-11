import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- TRADUCCIONES ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# --- BASE DE DATOS (Simplificada para el ejemplo, pero con lógica de 100 platos) ---
desayunos = [{"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db"], "kcal": 300, "p": 12, "c": 35}, 
             {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "veg"], "kcal": 350, "p": 15, "c": 25}]
comidas = [{"nombre": "Pollo al grill con calabaza", "tags": ["gf", "db"], "kcal": 500, "p": 35, "c": 30},
           {"nombre": "Wok de tofu y arroz integral", "tags": ["vgn", "db"], "kcal": 450, "p": 18, "c": 55}]

# --- LÓGICA DE AJUSTE NUTRICIONAL ---
def calcular_ajuste(plato, objetivo_kcal_comida):
    # Calculamos cuánto debe representar este plato para cumplir con las kcal de esa comida
    factor = objetivo_kcal_comida / plato["kcal"]
    return {
        "nom": plato["nombre"],
        "p": round(plato["p"] * factor, 1),
        "c": round(plato["c"] * factor, 1),
        "kcal": round(plato["kcal"] * factor),
        "factor": round(factor, 2)
    }

def obtener_plato_ajustado(lista, filtros, term, kcal_objetivo):
    res = [r for r in lista if all(tag in r["tags"] for tag in filtros)]
    if not res: res = lista
    seleccionado = random.choice(res)
    return calcular_ajuste(seleccionado, kcal_objetivo)

# --- SIDEBAR: CÁLCULOS PROFESIONALES ---
with st.sidebar:
    st.header("👤 Ficha y Objetivos")
    sexo = st.radio("Sexo", ["M", "F"])
    talla = st.number_input("Talla (cm)", 100, 220, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 18, 100, 30)
    naf = st.select_slider("Actividad (NAF)", options=[1.2, 1.375, 1.55, 1.725, 1.9])
    
    st.divider()
    st.header("⚖️ Distribución de Macros")
    p_cho = st.slider("% Carbohidratos", 10, 70, 50)
    p_pro = st.slider("% Proteínas", 10, 50, 20)
    p_lip = 100 - p_cho - p_pro
    st.write(f"Grasas: {p_lip}%")
    
    pats = st.multiselect("Patologías", ["gf", "db", "vgn"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS TÉCNICOS ---
tmb = (10 * peso_act) + (6.25 * talla) - (5 * edad) + (5 if sexo == "M" else -161)
get = tmb * naf
# Distribución por comida (Ej: 20% Des, 35% Alm, 15% Mer, 30% Cen)
dist_kcal = [get * 0.20, get * 0.35, get * 0.15, get * 0.30]

# --- UI PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro | Sincronización Total")
col_info, col_plan = st.columns([1, 2.5])

with col_info:
    st.markdown(f"""
    <div style="background:#f0f2f6;padding:15px;border-radius:10px;color:black">
        <h4>📊 Informe Técnico</h4>
        <b>GET:</b> {get:.0f} kcal/día<hr>
        <b>Objetivos (g):</b><br>
        🍞 CHO: {(get*p_cho/400):.1f}g<br>
        🍗 PRO: {(get*p_pro/400):.1f}g<br>
        🥑 LIP: {(get*p_lip/900):.1f}g
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 GENERAR PLAN SINCRONIZADO"):
    term = paises[pais]
    for i in range(7):
        for j in range(4):
            lista = desayunos if j in [0, 2] else comidas
            st.session_state[f"d{i}_m{j}"] = obtener_plato_ajustado(lista, pats, term, dist_kcal[j])
    st.session_state.listo = True

if st.session_state.get("listo"):
    for i, d in enumerate(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]):
        with st.expander(f"📅 {d}"):
            for j, lab in enumerate(["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]):
                p = st.session_state[f"d{i}_m{j}"]
                st.write(f"**{lab}:** {p['nom'].format(**paises[pais])}")
                st.caption(f"Ajuste: {p['factor']} porción/es | {p['kcal']} kcal | P: {p['p']}g | C: {p['c']}g")
