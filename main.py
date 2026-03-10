import streamlit as st
from datetime import datetime
import random

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍏", layout="wide")

# CSS PARA CORREGIR VISIBILIDAD Y COLORES
st.markdown("""
    <style>
    /* Fondo y texto general */
    .main { background-color: #f4f7f6; color: #1e1e1e; }
    
    /* Barra lateral - Forzamos colores legibles */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
        color: #1e1e1e !important;
    }
    
    /* Tarjeta del Plan */
    .plan-card { 
        padding: 30px; border-radius: 15px; 
        background-color: #ffffff; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); 
        border-left: 10px solid #2e7d32;
        color: #1e1e1e;
        margin-bottom: 20px;
    }
    
    /* Botones */
    .stButton>button { 
        border-radius: 10px; background-color: #2e7d32; color: white !important; 
        font-weight: bold; border: none; padding: 10px;
    }
    .stDownloadButton>button { 
        border-radius: 10px; background-color: #1565c0; color: white !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
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
    st.header("⚙️ Configuración")
    nombre = st.text_input("Nombre del Paciente", value="Emanuel")
    pais = st.selectbox("País de Residencia", list(diccionario.keys()))
    entorno = st.radio("Lugar de Almuerzo", ["Oficina (Recalentable)", "Hogar (Cocina en el momento)"])
    
    mes = datetime.now().month
    es_invierno = (3 <= mes <= 8) if pais == "Argentina 🇦🇷" else (mes >= 9 or mes <= 2)
    temporada_txt = "Otoño/Invierno" si es_invierno else "Primavera/Verano"
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
            <p style='color: #666; font-size: 0.9em;'><i>Nota: Las porciones deben ser ajustadas según el requerimiento calórico individual.</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Formato de exportación más prolijo
        texto_export = f"""
        =========================================
        PLAN ALIMENTARIO PERSONALIZADO
        =========================================
        PACIENTE: {nombre}
        PAÍS: {pais}
        TEMPORADA: {temporada_txt}
        
        SISTEMA: Nutri-Flow Pro
        -----------------------------------------
        
        DESAYUNO Y MERIENDA:
        {desayuno}
        
        ALMUERZO (Logística: {entorno}):
        {plato}
        
        -----------------------------------------
        RECOMENDACIONES GENERALES:
        - Hidratación: 2 a 3 litros de agua por día.
        - Priorizar alimentos frescos y de estación.
        - Masticar bien cada bocado.
        
        Generado el: {datetime.now().strftime('%d/%m/%Y')}
        =========================================
        """
        st.download_button(label="📥 DESCARGAR PLAN PARA EL PACIENTE", data=texto_export, file_name=f"Plan_{nombre}.txt")

with col_der:
    st.markdown("### 📊 Perfil Nutricional")
    st.metric("Energía", "1950 kcal")
    st.metric("Proteínas", "110g", help="Basado en 1.5g/kg de peso promedio")
    st.write("**Balance de Macros:**")
    st.progress(0.6)
    st.caption("Carbohidratos: 50% | Proteínas: 25% | Grasas: 25%")
