import streamlit as st
from datetime import datetime
import random

# CONFIGURACIÓN ESTÉTICA MEJORADA
st.set_page_config(page_title="Nutri-Flow Pro | Dashboard", page_icon="🍏", layout="wide")

# CSS CORREGIDO PARA VISIBILIDAD TOTAL
st.markdown("""
    <style>
    /* Fondo general */
    .main { background-color: #f0f2f6; }
    
    /* Forzar color de texto en inputs para evitar blanco sobre blanco */
    input { color: #1f1f1f !important; }
    div[data-baseweb="select"] > div { color: #1f1f1f !important; }
    
    /* Botones con mejor contraste */
    .stButton>button { 
        width: 100%; border-radius: 12px; 
        background-color: #2e7d32; color: white !important; 
        height: 3.5em; font-weight: bold; border: none;
    }
    .stDownloadButton>button { 
        width: 100%; border-radius: 12px; 
        background-color: #1565c0; color: white !important; 
        border: none;
    }
    
    /* Tarjeta de resultado */
    .plan-card { 
        padding: 25px; border-radius: 15px; 
        background-color: #ffffff; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        border-left: 8px solid #2e7d32;
        color: #1f1f1f;
    }
    h1, h2, h3, p { color: #1f1f1f !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
diccionario = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "frutilla": "Frutilla", "desayuno": "Mate con tostadas de pan integral y queso untable"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "frutilla": "Fresa", "desayuno": "Café de olla con molletes integrales y frijol"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "frutilla": "Fresa", "desayuno": "Tostada con aceite de oliva virgen y tomate triturado"}
}

recetas_oficina = ["Tarta de {zapallito} integral con semillas", "Ensalada de {porotos}, {choclo} y huevo", "Wrap integral de pollo y {palta}", "Wok de arroz con vegetales de estación"]
recetas_hogar = ["Milanesas de pollo al horno con puré", "Guiso de lentejas con cubos de calabaza", "Pescado al horno con rodajas de {zapallito}", "Pastel de papa y carne magra"]

# --- INTERFAZ ---
st.title("🥗 Nutri-Flow: Gestión Profesional")

with st.sidebar:
    st.header("⚙️ Panel de Control")
    nombre = st.text_input("Nombre del Paciente", value="Emanuel")
    pais = st.selectbox("Mercado / País", list(diccionario.keys()))
    entorno = st.radio("Logística del Almuerzo", ["Oficina (Recalentable)", "Hogar (Cocina en el momento)"])
    
    mes = datetime.now().month
    es_invierno = (3 <= mes <= 8) if pais == "Argentina 🇦🇷" else (mes >= 9 or mes <= 2)
    temporada_txt = "Otoño/Invierno" if es_invierno else "Primavera/Verano"
    st.info(f"📅 **Temporada:** {temporada_txt}")

col_izq, col_der = st.columns([2, 1])

with col_izq:
    if st.button("🚀 GENERAR PLAN NUTRICIONAL"):
        term = diccionario[pais]
        plato = random.choice(recetas_oficina if "Oficina" in entorno else recetas_hogar).format(**term)
        desayuno = term["desayuno"]
        
        st.markdown(f"""
        <div class="plan-card">
            <h3>📋 Plan Sugerido para {nombre}</h3>
            <p><b>📍 Región:</b> {pais} | <b>🌡️ Clima:</b> {temporada_txt}</p>
            <hr>
            <p><b>🌅 Desayuno/Merienda:</b> {desayuno}</p>
            <p><b>🍱 Almuerzo ({entorno}):</b> {plato}</p>
        </div>
        """, unsafe_allow_html=True)
        
        texto_export = f"PLAN NUTRICIONAL: {nombre}\nPaís: {pais}\n\nDesayuno: {desayuno}\nAlmuerzo: {plato}"
        st.download_button(label="📥 DESCARGAR PLAN (.TXT)", data=texto_export, file_name=f"Plan_{nombre}.txt")

with col_der:
    st.markdown("### 📊 Análisis de Macros")
    st.metric("Calorías", "1900 kcal")
    st.metric("Proteínas", "115g")
    st.progress(0.7)
