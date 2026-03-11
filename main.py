import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- BASE DE DATOS ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# 40 Desayunos/Meriendas y 60 Almuerzos/Cenas (Simplificado para estabilidad de copia)
# Nota: He mantenido la estructura para que los tags funcionen con tu multiselect
desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db", "ls"], "kcal": 250, "p": 10, "c": 30, "l": 5},
    {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "ls", "veg"], "kcal": 320, "p": 14, "c": 22, "l": 18},
    {"nombre": "Omelette de espinaca y queso", "tags": ["gf", "db", "ls", "dl"], "kcal": 280, "p": 20, "c": 5, "l": 15},
    {"nombre": "Pudín de chía y coco", "tags": ["gf", "vgn", "db"], "kcal": 210, "p": 6, "c": 15, "l": 12},
] # ... (puedes rellenar hasta 40)

comidas = [
    {"nombre": "Pechuga al grill con calabaza", "tags": ["gf", "db", "ls", "dl"], "kcal": 450, "p": 35, "c": 25, "l": 10},
    {"nombre": "Wok de tofu y arroz integral", "tags": ["vgn", "db", "ls"], "kcal": 520, "p": 18, "c": 60, "l": 12},
    {"nombre": "Pescado con {zapallito}", "tags": ["gf", "db", "ls", "dl"], "kcal": 380, "p": 32, "c": 10, "l": 14},
    {"nombre": "Ensalada de quinoa y {choclo}", "tags": ["gf", "vgn", "db"], "kcal": 410, "p": 12, "c": 55, "l": 8},
] # ... (puedes rellenar hasta 60)

# --- LÓGICA NUTRICIONAL ---
def diagnosticar_imc(imc):
    if imc < 18.5: return "Bajo Peso ⚠️", "#ffeb3b"
    if 18.5 <= imc < 25: return "Normopeso ✅", "#4caf50"
    if 25 <= imc < 30: return "Sobrepeso 🟠", "#ff9800"
    return "Obesidad 🔴", "#f44336"

def ajustar_a_objetivo(plato, kcal_objetivo):
    # El factor de ajuste se basa en las calorías necesarias para ese momento del día
    factor = kcal_objetivo / plato["kcal"]
    return {
        "nom": plato["nombre"],
        "p": round(plato["p"] * factor, 1),
        "c": round(plato["c"] * factor, 1),
        "l": round(plato["l"] * factor, 1),
        "kcal": round(plato["kcal"] * factor),
        "factor": round(factor, 2)
    }

def buscar_plato(lista, pats_seleccionadas, kcal_objetivo):
    # Mapeo de nombres de UI a tags de base de datos
    mapa_tags = {"Celíaco": "gf", "Hipertenso": "ls", "Diabético": "db", "Vegano": "vgn", "Dislipemia": "dl"}
    tags_busqueda = [mapa_tags[p] for p in pats_seleccionadas]
    
    # Filtrado por patología
    filtrados = [p for p in lista if all(t in p["tags"] for t in tags_busqueda)]
    seleccionado = random.choice(filtrados if filtrados else lista)
    return ajustar_a_objetivo(seleccionado, kcal_objetivo)

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Perfil del Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 230, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    naf = st.select_slider("Actividad (NAF)", options=[1.2, 1.375, 1.55, 1.725, 1.9], format_func=lambda x: {1.2:"Sedentario", 1.375:"Leve", 1.55:"Moderado", 1.725:"Fuerte", 1.9:"Muy Fuerte"}[x])
    
    st.divider()
    st.header("⚖️ Prescripción de Macros")
    p_cho = st.slider("% CHO", 10, 70, 50)
    p_pro = st.slider("% PRO", 10, 50, 20)
    p_lip = 100 - p_cho - p_pro
    st.caption(f"Grasas: {p_lip}% (calculado automáticamente)")
    
    pats = st.multiselect("Patologías", ["Celíaco", "Hipertenso", "Diabético", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS TÉCNICOS ---
tmb = (10 * peso_act) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * naf
imc = peso_act / ((talla/100)**2)
diag, color_diag = diagnosticar_imc(imc)

# Distribución calórica por comida: 20% - 35% - 15% - 30%
kcal_por_momento = [get * 0.20, get * 0.35, get * 0.15, get * 0.30]

# --- INTERFAZ PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro")
col_info, col_plan = st.columns([1, 2.5])

with col_info:
    st.markdown(f"""
    <div style="background:#f0f2f6;padding:15px;border-radius:10px;border:1px solid #ccc;color:#333">
        <h4>📊 Diagnóstico Nutricional</h4>
        <b>IMC:</b> {imc:.1f} <br>
        <span style="background:{color_diag};padding:2px 6px;border-radius:5px;font-weight:bold;color:white">{diag}</span><br>
        <b>GET:</b> {get:.0f} kcal/día<hr>
        <b>Metas Diarias (g):</b><br>
        🍞 CHO: {(get*p_cho/400):.1f}g<br>
        🍗 PRO: {(get*p_pro/400):.1f}g<br>
        🥑 LIP: {(get*p_lip/900):.1f}g
    </div>
    """, unsafe_allow_html=True)

# --- ACCIÓN ---
if st.button("🚀 GENERAR PLAN NUTRICIONAL COMPLETO"):
    term = paises[pais]
    for i in range(7):
        for j in range(4):
            lista = desayunos if j in [0, 2] else comidas
            st.session_state[f"d{i}_m{j}"] = buscar_plato(lista, pats, kcal_por_momento[j])
    st.session_state.listo = True

# --- RENDERIZADO DEL PLAN ---
if st.session_state.get("listo"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    term = paises[pais]
    
    for i, d in enumerate(dias):
        with st.expander(f"📅 {d}", expanded=True):
            for j, lab in enumerate(["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]):
                # Verificamos que la clave exista antes de renderizar para evitar KeyError
                key = f"d{i}_m{j}"
                if key in st.session_state:
                    p = st.session_state[key]
                    c_txt, c_btn = st.columns([0.85, 0.15])
                    with c_txt:
                        nombre_final = p['nom'].format(**term)
                        st.markdown(f"**{lab}:** {nombre_final}")
                        st.caption(f"⚖️ Porción: x{p['factor']} | 🔥 {p['kcal']} kcal | 🍗 P: {p['p']}g | 🍞 C: {p['c']}g | 🥑 L: {p['l']}g")
                    with c_btn:
                        if st.button("🔄", key=f"swap_{i}_{j}"):
                            lista = desayunos if j in [0, 2] else comidas
                            st.session_state[key] = buscar_plato(lista, pats, kcal_por_momento[j])
                            st.rerun()
