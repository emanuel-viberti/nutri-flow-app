# modules/generator.py
import random

# modules/generator.py (Asegurate de que termine así)

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    # ... (Mantené la lógica de los 3000 intentos y el factor hasta 3.5 que pusimos recién)
    # Esta función ya está lista para ser llamada individualmente.
    pass

    if not desayunos_pool or not comidas_pool:
        return None, (0,0,0,0)

    # Subimos a 3000 intentos porque 55% de carbos es un reto para este JSON
    for i in range(3000):
        platos = [
            random.choice(desayunos_pool),
            random.choice(comidas_pool),
            random.choice(desayunos_pool),
            random.choice(comidas_pool)
        ]
        
        kcal_base = sum(p['kcal'] for p in platos)
        if kcal_base == 0: continue
        
        factor = get_obj / kcal_base
        
        # RELAJACIÓN DE PORCIÓN: Si es difícil llegar, permitimos porciones más grandes (hasta 3.5)
        # Esto es clave para que el "Gordo Compu" llegue a los carbos con platos de baja densidad.
        max_f = 3.5 if i > 1000 else 2.5
        factor = max(0.4, min(factor, max_f))
        
        dia_actual = []
        nombres_dia = []
        for p in platos:
            dia_actual.append({
                "nom": p["nombre"],
                "kcal": p["kcal"] * factor,
                "p": p["p"] * factor,
                "c": p["c"] * factor,
                "l": p["l"] * factor,
                "factor": round(factor * 4) / 4
            })
            nombres_dia.append(p["nombre"])

        tk = sum(x["kcal"] for x in dia_actual)
        tp = sum(x["p"] for x in dia_actual)
        tc = sum(x["c"] for x in dia_actual)
        tl = sum(x["l"] for x in dia_actual)
        
        # Error matemático
        error = (abs(tk-get_obj)/get_obj) + (abs(tp-p_obj)/p_obj) + (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
        
        # Bajamos la importancia de la repetición si el objetivo es difícil
        if any(n in historial_global[-10:] for n in nombres_dia):
            error += 0.2

        if error < min_error:
            min_error = error
            best_day = (dia_actual, (tk, tp, tc, tl), nombres_dia)
        
        # Si el error es aceptable, cortamos. 
        # Si pedís 55% de carbos, un 10% de error es mejor que nada.
        umbral = 0.07 if i < 1500 else 0.15
        if error < umbral: break 

    if best_day:
        historial_global.extend(best_day[2])
        return best_day[0], best_day[1]
    
    return None, (0,0,0,0)
