import streamlit as st
import random

st.set_page_config(page_title="Nutri-Flow Pro", page_icon="🍎", layout="wide")

# --- BASE DE DATOS LOCALIZADA ---
paises = {
    "Argentina 🇦🇷": {"zapallito": "Zapallito", "palta": "Palta", "choclo": "Choclo", "frutilla": "Frutilla", "carne": "Peceto", "legumbre": "Lentejones"},
    "México 🇲🇽": {"zapallito": "Calabacita", "palta": "Aguacate", "choclo": "Elote", "frutilla": "Fresa", "carne": "Bistec", "legumbre": "Frijoles"},
    "España 🇪🇸": {"zapallito": "Calabacín", "palta": "Aguacate", "choclo": "Maíz", "frutilla": "Fresa", "carne": "Ternera", "legumbre": "Alubias"}
}

# --- 40 DESAYUNOS Y MERIENDAS (DyM) ---
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
    {"nombre": "Fainá de garbanzos", "tags": ["gf", "vgn", "db", "ls"], "rec": "Harina de garbanzo horneada.", "p": 10, "c": 25},
    {"nombre": "Yogur de soja y semillas", "tags": ["gf", "vgn", "db", "ls"], "rec": "Yogur vegetal + mix semillas.", "p": 10, "c": 14},
    {"nombre": "Sandwich de pollo y brotes", "tags": ["gf", "db", "ls", "dl"], "rec": "Pan de lino + pollo desmenuzado.", "p": 24, "c": 4},
    {"nombre": "Manzana asada y granola", "tags": ["gf", "vgn", "db", "ls"], "rec": "Fruta al horno con stevia.", "p": 3, "c": 28},
    {"nombre": "Quinoa inflada con leche", "tags": ["gf", "db", "ls", "veg"], "rec": "1 taza quinoa + leche descremada.", "p": 9, "c": 32},
    {"nombre": "Burrito de claras y pavo", "tags": ["db", "ls", "dl"], "rec": "Tortilla integral + claras + pavo.", "p": 20, "c": 15},
    {"nombre": "Bruschetta de tomate y albahaca", "tags": ["vgn", "db", "ls"], "rec": "Pan integral tostado con tomate.", "p": 5, "c": 20},
    {"nombre": "Kéfir con almendras", "tags": ["gf", "db", "ls"], "rec": "200ml kéfir + 5 almendras.", "p": 8, "c": 10},
    {"nombre": "Pancitos de queso y chía", "tags": ["gf", "db", "veg"], "rec": "Harina de almendras + queso + chía.", "p": 12, "c": 6},
    {"nombre": "Bowl de papaya y lima", "tags": ["gf", "vgn", "ls"], "rec": "Fruta fresca con jugo de lima.", "p": 2, "c": 25},
    {"nombre": "Arepa de maíz con queso magro", "tags": ["gf", "db", "ls"], "rec": "1 arepa mediana + queso sin sal.", "p": 10, "c": 30},
    {"nombre": "Rollitos de jamón y ricota", "tags": ["gf", "db", "ls"], "rec": "3 rollitos de jamón rellenos.", "p": 15, "c": 2},
    {"nombre": "Smoothie de cacao y banana", "tags": ["vgn", "gf", "db"], "rec": "Leche vegetal + cacao amargo.", "p": 6, "c": 28},
    {"nombre": "Galletas de avena caseras", "tags": ["db", "veg", "ls"], "rec": "Avena + banana pisada al horno.", "p": 5, "c": 22},
    {"nombre": "Triflé de yogur y calabaza", "tags": ["gf", "db", "ls"], "rec": "Yogur + puré dulce de calabaza.", "p": 10, "c": 18},
    {"nombre": "Infusión con tostadas de arroz", "tags": ["gf", "vgn", "db", "ls"], "rec": "3 tostadas con mermelada s/azúcar.", "p": 3, "c": 20},
    {"nombre": "Huevo duro y mix de frutos secos", "tags": ["gf", "db", "ls", "dl"], "rec": "1 huevo + 15g de nueces.", "p": 11, "c": 5},
    {"nombre": "Batido de espirulina y piña", "tags": ["gf", "vgn", "ls"], "rec": "Piña + agua de coco + espirulina.", "p": 4, "c": 20},
    {"nombre": "Crepe de espinaca", "tags": ["gf", "db", "ls", "veg"], "rec": "Masa de espinaca y clara.", "p": 12, "c": 8},
    {"nombre": "Sopa de avena y canela", "tags": ["vgn", "db", "ls"], "rec": "Avena cocida en agua con especias.", "p": 6, "c": 30},
    {"nombre": "Bocaditos de banana y coco", "tags": ["gf", "vgn", "db"], "rec": "Banana rodajas con coco rallado.", "p": 2, "c": 24},
    {"nombre": "Queso magro con dulce de membrillo s/azúcar", "tags": ["gf", "db", "ls"], "rec": "Postre vigilante versión saludable.", "p": 12, "c": 15},
    {"nombre": "Semillas de zapallo tostadas", "tags": ["gf", "vgn", "db", "ls"], "rec": "30g semillas naturales al horno.", "p": 9, "c": 5},
    {"nombre": "Yogur con semillas de lino", "tags": ["gf", "db", "ls"], "rec": "Yogur descremado + lino activado.", "p": 10, "c": 12},
    {"nombre": "Infusión con bizcochuelo de avena", "tags": ["db", "ls", "veg"], "rec": "1 porción pequeña casera.", "p": 6, "c": 20}
]

# --- 60 ALMUERZOS Y CENAS (AyC) ---
comidas = [
    {"nombre": "Pechuga al grill con calabaza", "tags": ["gf", "db", "ls", "dl"], "rec": "150g pollo + calabaza asada.", "p": 32, "c": 22},
    {"nombre": "Wok de tofu y arroz integral", "tags": ["vgn", "db", "ls", "dl"], "rec": "Vegetales + 1 taza arroz.", "p": 14, "c": 45},
    {"nombre": "Pescado con rodajas de {zapallito}", "tags": ["gf", "db", "ls", "dl"], "rec": "180g pescado + {zapallito}.", "p": 35, "c": 8},
    {"nombre": "Ensalada de quinoa y {choclo}", "tags": ["gf", "vgn", "db", "ls"], "rec": "Quinoa + {choclo} + tomate.", "p": 12, "c": 48},
    {"nombre": "Guiso de {legumbre} y vegetales", "tags": ["gf", "vgn", "db", "ls"], "rec
