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
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS (RECIETAS + MACROS) ---
desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db", "ls"], "receta": "200g yogur descremado + 3 cdas granola.", "pro": 8, "cho": 30},
    {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "veg", "ls"], "receta": "1 tostada integral + 1/2 palta + 1 huevo revuelto.", "pro": 12, "cho": 20},
    {"nombre": "Panqueque de avena y banana", "tags": ["db", "veg", "ls"], "receta": "1 huevo + 3 cdas avena + 1/2 banana a la sartén.", "pro": 10, "cho": 25},
    {"nombre": "Bowl de frutas y nueces", "tags": ["gf", "vgn", "db", "ls"], "receta": "Frutas de estación picadas + 3 nueces mariposa.", "pro": 4, "cho": 22}
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

# --- SIDEBAR: FICHA COMPLETA ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    nombre = st.text_input("Nombre", "Emanuel")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    edad = st.number_input("Edad", 18, 100, 30)
    peso = st.number_input("Peso (kg)", 75.0)
    talla = st.number_input("Talla (cm)", 175)
    
    # REINCORPORADO: Nivel de Actividad Física (NAF) detallado
    actividad_desc = st.selectbox("Nivel de Actividad Física", [
        "Sedentario (Poco o nada)", 
        "Leve (1-3 días/sem)", 
        "Moderado (3-5 días/sem)", 
        "Fuerte (6-7 días/sem)", 
        "Muy Fuerte (Atleta)"
    ])
    naf_map = {"Sedentario (Poco o nada)": 1.2, "Leve (1-3 días/sem)": 1.375, "Moderado (3-5 días/sem)": 1.55, "Fuerte (6-7 días/sem)": 1.725, "Muy Fuerte (Atleta)": 1.9}
    naf = naf_map[actividad_desc]

    st.divider()
    pats = st.multiselect("Patologías:", ["Celíaco", "Hipertenso", "Diabético", "Vegetariano", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- CÁLCULO METABÓLICO ---
tmb = (10 * peso) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * naf
imc = peso / ((talla/100)**2)

# --- LÓGICA DE FILTRADO ---
def obtener_menu(lista, filtros, term):
    res = lista.copy()
    if "Celíaco" in filtros: res = [r for r in res if "gf" in r["tags"]]
    if "Hipertenso" in filtros: res = [r for r in res if "ls" in r["tags"]]
    if "Diabético" in filtros: res = [r for r in res if "db" in r["tags"]]
    if "Vegano" in filtros: res = [r for r in res if "vgn" in r["tags"]]
    if "Dislipemia" in filtros: res = [r for r in res if "dl" in r["tags"]]
    
    plato = random.choice(res if res else lista)
    return {
        "nom": plato["nombre"].format(**term),
        "rec": plato["receta"].format(**term),
        "p": plato.get("pro", 0),
        "c": plato.get("cho", 0)
    }

# --- PANTALLA PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro")

col_m, col_p = st.columns([1, 2])

with col_m:
    st.markdown(f"""
    <div style="background:#f0f2f6; padding:15px; border-radius:10px; color:#333;">
        <h4>📊 Informe Metabólico</h4>
        <b>IMC:</b> {imc:.1f}<br>
        <b>GET:</b> {get:.0f} kcal/día<br>
        <hr>
        <b>Estrategia:</b> {actividad_desc}
    </div>
    """, unsafe_allow_html=True)

with col_p:
    if st.button("🚀 GENERAR / REFRESCAR PLAN SEMANAL"):
        st.session_state.listo = True
        term = paises[pais]
        for i in range(7):
            st.session_state[f"d_{i}"] = [obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term), 
                                          obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term)]

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
                    st.markdown(f"""
                    <div class="meal-box">
                        <b>{lab}:</b> {item['nom']} <span class="macro-tag">P: {item['p']}g | C: {item['c']}g</span>
                        <span class="receta-text">📖 {item['rec']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.write(" ") # Espaciador
                if st.button("🔄", key=f"re_{i}"):
                    st.session_state[f"d_{i}"] = [obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term), 
                                                  obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term)]
                    st.rerun()import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro | Consultorio", page_icon="🍎", layout="wide")

# --- CSS PROFESIONAL ---
st.markdown("""
    <style>
    h1, h2, h3 { color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #1e1e1e !important; font-weight: bold; }
    .day-card { 
        background-color: #ffffff; padding: 20px; border-radius: 12px; 
        border-left: 10px solid #2e7d32; margin-bottom: 20px; color: #1e1e1e !important;
    }
    .meal-box { margin-bottom: 10px; padding: 5px; border-bottom: 1px solid #eee; }
    .receta-text { font-size: 0.85em; color: #555; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS EXTENDIDA ---
desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db", "ls"], "receta": "Mezclar 200g de yogur descremado con 3 cdas de granola."},
    {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "veg", "ls"], "receta": "1 tostada integral con media palta pisada y 1 huevo revuelto."},
    {"nombre": "Panqueque de avena y banana", "tags": ["db", "veg", "ls"], "receta": "Mezclar 1 huevo, 3 cdas de avena y media banana. A la sartén."},
    {"nombre": "Bowl de frutas de estación y nueces", "tags": ["gf", "vgn", "db", "ls"], "receta": "Corta frutas variadas y agrega 3 mariposas de nuez."}
]

comidas = [
    {"nombre": "Pollo al horno con calabaza", "tags": ["gf", "db", "ls", "dl"], "receta": "150g de pechuga con 200g de calabaza asada con romero.", "pro": 30, "cho": 25},
    {"nombre": "Wok de vegetales y arroz integral", "tags": ["vgn", "db", "ls"], "receta": "Saltear brócoli, zanahoria y zuchini con 1 taza de arroz cocido.", "pro": 8, "cho": 45},
    {"nombre": "Pescado con {zapallito} grillado", "tags": ["gf", "db", "ls", "dl"], "receta": "Filete a la plancha con 2 {zapallito} en rodajas.", "pro": 28, "cho": 10},
    {"nombre": "Ensalada de quinoa y {choclo}", "tags": ["gf", "vgn", "ls", "db"], "receta": "1 taza de quinoa, medio {choclo} desgranado, tomate y albahaca.", "pro": 10, "cho": 50},
    {"nombre": "Tarta de {zapallito} integral", "tags": ["veg", "db", "ls"], "receta": "Masa integral, relleno de {zapallito}, cebolla y ligue de claras.", "pro": 12, "cho": 35}
]

paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "d": "Mate con tostadas"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "d": "Café con molletes"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "d": "Tostada con tomate y aceite de oliva"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    nombre = st.text_input("Nombre", "Emanuel")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    peso = st.number_input("Peso (kg)", 75.0)
    talla = st.number_input("Talla (cm)", 175)
    actividad = st.select_slider("Actividad Física", options=[1.2, 1.375, 1.55, 1.725])
    
    st.divider()
    pats = st.multiselect("Patologías:", ["Celíaco", "Hipertenso", "Diabético", "Vegetariano", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

# --- LÓGICA DE CÁLCULO ---
tmb = (10 * peso) + (6.25 * talla) - (5 * 30) + (5 if sexo == "Masculino" else -161)
get = tmb * actividad
imc = peso / ((talla/100)**2)

# --- FUNCION DE FILTRADO ---
def obtener_menu(lista, filtros, term):
    res = lista.copy()
    if "Celíaco" in filtros: res = [r for r in res if "gf" in r["tags"]]
    if "Hipertenso" in filtros: res = [r for r in res if "ls" in r["tags"]]
    if "Diabético" in filtros: res = [r for r in res if "db" in r["tags"]]
    if "Vegano" in filtros: res = [r for r in res if "vgn" in r["tags"]]
    
    plato = random.choice(res if res else lista)
    nombre_f = plato["nombre"].format(**term)
    return nombre_f, plato.get("receta", ""), plato.get("pro", 0), plato.get("cho", 0)

# --- CUERPO PRINCIPAL ---
st.title("🍎 Nutri-Flow Pro")

if st.button("🚀 GENERAR PLAN SEMANAL COMPLETO"):
    st.session_state.generado = True
    term = paises[pais]
    for i in range(7):
        st.session_state[f"dia_{i}"] = [obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term), 
                                        obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term)]

if "generado" in st.session_state:
    dias_n = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    term = paises[pais]
    
    for i, d_nombre in enumerate(dias_n):
        with st.container():
            col_t, col_b = st.columns([5, 1])
            with col_t:
                st.markdown(f'<div class="day-card"><div class="day-title">📅 {d_nombre}</div>', unsafe_allow_html=True)
                comidas_labels = ["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]
                for idx, label in enumerate(comidas_labels):
                    m_nom, m_rec, m_p, m_c = st.session_state[f"dia_{i}"][idx]
                    st.markdown(f"**{label}:** {m_nom}<br><span class='receta-text'>Prep: {m_rec}</span>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_b:
                if st.button("🔄", key=f"btn_{i}"):
                    st.session_state[f"dia_{i}"] = [obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term), 
                                                    obtener_menu(desayunos, pats, term), obtener_menu(comidas, pats, term)]
                    st.rerun()
