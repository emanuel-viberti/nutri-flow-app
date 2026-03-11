import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- CSS PROFESIONAL ---
st.markdown("""
    <style>
    h1, h2, h3 { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label { color: #1e1e1e !important; font-weight: bold; }
    .day-card { 
        background-color: #ffffff; padding: 15px; border-radius: 12px; 
        border-left: 8px solid #2e7d32; margin-bottom: 18px; color: #1e1e1e !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .macro-tag { font-size: 0.75em; background: #e8f5e9; color: #2e7d32; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    .metric-box { background: #f0f2f6; padding: 15px; border-radius: 10px; color: #333; border: 1px solid #ccc; margin-bottom: 10px;}
    .pi-box { background: #fff3e0; border: 1px solid #ff9800; padding: 8px; border-radius: 8px; color: #e65100; margin-top: 5px;}
    .receta-text { font-size: 0.85em; color: #666; font-style: italic; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS EXTENDIDA ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera"}
}

desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db", "ls"], "rec": "200g yogur descremado + 3 cdas granola.", "p": 8, "c": 30},
    {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "veg", "ls"], "rec": "1 tostada integral + 1/2 {palta} + 1 huevo.", "p": 12, "c": 20},
    {"nombre": "Panqueque de avena y banana", "tags": ["db", "veg", "ls"], "rec": "1 huevo + 3 cdas avena + 1/2 banana.", "p": 10, "c": 25},
    {"nombre": "Bowl de frutas y nueces", "tags": ["gf", "vgn", "db", "ls"], "rec": "{frutilla} picada + 3 nueces mariposa.", "p": 4, "c": 22},
    {"nombre": "Omelette de claras y espinaca", "tags": ["gf", "db", "ls", "dl"], "rec": "3 claras + 1 puñado de espinaca.", "p": 15, "c": 2},
    {"nombre": "Pudin de chía y leche de coco", "tags": ["gf", "vgn", "db"], "rec": "2 cdas chía en 1/2 taza leche de coco.", "p": 5, "c": 12},
    {"nombre": "Tostón de pan de centeno con queso", "tags": ["db", "ls"], "rec": "1 feta de pan centeno + queso untable descremado.", "p": 7, "c": 18}
]

comidas = [
    {"nombre": "Pollo al horno con calabaza", "tags": ["gf", "db", "ls", "dl"], "rec": "150g pechuga + 200g calabaza asada.", "p": 30, "c": 25},
    {"nombre": "Wok de vegetales y arroz integral", "tags": ["vgn", "db", "ls"], "rec": "Vegetales salteados + 1 taza arroz cocido.", "p": 8, "c": 45},
    {"nombre": "Pescado con {zapallito} grillado", "tags": ["gf", "db", "ls", "dl"], "rec": "Filete blanco + 2 {zapallito} en rodajas.", "p": 28, "c": 10},
    {"nombre": "Ensalada de quinoa y {choclo}", "tags": ["gf", "vgn", "ls", "db"], "rec": "1 taza quinoa + 1/2 {choclo} + tomate.", "p": 10, "c": 50},
    {"nombre": "Lentejas con vegetales", "tags": ["vgn", "gf", "db", "ls"], "rec": "1 taza lentejas cocidas + morrón y cebolla.", "p": 14, "c": 40},
    {"nombre": "{carne} a la plancha con puré", "tags": ["gf", "ls", "dl"], "rec": "150g {carne} magra + 150g puré mixto.", "p": 32, "c": 22},
    {"nombre": "Tarta de {zapallito} (sin masa)", "tags": ["gf", "veg", "db", "ls"], "rec": "3 {zapallito} + 2 huevos + queso magro.", "p": 18, "c": 12},
    {"nombre": "Wrap de pollo y hojas verdes", "tags": ["db", "ls"], "rec": "Tortilla integral + 100g pollo + lechuga.", "p": 22, "c": 28},
    {"nombre": "Garbanzos con espinaca y pimentón", "tags": ["vgn", "gf", "db"], "rec": "1 taza garbanzos + espinaca salteada.", "p": 12, "c": 38},
    {"nombre": "Risotto de hongos y cebada", "tags": ["veg", "db", "ls"], "rec": "1 taza cebada perlada + mix de hongos.", "p": 9, "c": 42}
]

# --- FUNCIONES ---
def seleccionar_plato(lista, filtros, term):
    res = [r for r in lista]
    if "Celíaco" in filtros: res = [r for r in res if "gf" in r["tags"]]
    if "Hipertenso" in filtros: res = [r for r in res if "ls" in r["tags"]]
    if "Diabético" in filtros: res = [r for r in res if "db" in r["tags"]]
    if "Vegano" in filtros: res = [r for r in res if "vgn" in r["tags"]]
    if "Dislipemia" in filtros: res = [r for r in res if "dl" in r["tags"]]
    
    # Si los filtros son muy estrictos y vacían la lista, volvemos a la lista original para no romper la app
    final_pool = res if len(res) > 0 else lista
    plato = random.choice(final_pool)
    
    return {
        "nom": plato["nombre"].format(**term), 
        "rec": plato["rec"].format(**term), 
        "p": plato["p"], 
        "c": plato["c"]
    }

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 50, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 10.0, 300.0, 75.0)
    edad = st.number_input("Edad", 1, 110, 30)
    
    pi = (talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9
    st.markdown(f'<div class="pi-box">⚖️ <b>Sugerencia PI:</b> {pi:.1f} kg</div>', unsafe_allow_html=True)
    peso_obj = st.number_input("Peso para Cálculo (kg)", 10.0, 300.0, float(pi))

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
tmb = (10 * peso_obj) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * naf
imc_act = peso_act / ((talla/100)**2)

# --- UI PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro")
col_info, col_plan = st.columns([1, 2.2])

with col_info:
    st.markdown(f"""
    <div class="metric-box">
        <h4>📊 Informe de Consultorio</h4>
        <b>IMC:</b> {imc_act:.1f}<br>
        <b>GET:</b> {get:.0f} kcal<br>
        <hr>
        <b>Objetivo Diario:</b><br>
        🍞 {(get * p_carb / 400):.1f}g CHO<br>
        🍗 {(get * p_prot / 400):.1f}g PRO<br>
        🥑 {(get * p_gras / 900):.1f}g LIP
    </div>
    """, unsafe_allow_html=True)

with col_plan:
    if (p_carb + p_prot + p_gras) == 100:
        if st.button("🚀 GENERAR / RESETEAR PLAN SEMANAL"):
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
    coms = ["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]
    for i, d_n in enumerate(dias):
        with st.container():
            st.markdown(f'<div class="day-card"><b>📅 {d_n}</b>', unsafe_allow_html=True)
            for j, lab in enumerate(coms):
                key = f"d{i}_m{j}"
                if key in st.session_state:
                    p = st.session_state[key]
                    c1, c2 = st.columns([0.88, 0.12])
                    with c1:
                        st.markdown(f"<b>{lab}:</b> {p['nom']} <span class='macro-tag'>P:{p['p']}g C:{p['c']}g</span><br><span class='receta-text'>📖 {p['rec']}</span>", unsafe_allow_html=True)
                    with c2:
                        if st.button("🔄", key=f"btn_{key}"):
                            pool = desayunos if j in [0,2] else comidas
                            st.session_state[key] = seleccionar_plato(pool, pats, paises[pais_sel])
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
