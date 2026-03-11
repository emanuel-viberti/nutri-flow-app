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
        background-color: #ffffff; padding: 15px; border-radius: 12px; 
        border-left: 8px solid #2e7d32; margin-bottom: 25px; color: #1e1e1e !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .receta-text { font-size: 0.85em; color: #666; font-style: italic; display: block; }
    .macro-tag { font-size: 0.75em; background: #e8f5e9; color: #2e7d32; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    .metric-box { background: #f0f2f6; padding: 15px; border-radius: 10px; color: #333; border: 1px solid #ccc; margin-bottom: 10px;}
    .pi-box { background: #fff3e0; border: 1px solid #ff9800; padding: 10px; border-radius: 8px; color: #e65100; margin-bottom: 10px;}
    .stButton>button { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
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

# --- FUNCIONES ---
def obtener_diagnostico_imc(imc):
    if imc < 18.5: return "Bajo Peso", "#ffeb3b"
    if 18.5 <= imc < 25: return "Normopeso", "#4caf50"
    if 25 <= imc < 30: return "Sobrepeso", "#ff9800"
    if 30 <= imc < 35: return "Obesidad I", "#ff5722"
    if 35 <= imc < 40: return "Obesidad II", "#f44336"
    return "Obesidad III", "#b71c1c"

def seleccionar_plato(lista, filtros, term):
    res = [r for r in lista]
    if "Celíaco" in filtros: res = [r for r in res if "gf" in r["tags"]]
    if "Hipertenso" in filtros: res = [r for r in res if "ls" in r["tags"]]
    if "Diabético" in filtros: res = [r for r in res if "db" in r["tags"]]
    if "Vegano" in filtros: res = [r for r in res if "vgn" in r["tags"]]
    if "Dislipemia" in filtros: res = [r for r in res if "dl" in r["tags"]]
    plato = random.choice(res if res else lista)
    return {"nom": plato["nombre"].format(**term), "rec": plato["receta"].format(**term), "p": plato.get("pro", 0), "c": plato.get("cho", 0)}

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 50, 250, 175)
    peso_actual = st.number_input("Peso Actual (kg)", 10.0, 300.0, 75.0)
    edad = st.number_input("Edad", 1, 110, 30)
    
    pi_sugerido = (talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9
    st.markdown(f'<div class="pi-box">⚖️ <b>Sugerencia PI:</b> {pi_sugerido:.1f} kg</div>', unsafe_allow_html=True)
    peso_objetivo = st.number_input("Peso para el Cálculo (kg)", 10.0, 300.0, float(pi_sugerido))

    naf_ops = {"Sedentario": 1.2, "Leve": 1.375, "Moderado": 1.55, "Fuerte": 1.725, "Muy Fuerte": 1.9}
    actividad = st.selectbox("Actividad Física", list(naf_ops.keys()))
    naf = naf_ops[actividad]

    st.divider()
    st.header("⚖️ Macros (%)")
    c1, c2, c3 = st.columns(3)
    p_carb = c1.number_input("CHO", 0, 100, 50)
    p_prot = c2.number_input("PRO", 0, 100, 20)
    p_gras = c3.number_input("LIP", 0, 100, 30)
    
    pats = st.multiselect("Patologías:", ["Celíaco", "Hipertenso", "Diabético", "Vegetariano", "Vegano", "Dislipemia"])
    pais_sel = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS ---
tmb = (10 * peso_objetivo) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * naf
imc_act = peso_actual / ((talla/100)**2)
diag_t, diag_c = obtener_diagnostico_imc(imc_act)

# --- MAIN UI ---
st.title("🍎 Nutri-Flow Pro")
col_info, col_plan = st.columns([1, 2.2])

with col_info:
    st.markdown(f"""
    <div class="metric-box">
        <h4>📊 Informe de Consultorio</h4>
        <b>IMC:</b> {imc_act:.1f} <small style="color:{diag_c}; font-weight:bold;">[{diag_t}]</small><br>
        <b>Peso Ref:</b> {peso_objetivo:.1f} kg | <b>GET:</b> {get:.0f} kcal<br>
        <hr>
        <b>Objetivo Diario:</b><br>
        🍞 {(get * p_carb / 400):.1f}g CHO | 🍗 {(get * p_prot / 400):.1f}g PRO<br>
        🥑 {(get * p_gras / 900):.1f}g LIP
    </div>
    """, unsafe_allow_html=True)

with col_plan:
    if (p_carb + p_prot + p_gras) == 100:
        if st.button("🚀 GENERAR / RESETEAR TODO EL PLAN"):
            term = paises[pais_sel]
            for i in range(7):
                st.session_state[f"d{i}_m0"] = seleccionar_plato(desayunos, pats, term)
                st.session_state[f"d{i}_m1"] = seleccionar_plato(comidas, pats, term)
                st.session_state[f"d{i}_m2"] = seleccionar_plato(desayunos, pats, term)
                st.session_state[f"d{i}_m3"] = seleccionar_plato(comidas, pats, term)
            st.session_state.listo = True
    else:
        st.error("Los macros deben sumar 100%")

if st.session_state.get("listo"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    labels = ["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda
