import streamlit as st
from datetime import datetime
import random

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍏", layout="wide")

# CSS CORRECTIVO TOTAL (Para legibilidad absoluta)
st.markdown("""
    <style>
    /* 1. Fondo principal y texto general (Cuerpo) */
    .main { background-color: #f4f7f6; color: #1e1e1e; font-family: 'Helvetica', sans-serif; }
    h1, h2, h3, p { color: #1e1e1e !important; }

    /* 2. Barra lateral - Fondo blanco y texto negro FORZADO */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Forzamos negro para labels, selectbox, radio buttons y texto */
    [data-testid="stSidebar"] label { 
        color: #1e1e1e !important; 
        font-weight: bold; 
    }
    [data-testid="stSidebar"] .stMarkdown p { 
        color: #1e1e1e !important; 
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] > div, 
    [data-testid="stSidebar"] input {
        color: #1e1e1e !important; 
        background-color: #ffffff !important;
        border-color: #cccccc !important;
    }

    /* 3. Tarjeta del Plan y Métricas */
    .plan-card, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { 
        color: #1e1e1e !important;
    }
    .plan-card {
        padding: 30px; border-radius: 15px; background-color: #ffffff; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-left: 10px solid #2e7d32;
        margin-bottom: 20px;
    }

    /* 4. Botones */
    .stButton>button { 
        border-radius: 10px; background-color: #2e7d32; color: white !important; 
        font-weight: bold; border: none; padding: 10px;
    }
    .stDownloadButton>button { 
        border-radius: 10px; background-color: #1565c0; color: white !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS (No cambia) ---
diccionario = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "frutilla": "Frutilla", "desayuno": "Mate con tostadas de pan integral y queso untable"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "frutilla": "Fresa", "desayuno": "Café de olla con molletes integrales y frijoles refritos"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "frutilla": "Fresa", "desayuno": "Tostada con aceite de oliva virgen y tomate triturado"}
}

recetas_oficina = ["Tarta de {zapallito} integral con semillas", "Ensalada de {porotos}, {choclo} y huevo", "Wrap integral de pollo y {palta}", "Wok de arroz con vegetales de estación"]
recetas_hogar = ["Milanesas de pollo al horno con puré", "Guiso de lentejas con calabaza", "Pescado al horno con rodajas de {zapallito}", "Pastel de papa y carne magra"]

# --- INTERFAZ ---
st.title("🥗 Nutri-Flow: Gestión Profesional")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424434.png", width=80)
    st.header("⚙️ Configuración")
    nombre = st.text_input("Nombre del Paciente", value="Emanuel")
    pais = st.selectbox("País de Residencia", list(diccionario.keys()))
    entorno = st.radio("Logística del Almuerzo", ["Oficina (Recalentable)", "Hogar (Cocina en el momento)"])
    
    # Lógica de Temporada Corregida
    mes = datetime.now().month
    es_invierno = (3 <= mes <= 8) if pais == "Argentina 🇦🇷" else (mes >= 9 or mes <= 2)
    temporada_txt = "Otoño/Invierno" if es_invierno else "Primavera/Verano"
    st.write(f"📅 **Temporada:** {temporada_txt}")
    st.divider()

col_izq, col_der = st.columns([2, 1])

with col_izq:
    if st.button("🚀 GENERAR PLAN NUTRICIONAL"):
        term = diccionario[pais]
        plato = random.choice(recetas_oficina if "Oficina" in entorno else recetas_hogar).format(**term)
        desayuno = term["desayuno"]
        
        st.markdown(f"""
        <div class="plan-card">
            <h2 style='color: #2e7d32;'>📋 Plan de Alimentación</h2>
            <p><b>Paciente:</b> {nombre}</p>
            <p><b>Región:</b> {pais} | <b>Temporada:</b> {temporada_txt}</p>
            <hr>
            <p style='font-size: 1.2em;'><b>🌅 Desayuno / Meriendas:</b><br>{desayuno}</p>
            <p style='font-size: 1.2em;'><b>🍱 Almuerzo Sugerido:</b><br>{plato}</p>
            <p style='color: #666; font-size: 0.9em;'><i>Nota: Porciones ajustadas individualmente.</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        texto_export = f"""
        PACIENTE: {nombre}
        PAÍS: {pais}
        TEMPORADA: {temporada_txt}
        
        DESAYUNO/MERIENDA: {desayuno}
        ALMUERZO ({entorno}): {plato}
        
        Generado por Nutri-Flow Pro - {datetime.now().strftime('%d/%m/%Y')}
        """
        st.download_button(label="📥 DESCARGAR PLAN (.TXT)", data=texto_export, file_name=f"Plan_{nombre}.txt")

with col_der:
    st.markdown("### 📊 Perfil Nutricional")
    st.metric("Energía", "1950 kcal")
    st.metric("Proteínas", "110g", help="1.5g/kg peso prom.")
    st.progress(0.6)
    st.caption("Balance: Carbs 50% | Prot 25% | Grasa 25%")
