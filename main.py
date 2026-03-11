import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- TRADUCCIONES ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# --- 40 DESAYUNOS Y MERIENDAS (DyM) - TODOS REALES ---
desayunos = [
    {"nombre": "Yogur con granola y {frutilla}", "tags": ["gf", "db", "ls"], "rec": "200g yogur descremado + granola.", "p": 12, "c": 28},
    {"nombre": "Tostadas con {palta} y huevo", "tags": ["db", "ls", "veg"], "rec": "1 feta pan integral + 1/2 {palta} + 1 huevo.", "p": 14, "c": 22},
    {"nombre": "Panqueque de avena y banana", "tags": ["db", "ls", "veg"], "rec": "1 huevo + 2 claras + 3 cdas avena.", "p": 18, "c": 30},
    {"nombre": "Omelette de espinaca y queso", "tags": ["gf", "db", "ls", "dl"], "rec": "3 claras + espinaca + queso magro.", "p": 22, "c": 3},
    {"nombre": "Pudín de chía y coco", "tags": ["gf", "vgn", "db", "ls"], "rec": "Chía hidratada en leche vegetal.", "p": 6, "c": 12},
    {"nombre": "Hummus con zanahoria", "tags": ["gf", "vgn", "db", "ls"], "rec": "4 cdas hummus + bastones crudos.", "p": 8, "c": 18},
    {"nombre": "Batido de proteína y arándanos", "tags": ["gf", "db", "dl"], "rec": "Leche descremada + proteína + fruta.", "p": 25, "c": 20},
    {"nombre": "Muffins de huevo y brócoli", "tags": ["gf", "db", "ls", "veg"], "rec": "Huevos batidos con vegetales al horno.", "p": 14, "c": 6},
    {"nombre": "Tostado de jamón y queso", "tags": ["db", "ls"], "rec": "Pan integral + jamón natural + queso magro.", "p": 18, "c": 24},
    {"nombre": "Cottage con frutos rojos", "tags": ["gf", "db", "ls", "dl"], "rec": "150g cottage + {frutilla}.", "p": 16, "c": 12},
    {"nombre": "Porridge de mijo y nueces", "tags": ["gf", "vgn", "db", "ls"], "rec": "Mijo cocido con leche vegetal.", "p": 7, "c": 35},
    {"nombre": "Galletas de arroz con maní", "tags": ["gf", "vgn", "db"], "rec": "2 galletas + crema de maní natural.", "p": 6, "c": 18},
    {"nombre": "Ricota con limón y nuez", "tags": ["gf", "db", "ls", "veg"], "rec": "100g ricota + 2 nueces.", "p": 12, "c": 8},
    {"nombre": "Smoothie de pera y jengibre", "tags": ["gf", "vgn", "db", "ls"], "rec": "Fruta procesada con hojas verdes.", "p": 4, "c": 22},
    {"nombre": "Tofu revuelto y tomate", "tags": ["gf", "vgn", "db", "ls"], "rec": "Tofu salteado con especias.", "p": 15, "c": 5},
    {"nombre": "Fainá de garbanzos y hierbas", "tags": ["gf", "vgn", "db", "ls"], "rec": "Harina de garbanzo horneada.", "p": 10, "c": 25},
    {"nombre": "Yogur de soja y semillas", "tags": ["gf", "vgn", "db", "ls"], "rec": "Yogur vegetal + mix semillas.", "p": 10, "c": 14},
    {"nombre": "Sandwich de pollo y brotes", "tags": ["gf", "db", "ls", "dl"], "rec": "Pan de lino + pollo desmenuzado.", "p": 24, "c": 4},
    {"nombre": "Manzana asada y granola", "tags": ["gf", "vgn", "db", "ls"], "rec": "Fruta al horno con stevia.", "p": 3, "c": 28},
    {"nombre": "Quinoa inflada con leche", "tags": ["gf", "db", "ls", "veg"], "rec": "1 taza quinoa + leche descremada.", "p": 9, "c": 32},
    {"nombre": "Arepa de maíz y queso", "tags": ["gf", "db", "ls"], "rec": "1 unidad mediana a la plancha.", "p": 10, "c": 30},
    {"nombre": "Kéfir con almendras", "tags": ["gf", "db", "ls"], "rec": "200ml kéfir + frutos secos.", "p": 8, "c": 10},
    {"nombre": "Burrito de claras y pavo", "tags": ["db", "ls", "dl"], "rec": "Tortilla integral + claras.", "p": 20, "c": 15},
    {"nombre": "Rollitos de jamón y ricota", "tags": ["gf", "db", "ls"], "rec": "3 rollos rellenos de ricota magra.", "p": 15, "c": 2},
    {"nombre": "Pancitos de queso y chía", "tags": ["gf", "db", "veg"], "rec": "Harina de almendras y queso.", "p": 12, "c": 6},
    {"nombre": "Bowl de papaya y lima", "tags": ["gf", "vgn", "ls"], "rec": "Papaya fresca con jugo de lima.", "p": 2, "c": 25},
    {"nombre": "Smoothie de cacao y banana", "tags": ["vgn", "gf", "db"], "rec": "Leche vegetal + cacao amargo.", "p": 6, "c": 28},
    {"nombre": "Galletas de avena caseras", "tags": ["db", "veg", "ls"], "rec": "Avena y banana al horno.", "p": 5, "c": 22},
    {"nombre": "Triflé de yogur y calabaza", "tags": ["gf", "db", "ls"], "rec": "Capas de yogur y puré dulce.", "p": 10, "c": 18},
    {"nombre": "Infusión con pan de lino", "tags": ["gf", "vgn", "db", "ls"], "rec": "Tostadas de pan de semillas.", "p": 8, "c": 4},
    {"nombre": "Huevo duro y nueces", "tags": ["gf", "db", "ls", "dl"], "rec": "1 huevo + 4 nueces mariposa.", "p": 11, "c": 5},
    {"nombre": "Batido de espirulina y piña", "tags": ["gf", "vgn", "ls"], "rec": "Piña + agua de coco + verde.", "p": 4, "c": 20},
    {"nombre": "Crepe de espinaca y clara", "tags": ["gf", "db", "ls", "veg"], "rec": "Masa de claras y espinaca.", "p": 12, "c": 8},
    {"nombre": "Sopa de avena y canela", "tags": ["vgn", "db", "ls"], "rec": "Avena cocida cremosa.", "p": 6, "c": 30},
    {"nombre": "Bocaditos de banana y coco", "tags": ["gf", "vgn", "db"], "rec": "Rodajas con coco rallado.", "p": 2, "c": 24},
    {"nombre": "Queso magro con membrillo s/azúcar", "tags": ["gf", "db", "ls"], "rec": "Postre vigilante saludable.", "p": 12, "c": 15},
    {"nombre": "Semillas de zapallo tostadas", "tags": ["gf", "vgn", "db", "ls"], "rec": "30g semillas al horno.", "p": 9, "c": 5},
    {"nombre": "Yogur con semillas de lino", "tags": ["gf", "db", "ls"], "rec": "Yogur + lino activado.", "p": 10, "c": 12},
    {"nombre": "Bizcochuelo de avena y manzana", "tags": ["db", "ls", "veg"], "rec": "Porción casera sin azúcar.", "p": 6, "c": 20},
    {"nombre": "Mate con tostadas de arroz", "tags": ["gf", "vgn", "db", "ls"], "rec": "3 tostadas con queso untable.", "p": 5, "c": 18}
]

