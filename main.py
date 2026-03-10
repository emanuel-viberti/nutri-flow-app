import streamlit as st
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Nutri-Flow Global", page_icon="🥗")

st.title("🍎 Nutri-Flow: Gestión Inteligente")
st.markdown("---")

# --- FICHA DEL PACIENTE (LATERAL) ---
with st.sidebar:
    st.header("📋 Ficha del Paciente")
    nombre = st.text_input("Nombre del Paciente")
    pais = st.selectbox("País de Residencia", ["Argentina 🇦🇷", "México 🇲🇽", "España 🇪🇸"])
    objetivo = st.selectbox("Objetivo", ["Descenso de peso", "Mantenimiento", "Hipertrofia"])
    entorno = st.selectbox("Entorno Almuerzo", ["Hogar", "Oficina (con microondas)", "Oficina (sin recursos)"])
    
    st.divider()
    st.write("🔧 **Configuración del Software**")
    mes_actual = datetime.now().month
    hemisferio = "Sur" if pais == "Argentina 🇦🇷" else "Norte"
    temporada = "Otoño/Invierno" if (hemisferio == "Sur" and 3 <= mes_actual <= 8) or (hemisferio == "Norte" and (mes_actual >= 9 or mes_actual <= 2)) else "Primavera/Verano"
    st.info(f"Temporada detectada: **{temporada}**")

# --- LÓGICA DE RECETAS (EJEMPLO DE LAS 50) ---
# Aquí el software decide qué mostrar según tus reglas
st.subheader(f"Plan Sugerido para: {nombre if nombre else '...'}")

if st.button("🚀 Generar Menú Inteligente"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🌅 Desayuno/Merienda")
        if pais == "Argentina 🇦🇷":
            st.success("Opción: Mate con tostadas de pan integral y queso untable.")
        elif pais == "México 🇲🇽":
            st.success("Opción: Café de olla con molletes integrales (poca grasa).")
        else:
            st.success("Opción: Tostada con aceite de oliva virgen y tomate triturado.")

    with col2:
        st.write("### 🍱 Almuerzo (Adaptado)")
        # Lógica de entorno + temporada
        if entorno == "Oficina (con microondas)":
            st.warning("Plato: Tarta integral de zapallitos (Fácil de calentar)")
            st.caption("💡 Tip: Ideal para llevar en táper, no pierde textura.")
        else:
            if temporada == "Otoño/Invierno":
                st.warning("Plato: Guiso de lentejas saludable con cubos de calabaza.")
            else:
                st.warning("Plato: Ensalada completa de fideos integrales y atún.")

    st.markdown("---")
    st.button("🔄 Cambiar opción (Intercambio)")
