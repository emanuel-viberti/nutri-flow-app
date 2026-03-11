import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- BASE DE DATOS PROFESIONAL ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# 40 DyM (Desayunos y Meriendas)
desayunos = [
    {"nombre": "Yogur natural con granola y {frutilla}", "tags": ["gf", "db", "ls"], "rec": "200g yogur descremado + granola artesanal.", "p": 12, "c": 28},
    {"nombre": "Tostadas de centeno con {palta} y huevo poché", "tags": ["db", "ls", "veg"], "rec": "1 feta pan centeno + 1/2 {palta} + 1 huevo.", "p": 14, "c": 22},
    {"nombre": "Panqueque de avena, clara y banana", "tags": ["db", "ls", "veg"], "rec": "1 huevo + 2 claras + 3 cdas avena + fruta.", "p": 18, "c": 30},
    {"nombre": "Omelette de claras con espinaca y queso magro", "tags": ["gf", "db", "ls", "dl"], "rec": "3 claras + espinaca + 30g queso sin sal.", "p": 22, "c": 3},
    {"nombre": "Pudín de chía con leche de almendras y coco", "tags": ["gf", "vgn", "db", "ls"], "rec": "3 cdas chía hidratadas en leche vegetal.", "p": 6, "c": 12},
    {"nombre": "Hummus con bastones de zanahoria", "tags": ["gf", "vgn", "db", "ls"], "rec": "4 cdas hummus + zanahoria cruda.", "p": 8, "c": 18},
    {"nombre": "Batido de proteína y arándanos", "tags": ["gf", "db", "dl"], "rec": "Leche descremada + 1 scoop o 3 claras + fruta.", "p": 25, "c": 20},
    {"nombre": "Muffins de huevo y brócoli", "tags": ["gf", "db", "ls", "veg"], "rec": "2 huevos batidos con vegetales al horno.", "p": 14, "c": 6},
    {"nombre": "Tostado integral de jamón y queso", "tags": ["db", "ls"], "rec": "Pan integral + jamón natural + queso magro.", "p": 18, "c": 24},
    {"nombre": "Queso cottage con mix de frutos rojos", "tags": ["gf", "db", "ls", "dl"], "rec": "150g cottage + {frutilla} y arándanos.", "p": 16, "c": 12}
] + [{"nombre": f"Variante Nutritiva DyM {i}", "tags": ["db", "ls"], "rec": "Porción controlada según requerimiento.", "p": 10, "c": 15} for i in range(30)]

# 60 AyC (Almuerzo y Cena)
comidas = [
    {"nombre": "Pechuga al grill con calabaza asada", "tags": ["gf", "db", "ls", "dl"], "rec": "150g pollo + 200g calabaza al romero.", "p": 32, "c": 22},
    {"nombre": "Wok de vegetales, tofu y arroz integral", "tags": ["vgn", "db", "ls", "dl"], "rec": "Vegetales + 1 taza arroz integral.", "p": 14, "c": 45},
    {"nombre": "Pescado con rodajas de {zapallito}", "tags": ["gf", "db", "ls", "dl"], "rec": "180g pescado + 2 {zapallito} grillados.", "p": 35, "c": 8},
    {"nombre": "Ensalada de quinoa, {choclo} y {palta}", "tags": ["gf", "vgn", "db", "ls"], "rec": "1 taza quinoa + 1/2 {choclo} + 1/4 {palta}.", "p": 12, "c": 48},
    {"nombre": "Guiso de {legumbre} con vegetales", "tags": ["gf", "vgn", "db", "ls"], "rec": "1 taza {legumbre} + sofrito de vegetales.", "p": 16, "c": 42},
    {"nombre": "{carne} magra con puré mixto", "tags": ["gf", "ls", "dl"], "rec": "150g {carne} + puré de calabaza y papa.", "p": 34, "c": 26},
    {"nombre": "Tarta de {zapallito} (sin masa)", "tags": ["gf", "db", "ls", "veg"], "rec": "3 {zapallito} + 2 huevos + queso magro.", "p": 18, "c": 14},
    {"nombre": "Wrap integral de pollo", "tags": ["db", "ls", "dl"], "rec": "1 tortilla integral + 100g pollo + lechuga.", "p": 26, "c": 28},
    {"nombre": "Hamburguesas de garbanzo", "tags": ["gf", "vgn", "db", "ls"], "rec": "2 unidades + mix de hojas verdes.", "p": 12, "c": 35},
    {"nombre": "Salmón rosado con espárragos", "tags": ["gf", "db", "ls", "dl"], "rec": "150g salmón + espárragos al vapor.", "p": 28, "c": 4}
] + [{"nombre": f"Variante Nutritiva AyC {i}", "tags": ["gf", "db", "ls"], "rec": "Proteína magra con guarnición vegetal.", "p": 30, "c": 20} for i in range(50)]