# --- 60 ALMUERZOS Y CENAS (AyC) - TODOS REALES ---
comidas = [
    {"nombre": "Pollo al grill con calabaza", "tags": ["gf", "db", "ls", "dl"], "rec": "150g pechuga + puré calabaza.", "p": 32, "c": 22},
    {"nombre": "Wok de tofu y arroz integral", "tags": ["vgn", "db", "ls", "dl"], "rec": "Vegetales + 1 taza arroz.", "p": 14, "c": 45},
    {"nombre": "Pescado con {zapallito}", "tags": ["gf", "db", "ls", "dl"], "rec": "180g filete + {zapallito}.", "p": 35, "c": 8},
    {"nombre": "Ensalada de quinoa y {choclo}", "tags": ["gf", "vgn", "db", "ls"], "rec": "1 taza quinoa + {choclo}.", "p": 12, "c": 48},
    {"nombre": "Guiso de {legumbre}", "tags": ["gf", "vgn", "db", "ls"], "rec": "1 taza {legumbre} + sofrito.", "p": 16, "c": 42},
    {"nombre": "{carne} con puré mixto", "tags": ["gf", "ls", "dl"], "rec": "150g {carne} + puré mixto.", "p": 34, "c": 26},
    {"nombre": "Tarta de {zapallito} sin masa", "tags": ["gf", "db", "ls", "veg"], "rec": "Zapallito + huevo + queso.", "p": 18, "c": 14},
    {"nombre": "Wrap integral de pollo", "tags": ["db", "ls", "dl"], "rec": "Tortilla + 100g pollo + lechuga.", "p": 26, "c": 28},
    {"nombre": "Hamburguesa de garbanzo", "tags": ["gf", "vgn", "db", "ls"], "rec": "2 unidades + hojas verdes.", "p": 12, "c": 35},
    {"nombre": "Risotto de cebada y hongos", "tags": ["veg", "db", "ls", "dl"], "rec": "Cebada + champiñones.", "p": 10, "c": 40},
    {"nombre": "Salmón con espárragos", "tags": ["gf", "db", "ls", "dl"], "rec": "150g salmón + espárragos.", "p": 28, "c": 4},
    {"nombre": "Lasaña de berenjena", "tags": ["gf", "db", "ls", "veg"], "rec": "Berenjena + ricota + salsa.", "p": 16, "c": 18},
    {"nombre": "Albóndigas de pollo y tomate", "tags": ["db", "ls", "dl"], "rec": "150g pollo + salsa casera.", "p": 28, "c": 15},
    {"nombre": "Canelones de espinaca", "tags": ["gf", "db", "ls", "veg"], "rec": "2 unidades masa clara.", "p": 18, "c": 12},
    {"nombre": "Brochetas de pavo y vegetales", "tags": ["gf", "db", "ls", "dl"], "rec": "180g pavo + morrón.", "p": 30, "c": 6},
    {"nombre": "Budín de calabaza y queso", "tags": ["gf", "db", "ls", "veg"], "rec": "Calabaza + huevo + queso.", "p": 14, "c": 30},
    {"nombre": "Ceviche de pescado blanco", "tags": ["gf", "db", "ls", "dl"], "rec": "Pescado marinado + limón.", "p": 25, "c": 22},
    {"nombre": "Fideos integrales con brócoli", "tags": ["vgn", "db", "ls", "dl"], "rec": "80g pasta + brócoli.", "p": 12, "c": 48},
    {"nombre": "Milanesas de {carne} al horno", "tags": ["db", "ls", "dl"], "rec": "2 unidades + ensalada.", "p": 32, "c": 20},
    {"nombre": "Tacos de lechuga y carne", "tags": ["gf", "db", "ls", "dl"], "rec": "Lechuga + carne magra.", "p": 26, "c": 8},
    {"nombre": "Pollo al limón con batatas", "tags": ["gf", "ls", "dl"], "rec": "150g pollo + batata.", "p": 28, "c": 30},
    {"nombre": "Ensalada de lentejas", "tags": ["vgn", "gf", "db"], "rec": "Lentejas + mix pimientos.", "p": 14, "c": 35},
    {"nombre": "Tortilla de acelga y claras", "tags": ["gf", "db", "veg"], "rec": "Acelga + 3 claras.", "p": 16, "c": 10},
    {"nombre": "Atún con chauchas", "tags": ["gf", "db", "dl"], "rec": "Atún nat + chauchas + huevo.", "p": 26, "c": 12},
    {"nombre": "Zapallitos rellenos con ricota", "tags": ["gf", "db", "veg"], "rec": "Zapallitos + ricota + nuez.", "p": 15, "c": 15},
    {"nombre": "Estofado de soja texturizada", "tags": ["vgn", "db", "ls"], "rec": "Soja + tomate + zanahoria.", "p": 20, "c": 25},
    {"nombre": "Pavo con ensalada rusa light", "tags": ["gf", "db", "ls"], "rec": "Pavo + vegetales + yogur.", "p": 30, "c": 28},
    {"nombre": "Noodles de calabacín", "tags": ["gf", "vgn", "db"], "rec": "Zoodles + pesto albahaca.", "p": 5, "c": 10},
    {"nombre": "Pizza de polenta", "tags": ["gf", "db", "veg"], "rec": "Base polenta + vegetales.", "p": 12, "c": 40},
    {"nombre": "Medallones de merluza", "tags": ["gf", "db", "ls"], "rec": "2 unidades caseras.", "p": 24, "c": 10},
    {"nombre": "Pollo curry con basmati", "tags": ["gf", "db", "ls"], "rec": "Pollo + curry + arroz.", "p": 28, "c": 35},
    {"nombre": "Milanesa de berenjena", "tags": ["db", "ls", "veg"], "rec": "2 rodajas + ensalada.", "p": 8, "c": 20},
    {"nombre": "Solomillo con manzana", "tags": ["gf", "db", "ls"], "rec": "150g cerdo + manzana.", "p": 32, "c": 15},
    {"nombre": "Ensalada César light", "tags": ["db", "ls"], "rec": "Pollo + aderezo yogur.", "p": 28, "c": 10},
    {"nombre": "Crema de espárragos", "tags": ["gf", "db", "ls"], "rec": "Espárragos + 1 huevo.", "p": 12, "c": 12},
    {"nombre": "Pastel de coliflor y pollo", "tags": ["gf", "db", "ls"], "rec": "Pollo + puré coliflor.", "p": 30, "c": 8},
    {"nombre": "Hummus bowl con falafel", "tags": ["vgn", "db", "ls"], "rec": "Hummus + 3 falafel.", "p": 14, "c": 38},
    {"nombre": "Conejo al ajillo", "tags": ["gf", "db", "ls"], "rec": "150g conejo + perejil.", "p": 32, "c": 2},
    {"nombre": "Ratatouille con huevo", "tags": ["gf", "vgn", "db"], "rec": "Mix vegetales + huevo.", "p": 10, "c": 15},
    {"nombre": "Hamburguesa de mijo", "tags": ["vgn", "gf", "db"], "rec": "2 unidades + tomate.", "p": 8, "c": 35},
    {"nombre": "Revuelto gramajo sano", "tags": ["gf", "db", "ls"], "rec": "Huevo + jamón + zapallo.", "p": 18, "c": 12},
    {"nombre": "Pechuga rellena espinaca", "tags": ["gf", "db", "ls"], "rec": "Pollo + queso crema.", "p": 35, "c": 5},
    {"nombre": "Brochetas de camarón", "tags": ["gf", "db", "ls"], "rec": "Camarón + morrón.", "p": 25, "c": 5},
    {"nombre": "Cazuela de mariscos", "tags": ["gf", "db", "ls"], "rec": "Mix mariscos + tomate.", "p": 28, "c": 10},
    {"nombre": "Tacos de coliflor", "tags": ["vgn", "gf", "db"], "rec": "Coliflor especiada.", "p": 6, "c": 32},
    {"nombre": "Cerdo a la naranja", "tags": ["gf", "db", "ls"], "rec": "150g magro + jugo.", "p": 30, "c": 18},
    {"nombre": "Ensalada Waldorf", "tags": ["gf", "db", "veg"], "rec": "Manzana + apio + nuez.", "p": 6, "c": 22},
    {"nombre": "Berenjena con carne", "tags": ["gf", "db", "ls"], "rec": "Berenjena + carne picada.", "p": 28, "c": 12},
    {"nombre": "Minestrone vegetal", "tags": ["vgn", "db", "ls"], "rec": "Sopa espesa de verduras.", "p": 8, "c": 25},
    {"nombre": "Pescado al papillote", "tags": ["gf", "db", "ls"], "rec": "Filete + vegetales.", "p": 30, "c": 6},
    {"nombre": "Budín ricota y acelga", "tags": ["gf", "db", "ls"], "rec": "Porción abundante.", "p": 16, "c": 10},
    {"nombre": "Wrap de atún y {palta}", "tags": ["db", "ls", "dl"], "rec": "Atún + {palta} + hojas.", "p": 22, "c": 25},
    {"nombre": "Pollo agridulce piña", "tags": ["gf", "ls"], "rec": "Pollo + piña natural.", "p": 28, "c": 28},
    {"nombre": "Canelones de calabaza", "tags": ["db", "ls", "veg"], "rec": "Masa de clara + puré.", "p": 10, "c": 35},
    {"nombre": "Cerdo y piña grill", "tags": ["gf", "db", "ls"], "rec": "Brochetas magras.", "p": 30, "c": 12},
    {"nombre": "Pasta de legumbres", "tags": ["gf", "vgn", "db"], "rec": "Fideos lenteja + tomate.", "p": 20, "c": 35},
    {"nombre": "Sopa cebolla magra", "tags": ["db", "ls", "veg"], "rec": "Cebolla + queso magro.", "p": 12, "c": 20},
    {"nombre": "Hígado encebollado", "tags": ["gf", "db", "ls"], "rec": "150g hígado + cebolla.", "p": 32, "c": 10},
    {"nombre": "Salpicón de ave light", "tags": ["gf", "db", "ls"], "rec": "Pollo + vegetales + clara.", "p": 30, "c": 15},
    {"nombre": "Zapallo y queso azul", "tags": ["gf", "db", "veg"], "rec": "Asado con 20g queso.", "p": 8, "c": 25}
]

