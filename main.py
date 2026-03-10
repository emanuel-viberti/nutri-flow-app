import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎")

# --- BASE DE DATOS DE DICCIONARIO POR PAÍS ---
diccionario = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "porotos": "Porotos", "frutilla": "Frutilla"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "porotos": "Frijoles", "frutilla": "Fresa"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "porotos": "Alubias", "frutilla": "Fresa"}
}

# --- BASE DE DATOS DE 50 RECETAS (Muestra para el MVP) ---
# Aquí cargo las categorías que aprobaste ayer
recetas_oficina = ["Tarta de {zapallito} integral", "Ensalada de {porotos} y {choclo}", "Wrap de pollo y {palta}", "Arroz primavera con huevo"]
recetas_invierno = ["Guiso de lentejas nutri", "Cazuela de pollo y vegetales", "Pastel de papa y carne magra", "Sopa crema de calabaza"]
recetas_verano = ["Ensalada de fideos y atún", "Pechuga al limón con tomate", "Salpicón de ave", "Tostadas con hummus y vegetales"]

st.title("🍎 Nutri-Flow: Gestión Inteligente")

with st.sidebar:
    st.header("📋 Configuración")
    nombre = st.text_input("Paciente", value="Emanuel")
    pais = st.selectbox("País", list(diccionario.keys()))
    entorno = st.selectbox("Lugar de Almuerzo", ["Oficina (con micro)", "Hogar", "Sin recursos"])
    
    # Lógica de Temporada Automática
    mes = datetime.now().month
    hemisferio_sur = True if pais == "Argentina 🇦🇷" else False
    es_invierno = (3 <= mes <= 8) if hemisferio_sur else (mes >= 9 or mes <= 2)
    temporada_txt = "Otoño/Invierno" if es_invierno else "Primavera/Verano"
    st.info(f"📅 Temporada: {temporada_txt}")

# --- GENERADOR ---
if st.button("🚀 Generar Plan Personalizado"):
    st.subheader(f"Plan para {nombre}")
    
    # 1. Selección de Receta según lógica
    term = diccionario[pais] # Diccionario del país elegido
    
    if "Oficina" in entorno:
        plato_base = random.choice(recetas_oficina)
    elif es_invierno:
        plato_base = random.choice(recetas_invierno)
    else:
        plato_base = random.choice(recetas_verano)
        
    # 2. Traducción automática de ingredientes
    plato_final = plato_base.format(**term)
    
    # --- MOSTRAR RESULTADO ---
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Calorías Sugeridas", "1950 kcal")
        st.write("### 🌅 Desayuno")
        opcion_desayuno = "Mate con tostadas" if pais == "Argentina 🇦🇷" else "Café con molletes" if pais == "México 🇲🇽" else "Pan con tomate y oliva"
        st.success(opcion_desayuno)
        
    with col2:
        st.metric("Proteínas", "110g")
        st.write(f"### 🍱 Almuerzo ({entorno})")
        st.warning(plato_final)
        
    st.divider()
    st.info("💡 Este plan se ajustó automáticamente a los ingredientes disponibles en tu región y la temporada actual.")
