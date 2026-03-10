import streamlit as st
from datetime import datetime
import random

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍏", layout="wide")

# CSS PARA LEGIBILIDAD EXTREMA
st.markdown("""
    <style>
    /* 1. Título Principal y Subtítulos (Cuerpo Central) */
    h1, h2, h3, [data-testid="stMarkdownContainer"] p { 
        color: #FFFFFF !important; 
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    /* 2. Columna Derecha: Métricas y Perfil Nutricional */
    [data-testid="stMetricLabel"] p { 
        color: #E0E0E0 !important; 
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] { 
        color: #FFFFFF !important; 
    }
    [data-testid="stCaption"] { 
        color: #B0B0B0 !important; 
        font-size: 0.9rem !important;
    }

    /* 3. Barra lateral (Mantenemos fondo blanco para orden) */
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { 
        color: #1e1e1e !important; 
    }

    /* 4. Tarjeta Blanca del Plan (Texto siempre oscuro aquí) */
    .plan-card h2, .plan-card p, .plan-card b { 
        color: #1e1e1e !important; 
    }
    .plan-card {
        padding: 30px; border-radius: 15px; background-color: #ffffff; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.5); border-left: 10px solid #2e7d32;
        margin-bottom: 20px;
    }

    /* 5. Botones */
    .stButton>button { background-color: #2e7d32; color: white !important; font-weight: bold; }
    .stDownloadButton>button { background-color: #1565c0; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
diccionario = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "frutilla": "Frutilla", "desayuno": "Mate con tostadas de pan integral y queso untable"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "frutilla": "Fresa", "desayuno": "Café de olla con molletes integrales"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "frutilla": "Fresa", "desayuno": "Tostada con aceite de oliva y tomate"}
}

recetas_oficina = ["Tarta de {zapallito} integral con semillas", "Ensalada de {porotos}, {choclo} y huevo", "Wrap integral de pollo y {palta}", "Wok de arroz con vegetales"]
recetas_hogar = ["Milanesas de pollo al horno con puré", "Guiso de lentejas con calabaza", "Pescado al horno con rodajas de {zapallito}", "Pastel de papa y carne magra"]

# --- INTERFAZ ---
st.title("🥗 Nutri-Flow: Gestión Profesional")

with st.sidebar:
    st.header("⚙️ Configuración")
    nombre = st.text_input("Nombre del Paciente", value="Emanuel")
    pais = st.selectbox("País de Residencia", list(diccionario.keys()))
    entorno = st.radio("Logística del Almuerzo", ["Oficina (Recalentable)", "Hogar (Cocina en el momento)"])
    
    mes = datetime.now().month
    es_invierno = (3 <= mes <= 8) if pais == "Argentina 🇦🇷" else (mes >= 9 or mes <= 2)
    temporada_txt = "Otoño/Invierno" if es_invierno else "Primavera/Verano"
    st.write(f"📅 **Temporada:** {temporada_txt}")

col_izq, col_der = st.columns([2, 1])

with col_izq:
    if st.button("🚀 GENERAR PLAN NUTRICIONAL"):
        term = diccionario[pais]
        plato = random.choice(recetas_oficina if "Oficina" in entorno else recetas_hogar).format(**term)
        desayuno = term["desayuno"]
        
        st.markdown(f"""
        <div class="plan-card">
            <h2 style='margin-top:0;'>📋 Plan de Alimentación</h2>
            <p><b>Paciente:</b> {nombre}</p>
            <p><b>Región:</b> {pais} | <b>Temporada:</b> {temporada_txt}</p>
            <hr>
            <p><b>🌅 Desayuno / Meriendas:</b><br>{desayuno}</p>
            <p><b>🍱 Almuerzo Sugerido:</b><br>{plato}</p>
        </div>
        """, unsafe_allow_html=True)
        
        texto_export = f"PACIENTE: {nombre}\nPAÍS: {pais}\nDESAYUNO: {desayuno}\nALMUERZO: {plato}"
        st.download_button(label="📥 DESCARGAR PLAN (.TXT)", data=texto_export, file_name=f"Plan_{nombre}.txt")

with col_der:
    st.markdown("### 📊 Perfil Nutricional")
    st.metric("Energía", "1950 kcal")
    st.metric("Proteínas", "110g")
    st.progress(0.6)
    st.caption("Balance: Carbs 50% | Prot 25% | Grasa 25%")
