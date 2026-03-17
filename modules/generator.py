import random
from modules.config import LIMITES_SEMANALES

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    """
    Motor de generación de menú semanal para Nutri-Flow Pro.
    Busca combinar platos para alcanzar los objetivos calóricos y de macros.
    """
    
    # Aumentamos a 2000 intentos para dar más flexibilidad al azar
    for _ in range(2000): 
        dia = []
        nombres_dia = []
        
        # Distribución de energía por comida (20% Des, 35% Alm, 15% Mer, 30% Cen)
        dist = [get_obj * 0.20, get_obj * 0.35, get_obj * 0.15, get_obj * 0.30]
        
        for j in range(4):
            # Seleccionamos el pool (0 y 2 son desayunos/meriendas, 1 y 3 son almuerzos/cenas)
            pool = desayunos_pool if j in [0, 2] else comidas_pool
            
            # Filtro de variedad: Evita repetir los últimos 8 platos servidos
            pool_variedad = [p for p in pool if p["nombre"] not in historial_global[-8:]]
            seleccion = pool_variedad if pool_variedad else pool
            
            # Elegir plato al azar
            plato_base = random.choice(seleccion)
            
            # Calcular factor de porción para acercarse a la caloría de esa comida
            # Redondeamos a cuartos de porción (0.25, 0.5, 0.75, 1, 1.25...)
            factor = round((dist[j] / plato_base["kcal"]) * 4) / 4
            if factor <= 0: factor = 0.25
            
            dia.append({
                "nom": plato_base["nombre"],
                "kcal": plato_base["kcal"] * factor,
                "p": plato_base["p"] * factor,
                "c": plato_base["c"] * factor,
                "l": plato_base["l"] * factor,
                "factor": factor
            })
            nombres_dia.append(plato_base["nombre"])
        
        # Totales logrados en este intento
        tk = sum(x["kcal"] for x in dia)
        tp = sum(x["p"] for x in dia)
        tc = sum(x["c"] for x in dia)
        tl = sum(x["l"] for x in dia)
        
        # FUNCIÓN DE CONTROL CON TOLERANCIA DEL 20% (0.20)
        # Esto permite que el plan sea exitoso aunque no sea matemáticamente perfecto.
        def check(real, objetivo): 
            if objetivo <= 0: return True
            return abs(real - objetivo) / objetivo <= 0.20
        
        # Verificamos si los 4 parámetros (kcal, P, C, G) están dentro del margen
        if all([check(tk, get_obj), check(tp, p_obj), check(tc, c_obj), check(tl, l_obj)]):
            historial_global.extend(nombres_dia)
            return dia, (tk, tp, tc, tl)
            
    # Si después de 2000 intentos no hay éxito, devuelve None
    return None, (0, 0, 0, 0)
