import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- TRADUCCIONES Y BASE DE DATOS ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# (Las listas 'desayunos' y 'comidas' se mantienen iguales a la versión anterior para asegurar los 100 platos reales)
# [INSERTAR AQUÍ LAS LISTAS DE DESAYUNOS Y COMIDAS PROPORCIONADAS ANTERIORMENTE]
# Por brevedad en la respuesta, asumo que ya tenés las listas cargadas arriba.

# --- LÓGICA DE SELECCIÓN ---
def obtener_plato(lista, filtros, term):
    res = [r for r in lista]
    if "Celíaco" in filtros: res = [r for r in res if "gf" in r["tags"]]
    if "Hipertenso" in filtros: res = [r for r in res if "ls" in r["tags"]]
    if "Diabético" in filtros: res = [r for r in res if "db" in r["tags"]]
    if "Vegano" in filtros: res = [r for r in res if "vgn" in r["tags"]]
    if "Dislipemia" in filtros: res = [r for r in res if "dl" in r["tags"]]
    
    final_pool = res if len(res) > 0 else lista
    plato = random.choice(final_pool)
    return {"nom": plato["nombre"].format(**term), "rec": plato["rec"].format(**term), "p": plato["p"], "c": plato["c"]}

def diagnosticar_imc(imc):
    if imc < 18.5: return "Bajo Peso ⚠️", "#ffeb3b"
    if 18.5 <= imc < 25: return "Normopeso ✅", "#4caf50"
    if 25 <= imc < 30: return "Sobrepeso 🟠", "#ff9800"
    return "Obesidad 🔴", "#f44336"

# --- INTERFAZ SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 50, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 10.0, 200.0, 75.0)
    edad = st.number_input("Edad", 1, 110, 30)
    
    pi = (talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9
    st.info(f"⚖️ Peso Ideal Sugerido: {pi:.1f} kg")
    peso_obj = st.number_input("Peso para Cálculo (kg)", 10.0, 200.0, float(pi))
    
    naf = st.selectbox("Actividad", [1.2, 1.375, 1.55, 1.725, 1.9], format_func=lambda x: {1.2:"Sedentario", 1.375:"Leve", 1.55:"Moderado", 1.725:"Fuerte", 1.9:"Muy Fuerte"}[x])
    pats = st.multiselect("Patologías", ["Celíaco", "Hipertenso", "Diabético", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS ---
tmb = (10 * peso_obj) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * naf
imc = peso_act / ((talla/100)**2)
diag, color_diag = diagnosticar_imc(imc)

# --- UI PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro")
col_info, col_plan = st.columns([1, 2.5])

with col_info:
    st.markdown(f"""
    <div style="background:#f0f2f6;padding:15px;border-radius:10px;border:1px solid #ccc;color:#333">
        <h4>📊 Informe Técnico</h4>
        <b>IMC:</b> {imc:.1f} <br>
        <span style="background:{color_diag};padding:2px 6px;border-radius:5px;font-weight:bold">{diag}</span><br>
        <b>GET:</b> {get:.0f} kcal/día<hr>
        <b>Macros Diarios:</b><br>
        🍞 {(get*0.5/4):.1f}g CHO (50%)<br>
        🍗 {(get*0.2/4):.1f}g PRO (20%)<br>
        🥑 {(get*0.3/9):.1f}g LIP (30%)
    </div>
    """, unsafe_allow_html=True)

# --- GENERACIÓN DEL PLAN ---
if st.button("🚀 GENERAR PLAN SEMANAL"):
    term = paises[pais]
    for i in range(7):
        for j in range(4): # 0:Des, 1:Alm, 2:Mer, 3:Cen
            lista = desayunos if j in [0, 2] else comidas
            st.session_state[f"d{i}_m{j}"] = obtener_plato(lista, pats, term)
    st.session_state.listo = True

# --- MOSTRAR PLAN E INTERCAMBIOS ---
if st.session_state.get("listo"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    term = paises[pais]
    
    for i, d in enumerate(dias):
        with st.expander(f"📅 {d}", expanded=True):
            for j, lab in enumerate(["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]):
                col_txt, col_btn = st.columns([0.85, 0.15])
                p = st.session_state[f"d{i}_m{j}"]
                
                with col_txt:
                    st.markdown(f"**{lab}:** {p['nom']} <small>(P:{p['p']}g C:{p['c']}g)</small>  \n*{p['rec']}*", unsafe_allow_html=True)
                
                with col_btn:
                    if st.button("🔄", key=f"btn_{i}_{j}"):
                        lista = desayunos if j in [0, 2] else comidas
                        st.session_state[f"d{i}_m{j}"] = obtener_plato(lista, pats, term)
                        st.rerun()
