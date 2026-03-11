# --- LÓGICA MÉDICA ---
tmb = (10 * peso_objetivo) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * naf
imc_actual = peso_actual / ((talla/100)**2)

# Función para determinar el diagnóstico de IMC
def obtener_diagnostico_imc(imc):
    if imc < 18.5: return "Bajo Peso", "#ffeb3b"
    if 18.5 <= imc < 25: return "Normopeso", "#4caf50"
    if 25 <= imc < 30: return "Sobrepeso", "#ff9800"
    if 30 <= imc < 35: return "Obesidad I", "#ff5722"
    if 35 <= imc < 40: return "Obesidad II", "#f44336"
    return "Obesidad III", "#b71c1c"

diag_texto, diag_color = obtener_diagnostico_imc(imc_actual)

# --- MAIN UI ---
st.title("🍎 Nutri-Flow Pro")

col_m, col_p = st.columns([1, 2])

with col_m:
    st.markdown(f"""
    <div class="metric-box">
        <h4>📊 Informe de Consultorio</h4>
        <b>IMC Actual:</b> {imc_actual:.1f} 
        <span style="background-color:{diag_color}; color:white; padding:2px 6px; border-radius:4px; font-size:0.8em; margin-left:5px;">
            {diag_texto}
        </span><br>
        <b>Peso de referencia:</b> {peso_objetivo:.1f} kg<br>
        <b>GET Objetivo:</b> {get:.0f} kcal/día<br>
        <hr>
        <b>Gramos:</b><br>
        🍞 CHO: {(get * p_carb / 400):.1f}g | 🍗 PRO: {(get * p_prot / 400):.1f}g | 🥑 LIP: {(get * p_gras / 900):.1f}g
    </div>
    """, unsafe_allow_html=True)
