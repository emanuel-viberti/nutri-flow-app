import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- BASE DE DATOS ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# (Usa tus listas de 100 platos aquí; mantengo 2 de ejemplo para que el código corra)
desayunos = [{"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db", "ls"], "kcal": 250, "p": 12, "c": 30, "l": 8},
             {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "ls", "veg"], "kcal": 320, "p": 15, "c": 25, "l": 18}]
comidas = [{"nombre": "Pollo al grill con calabaza", "tags": ["gf", "db", "ls", "dl"], "kcal": 450, "p": 35, "c": 25, "l": 12},
           {"nombre": "Wok de tofu y arroz integral", "tags": ["vgn", "db", "ls"], "kcal": 500, "p": 18, "c": 60, "l": 15}]

# --- LÓGICA ---
def ajustar_plato(plato, kcal_obj):
    factor = kcal_obj / plato["kcal"]
    return {
        "nom": plato["nombre"],
        "p": round(plato["p"] * factor, 1),
        "c": round(plato["c"] * factor, 1),
        "l": round(plato["l"] * factor, 1),
        "kcal": round(plato["kcal"] * factor),
        "factor": round(factor, 2)
    }

def buscar_plato(lista, pats_sel, kcal_obj):
    mapa = {"Celíaco": "gf", "Hipertenso": "ls", "Diabético": "db", "Vegano": "vgn", "Dislipemia": "dl"}
    tags_req = [mapa[p] for p in pats_sel]
    filtrados = [p for p in lista if all(t in p["tags"] for t in tags_req)]
    sel = random.choice(filtrados if filtrados else lista)
    return ajustar_plato(sel, kcal_obj)

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    
    # Peso Ideal Editable
    pi_sugerido = (talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9
    pi_real = st.number_input("Peso Objetivo / Ideal (kg)", 30.0, 200.0, float(pi_sugerido))
    
    # AF Desplegable (Vuelve a tu formato favorito)
    opciones_af = {
        "Sedentario (1.2)": 1.2,
        "Leve (1.375)": 1.375,
        "Moderado (1.55)": 1.55,
        "Fuerte (1.725)": 1.725,
        "Muy Fuerte (1.9)": 1.9
    }
    af_label = st.selectbox("Actividad Física (AF)", list(opciones_af.keys()))
    af_valor = opciones_af[af_label]
    
    st.divider()
    st.header("⚖️ Prescripción de Macros")
    p_cho = st.number_input("% Carbohidratos", 0, 100, 50)
    p_pro = st.number_input("% Proteínas", 0, 100, 20)
    p_lip = st.number_input("% Grasas", 0, 100, 30)
    
    total_pct = p_cho + p_pro + p_lip
    if total_pct != 100:
        st.error(f"Suma: {total_pct}% (Debe ser 100%)")
        
    pats = st.multiselect("Patologías", ["Celíaco", "Hipertenso", "Diabético", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS ---
tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * af_valor
imc = peso_act / ((talla/100)**2)

def diagnosticar_imc(imc_val):
    if imc_val < 18.5: return "Bajo Peso ⚠️", "#ffeb3b"
    if 18.5 <= imc_val < 25: return "Normopeso ✅", "#4caf50"
    if 25 <= imc_val < 30: return "Sobrepeso 🟠", "#ff9800"
    return "Obesidad 🔴", "#f44336"

diag, color_diag = diagnosticar_imc(imc)
dist_kcal = [get * 0.20, get * 0.35, get * 0.15, get * 0.30]

# --- UI PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro")
c_info, c_plan = st.columns([1, 2.5])

with c_info:
    st.markdown(f"""
    <div style="background:#f0f2f6;padding:15px;border-radius:10px;border:1px solid #ccc;color:#333">
        <h4>📊 Informe Técnico</h4>
        <b>IMC:</b> {imc:.1f} <br>
        <span style="background:{color_diag};padding:2px 6px;border-radius:5px;font-weight:bold;color:white">{diag}</span><br>
        <b>GET:</b> {get:.0f} kcal/día<hr>
        <b>Objetivos Diarios:</b><br>
        🍞 CHO: {(get*p_cho/400):.1f}g ({p_cho}%)<br>
        🍗 PRO: {(get*p_pro/400):.1f}g ({p_pro}%)<br>
        🥑 LIP: {(get*p_lip/900):.1f}g ({p_lip}%)
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 GENERAR PLAN NUTRICIONAL"):
    if total_pct == 100:
        term = paises[pais]
        for i in range(7):
            for j in range(4):
                lista = desayunos if j in [0, 2] else comidas
                st.session_state[f"d{i}_m{j}"] = buscar_plato(lista, pats, dist_kcal[j])
        st.session_state.listo = True
    else:
        st.warning("La suma de macros debe ser 100%.")

if st.session_state.get("listo"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    term = paises[pais]
    for i, d in enumerate(dias):
        with st.expander(f"📅 {d}", expanded=True):
            for j, lab in enumerate(["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]):
                key = f"d{i}_m{j}"
                if key in st.session_state:
                    p = st.session_state[key]
                    c_t, c_b = st.columns([0.85, 0.15])
                    with c_t:
                        st.markdown(f"**{lab}:** {p['nom'].format(**term)}")
                        st.caption(f"x{p['factor']} porción | {p['kcal']} kcal | P: {p['p']}g | C: {p['c']}g | G: {p['l']}g")
                    with c_b:
                        if st.button("🔄", key=f"sw_{i}_{j}"):
                            lista = desayunos if j in [0, 2] else comidas
                            st.session_state[key] = buscar_plato(lista, pats, dist_kcal[j])
                            st.rerun()