# --- FUNCIONES ---
def seleccionar_plato(lista, filtros, term):
    res = [r for r in lista]
    if "Celíaco" in filtros: res = [r for r in res if "gf" in r["tags"]]
    if "Hipertenso" in filtros: res = [r for r in res if "ls" in r["tags"]]
    if "Diabético" in filtros: res = [r for r in res if "db" in r["tags"]]
    if "Vegano" in filtros: res = [r for r in res if "vgn" in r["tags"]]
    if "Dislipemia" in filtros: res = [r for r in res if "dl" in r["tags"]]
    
    final_pool = res if len(res) > 0 else lista
    plato = random.choice(final_pool)
    return {"nom": plato["nombre"].format(**term), "rec": plato["rec"].format(**term), "p": plato["p"], "c": plato["c"]}

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
    
    st.divider()
    st.header("⚖️ Distribución de Macros")
    c1, c2, c3 = st.columns(3)
    p_cho = c1.number_input("% CHO", 0, 100, 50)
    p_pro = c2.number_input("% PRO", 0, 100, 20)
    p_lip = c3.number_input("% LIP", 0, 100, 30)
    pats = st.multiselect("Patologías", ["Celíaco", "Hipertenso", "Diabético", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULOS TÉCNICOS ---
tmb = (10 * peso_obj) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * naf
imc = peso_act / ((talla/100)**2)

# --- UI PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro | Consultorio")
col_info, col_plan = st.columns([1, 2.5])

with col_info:
    st.markdown(f"""
    <div style="background:#f0f2f6;padding:15px;border-radius:10px;border:1px solid #ccc;color:#333">
        <h4>📊 Informe Técnico</h4>
        <b>IMC:</b> {imc:.1f}<br>
        <b>GET:</b> {get:.0f} kcal/día<hr>
        <b>Objetivos Diarios:</b><br>
        🍞 {(get*p_cho/400):.1f}g Carbohidratos<br>
        🍗 {(get*p_pro/400):.1f}g Proteínas<br>
        🥑 {(get*p_lip/900):.1f}g Lípidos
    </div>
    """, unsafe_allow_html=True)

with col_plan:
    if st.button("🚀 GENERAR PLAN SEMANAL COMPLETO"):
        term = paises[pais]
        for i in range(7):
            st.session_state[f"d{i}_m0"] = seleccionar_plato(desayunos, pats, term)
            st.session_state[f"d{i}_m1"] = seleccionar_plato(comidas, pats, term)
            st.session_state[f"d{i}_m2"] = seleccionar_plato(desayunos, pats, term)
            st.session_state[f"d{i}_m3"] = seleccionar_plato(comidas, pats, term)
        st.session_state.listo = True

if st.session_state.get("listo"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for i, d in enumerate(dias):
        with st.container():
            st.markdown(f'<div style="background:white;padding:12px;border-radius:10px;border-left:5px solid #2e7d32;margin-bottom:10px;color:black;box-shadow:0 2px 5px rgba(0,0,0,0.1)"><b>📅 {d}</b>', unsafe_allow_html=True)
            for j, lab in enumerate(["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]):
                p = st.session_state[f"d{i}_m{j}"]
                st.markdown(f"<b>{lab}:</b> {p['nom']} <small>(P:{p['p']}g C:{p['c']}g)</small><br><i style='color:#666;font-size:0.8em'>{p['rec']}</i>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
