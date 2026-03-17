import random
from modules.config import LIMITES_SEMANALES

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    """
    Motor de generación de menú diario. 
    Intenta cuadrar los platos del pool con los objetivos de macros del usuario.
    """
    # Intentos para cuadrar el día (aumentamos a 1000 para dar más chances)
    for _ in range(1000): 
        dia = []
        nombres_dia = []
        # Distribución sugerida de kcal por comida: Desayuno 20%, Almuerzo 35%, Merienda 15%, Cena 30%
        dist = [get_obj * 0.20, get_obj * 0.35, get_obj * 0.15, get_obj * 0.30]
        
        for j in range(4):
            pool = desayunos_pool if j in [0, 2] else comidas_pool
            
            # Filtro de variedad: Evita repetir platos que salieron recientemente
            pool_variedad = [p for p in pool if p["nombre"] not in historial_global[-8:]]
            
            # Si el filtro de variedad vacía la lista, usamos el pool original
            seleccion = pool_variedad if pool_variedad else pool
            
            # Selección al azar del plato
            plato_base = random.choice(seleccion)
            
            # Calculamos cuánto de ese plato hay que comer (factor de porción)
            factor = round((dist[j] / plato_base["kcal"]) * 4) / 4
            if factor <= 0: factor = 0.25 # Mínimo un cuarto de porción
            
            dia.append({
                "nom": plato_base["nombre"],
                "kcal": plato_base["kcal"] * factor,
                "p": plato_base["p"] * factor,
                "c": plato_base["c"] * factor,
                "l": plato_base["l"] * factor,
                "factor": factor
            })
            nombres_dia.append(plato_base["nombre"])
        
        # Sumamos totales del día generado
        tk = sum(x["kcal"] for x in dia)
        tp = sum(x["p"] for x in dia)
        tc = sum(x["c"] for x in dia)
        tl = sum(x["l"] for x in dia)
        
        # FUNCIÓN DE CONTROL: Margen de error aumentado al 15% (0.15) 
        # para absorber cambios manuales de macros.
        def check(real, objetivo): 
            if objetivo <= 0: return True
            return abs(real - objetivo) / objetivo <= 0.15
        
        # Si el día cumple con los 4 objetivos, lo validamos
        if all([check(tk, get_obj), check(tp, p_obj), check(tc, c_obj), check(tl, l_obj)]):
            # Registramos en el historial para la próxima vuelta
            historial_global.extend(nombres_dia)
            return dia, (tk, tp, tc, tl)
            
    # Si después de 1000 intentos no cuadra, devuelve None para avisar en la UI
    return None, (0, 0, 0, 0)