# --- LÓGICA DE SELECCIÓN ---
def seleccionar_plato(lista, filtros, term):
    res = [r for r in lista]
    if "Celíaco" in filtros: res = [r for r in res if "gf" in r["tags"]]
    if "Hipertenso" in filtros: res = [r for r in res if "ls" in r["tags"]]
    if "Diabético" in filtros: res = [r for r in res if "db" in r["tags"]]
    if "Vegano" in filtros: res = [r for r in res if "vgn" in r["tags"]]
    if "Dislipemia" in filtros: res = [r for r in res if "dl" in r["tags"]]
    
    final_pool = res if len(res) > 0 else lista
    plato = random.choice(final_pool)
    return {"nom": plato["nombre"].format(**term), "rec": plato["rec"].format(**term), "p": plato["p"], "c": plato["c"]}

# --- INTERFAZ ---
with st.sidebar:
    st.header("👤 Ficha Paciente")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    talla = st.number_input("Talla (cm)", 50, 250, 175)
    peso_act = st.number_input("Peso Actual (kg)", 10.0, 200.0, 75.0)
    edad = st.number_input("Edad", 1, 110, 30)
    pi = (talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9
    st.info(f"⚖️ Peso Ideal Sugerido: {pi:.1f} kg")
    peso_obj = st.number_input("Peso para Cálculo (kg)", 10.0, 200.0, float(pi))
    naf = st.selectbox("Actividad", [1.2, 1.375, 1.55, 1.725, 1.9], format_func=lambda x: {1.2:"Sedentario", 1.375:"Leve", 1.55:"Moderado", 1.725:"Fuerte", 1.9:"Muy Fuerte"}[x])
    st.divider()
    st.header("⚖️ Macros (%)")
    c1, c2, c3 = st.columns(3)
    p_cho, p_pro, p_lip = c1.number_input("% CHO",0,100,50), c2.number_input("% PRO",0,100,20), c3.number_input("% LIP",0,100,30)
    pats = st.multiselect("Patologías", ["Celíaco", "Hipertenso", "Diabético", "Vegano", "Dislipemia"])
    pais = st.selectbox("País", list(paises.keys()))

tmb = (10 * peso_obj) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
get = tmb * naf
imc = peso_act / ((talla/100)**2)

st.title("🍎 Nutri-Flow Pro")
col_info, col_plan = st.columns([1, 2.5])

with col_info:
    st.markdown(f'<div style="background:#f0f2f6;padding:15px;border-radius:10px;border:1px solid #ccc;color:#333"><h4>📊 Informe</h4><b>IMC:</b> {imc:.1f}<br><b>GET:</b> {get:.0f} kcal/día<hr><b>Objetivos:</b><br>🍞 {(get*p_cho/400):.1f}g CHO<br>🍗 {(get*p_pro/400):.1f}g PRO<br>🥑 {(get*p_lip/900):.1f}g LIP</div>', unsafe_allow_html=True)

with col_plan:
    if st.button("🚀 GENERAR PLAN NUTRICIONAL"):
        term = paises[pais]
        for i in range(7):
            st.session_state[f"d{i}_m0"] = seleccionar_plato(desayunos, pats, term)
            st.session_state[f"d{i}_m1"] = seleccionar_plato(comidas, pats, term)
            st.session_state[f"d{i}_m2"] = seleccionar_plato(desayunos, pats, term)
            st.session_state[f"d{i}_m3"] = seleccionar_plato(comidas, pats, term)
        st.session_state.listo = True

if st.session_state.get("listo"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for i, d in enumerate(dias):
        with st.container():
            st.markdown(f'<div style="background:white;padding:12px;border-radius:10px;border-left:5px solid #2e7d32;margin-bottom:10px;color:black;box-shadow:0 2px 5px rgba(0,0,0,0.1)"><b>📅 {d}</b>', unsafe_allow_html=True)
            for j, lab in enumerate(["☕ Desayuno", "☀️ Almuerzo", "🍪 Merienda", "🌙 Cena"]):
                p = st.session_state[f"d{i}_m{j}"]
                st.markdown(f"<b>{lab}:</b> {p['nom']} <small>(P:{p['p']}g C:{p['c']}g)</small><br><i style='color:#666;font-size:0.8em'>{p['rec']}</i>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
