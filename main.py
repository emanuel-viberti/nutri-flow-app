import streamlit as st
from datetime import datetime
import random

# CONFIGURACIÓN ESTÉTICA
st.set_page_config(page_title="Nutri-Flow Pro | Dashboard", page_icon="🍏", layout="wide")

# CSS PERSONALIZADO (Para que no parezca una web común)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #2e7d32; color: white; height: 3em; font-weight: bold; }
    .stDownloadButton>button { width: 100%; border-radius: 20px; background-color: #1565c0; color: white; }
    .plan-card { padding: 20px; border-radius: 15px; background-color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); border-left: 5px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ACTUALIZADA ---
diccionario = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "frutilla": "Frutilla", "desayuno": "Mate con tostadas de pan integral y queso untable"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "frutilla": "Fresa", "desayuno": "Café de olla con molletes integrales y frijol"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "frutilla": "Fresa", "desayuno": "Tostada con aceite de oliva virgen y tomate triturado"}
}

recetas_oficina = ["Tarta de {zapallito} integral con semillas", "Ensalada de {porotos}, {choclo} y huevo", "Wrap integral de pollo y {palta}", "Wok de arroz con vegetales de estación"]
recetas_hogar = ["Milanesas de pollo al horno con puré", "Guiso de lentejas con cubos de calabaza", "Pescado al horno con rodajas de {zapallito}", "Pastel de papa y carne magra"]

# --- INTERFAZ PRINCIPAL ---
st.title("🥗 Nutri-Flow: Gestión Profesional")
st.subheader("Generador Inteligente de Planes Alimentarios")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424434.png", width=100)
    st.header("⚙️ Panel de Control")
    nombre = st.text_input("Paciente", placeholder="Ej: Emanuel")
    pais = st.selectbox("Mercado / País", list(diccionario.keys()))
    entorno = st.radio("Logística del Almuerzo", ["Oficina (Recalentable)", "Hogar (Cocina en el momento)"])
    
    # Lógica de Temporada
    mes = datetime.now().month
    es_invierno = (3 <= mes <= 8) if pais == "Argentina 🇦🇷" else (mes >= 9 or mes <= 2)
    temporada_txt = "Otoño/Invierno" if es_invierno else "Primavera/Verano"
    st.caption(f"📅 **Temporada Actual:** {temporada_txt}")
    st.divider()
    st.write("🔒 **Módulo Pro:** Patologías (Próximamente)")

# --- ÁREA DE TRABAJO ---
col_izq, col_der = st.columns([2, 1])

with col_izq:
    if st.button("🚀 GENERAR PLAN NUTRICIONAL"):
        term = diccionario[pais]
        
        # Lógica de selección con los 50 (simplificado para el código)
        plato = random.choice(recetas_oficina if "Oficina" in entorno else recetas_hogar).format(**term)
        desayuno = term["desayuno"]
        
        st.markdown(f"""
        <div class="plan-card">
            <h3>📋 Plan Sugerido para {nombre}</h3>
            <p><b>📍 Región:</b> {pais} | <b>🌡️ Clima:</b> {temporada_txt}</p>
            <hr>
            <p><b>🌅 Desayuno/Merienda:</b> {desayuno}</p>
            <p><b>🍱 Almuerzo ({entorno}):</b> {plato}</p>
            <p><b>🥤 Hidratación:</b> 2.5 Litros de agua diarios.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- PREPARACIÓN DEL ARCHIVO ---
        texto_export = f"PLAN NUTRICIONAL: {nombre}\nPaís: {pais}\n\nDesayuno: {desayuno}\nAlmuerzo: {plato}\n\nNutri-Flow Pro 2026"
        st.download_button(label="📥 DESCARGAR PLAN PARA EL PACIENTE", data=texto_export, file_name=f"Plan_{nombre}.txt")
    else:
        st.info("Configurá los datos en el panel izquierdo y hacé clic en Generar.")

with col_der:
    st.markdown("### 📊 Métricas del Plan")
    st.metric("Calorías Promedio", "1900 kcal", "+50 kcal")
    st.metric("Proteínas", "115g", "Ideal")
    st.progress(0.7)
    st.caption("Balance de Macronutrientes")
