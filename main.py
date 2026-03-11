import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- DATA BASE ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# (Mantené tus listas de 100 platos aquí)
desayunos = [{"nombre": "Yogur con granola y {frutilla}", "kcal": 250, "p": 12, "c": 35, "l": 6, "tags":[]}]
comidas = [{"nombre": "Pechuga con calabaza", "kcal": 450, "p": 35, "c": 30, "l": 10, "tags":[]}]

# --- LÓGICA DE CÁLCULO ---
def redondear_porcion(valor):
    return round(valor * 4) / 4

def buscar_y_ajustar(lista, kcal_obj, term):
    plato = random.choice(lista)
    factor = redondear_porcion(kcal_obj / plato["kcal"])
    if factor == 0: factor = 0.25
    return {
        "nom": plato["nombre"].format(**term),
        "kcal": round(plato["kcal"] * factor),
        "p": round(plato["p"] * factor, 1),
        "c": round(plato["c"] * factor, 1),
        "l": round(plato["l"] * factor, 1),
        "factor": factor
    }

# --- SIDEBAR DINÁMICO ---
with st.sidebar:
    st.header("👤 Ficha del Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 100, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0)
    edad = st.number_input("Edad", 1, 110, 30)
    
    # --- LA CORRECCIÓN CLAVE AQUÍ ---
    # Calculamos el PI sugerido dinámicamente según la talla ingresada arriba
    pi_sugerido = float((talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9)
    
    # El value ahora es pi_sugerido, por lo que cambiará al mover la talla
    pi_real = st.number_input("Peso Objetivo / Ideal (kg)", 30.0, 200.0, value=pi_sugerido)
    
    opciones_af = {"Sedentario": 1.2, "Leve": 1.375, "Moderado": 1.55, "Fuerte": 1.725, "Muy Fuerte": 1.9}
    af_label = st.selectbox("Actividad Física", list(opciones_af.keys()))
    af_valor = opciones_af[af_label]
    
    st.divider()
    st.header("⚖️ Prescripción de Macros")
    p_cho = st.number_input("% CHO", 0, 100, 50)
    p_pro = st.number_input("% PRO", 0, 100, 20)
    p_lip = st.number_input("% LIP", 0, 100, 30)
    
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS TÉCNICOS ---
# TMB usando el Peso Objetivo (pi_real)
tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * af_valor

# Metas en gramos
g_pro = (get * p_pro / 400)
g_cho = (get * p_cho / 400)
g_lip = (get * p_lip / 900)

# --- UI PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro")
c_info, c_plan = st.columns([1, 2.5])

with c_info:
    imc = peso_act / ((talla/100)**2)
    st.markdown(f"""
    <div style="background:#f0f2f6;padding:15px;border-radius:10px;color:black;border:1px solid #ccc">
        <h4>📊 Informe Técnico</h4>
        <b>GET:</b> {get:.0f} kcal<br>
        <b>IMC Actual:</b> {imc:.1f}<hr>
        <b>Metas Diarias:</b><br>
        🍗 PRO: {g_pro:.1f}g<br>
        🍞 CHO: {g_cho:.1f}g<br>
        🥑 LIP: {g_lip:.1f}g
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 GENERAR PLAN"):
    term = paises[pais]
    # Distribución 20-35-15-30
    dist = [get*0.20, get*0.35, get*0.15, get*0.30]
    for i in range(7):
        for j in range(4):
            lista = desayunos if j in [0, 2] else comidas
            st.session_state[f"d{i}_{j}"] = buscar_y_ajustar(lista, dist[j], term)
    st.session_state.listo = True

if st.session_state.get("listo"):
    for i, d in enumerate(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]):
        with st.expander(f"📅 {d}", expanded=True):
            tk, tp, tc, tl = 0, 0, 0, 0
            for j, lab in enumerate(["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]):
                p = st.session_state[f"d{i}_{j}"]
                st.write(f"**{lab}:** {p['nom']} (x{p['factor']})")
                st.caption(f"🔥 {p['kcal']} kcal | P: {p['p']}g | C: {p['c']}g | G: {p['l']}g")
                tk+=p['kcal']; tp+=p['p']; tc+=p['c']; tl+=p['l']
            
            # Validación rápida al pie de cada día
            st.markdown(f"<p style='font-size:0.8em; color:gray'>Suma diaria: {tk} kcal | P: {tp:.1f}g | C: {tc:.1f}g | G: {tl:.1f}g</p>", unsafe_allow_html=True)
