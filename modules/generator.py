import random
from modules.config import LIMITES_SEMANALES

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    """
    Motor de generación ultra-flexible. 
    Si no encuentra la combinación ideal, relaja los parámetros para asegurar el resultado.
    """
    
    # Intentaremos hasta 3000 veces para agotar posibilidades
    for intento in range(3000): 
        dia = []
        nombres_dia = []
        dist = [get_obj * 0.20, get_obj * 0.35, get_obj * 0.15, get_obj * 0.30]
        
        # Cada 500 intentos fallidos, aumentamos la tolerancia un 5% (Dinámico)
        # Esto evita que la app se trabe si pides algo muy difícil
        tolerancia_actual = 0.15 + (intento // 500) * 0.05
        
        for j in range(4):
            pool = desayunos_pool if j in [0, 2] else comidas_pool
            
            # Variedad: No repetir últimos 8 platos
            pool_variedad = [p for p in pool if p["nombre"] not in historial_global[-8:]]
            seleccion = pool_variedad if pool_variedad else pool
            
            plato_base = random.choice(seleccion)
            
            # Factor de porción redondeado a 0.25
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
        
        # Totales del intento actual
        tk, tp, tc, tl = sum(x["kcal"] for x in dia), sum(x["p"] for x in dia), sum(x["c"] for x in dia), sum(x["l"] for x in dia)
        
        def check(real, objetivo, tol): 
            if objetivo <= 0: return True
            return abs(real - objetivo) / objetivo <= tol
        
        # Validación con la tolerancia que crece según los intentos
        if all([check(tk, get_obj, tolerancia_actual), 
                check(tp, p_obj, tolerancia_actual), 
                check(tc, c_obj, tolerancia_actual), 
                check(tl, l_obj, tolerancia_actual)]):
            
            historial_global.extend(nombres_dia)
            return dia, (tk, tp, tc, tl)
            
    return None, (0, 0, 0, 0)
