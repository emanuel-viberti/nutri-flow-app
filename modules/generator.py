# modules/generator.py
import random

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    best_day = None
    min_error = float('inf')

    # Validación de seguridad básica
    if not desayunos_pool or not comidas_pool:
        return None, (0,0,0,0)

    # Bajamos la cantidad de intentos pero los hacemos más efectivos
    for i in range(1000):
        # Selección aleatoria simple
        platos = [
            random.choice(desayunos_pool), # Desayuno
            random.choice(comidas_pool),   # Almuerzo
            random.choice(desayunos_pool), # Merienda
            random.choice(comidas_pool)    # Cena
        ]
        
        # Calculamos el factor necesario para llegar a las Kcal objetivo
        kcal_base = sum(p['kcal'] for p in platos)
        if kcal_base == 0: continue
        
        factor = get_obj / kcal_base
        # Rango de porción flexible (0.5 a 2.5 veces la porción base)
        factor = max(0.5, min(factor, 2.5))
        
        dia_actual = []
        nombres_dia = []
        for p in platos:
            dia_actual.append({
                "nom": p["nombre"],
                "kcal": p["kcal"] * factor,
                "p": p["p"] * factor,
                "c": p["c"] * factor,
                "l": p["l"] * factor,
                "factor": round(factor * 4) / 4 # Redondeo a cuartos (0.25, 0.5, etc)
            })
            nombres_dia.append(p["nombre"])

        # Totales del día generado
        tk = sum(x["kcal"] for x in dia_actual)
        tp = sum(x["p"] for x in dia_actual)
        tc = sum(x["c"] for x in dia_actual)
        tl = sum(x["l"] for x in dia_actual)
        
        # Error matemático (Kcal + Macros)
        error = (abs(tk-get_obj)/get_obj) + (abs(tp-p_obj)/p_obj) + (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
        
        # Penalización por repetición (solo si ya se usó mucho en la semana)
        # Bajamos la penalización para que no bloquee el resultado
        for n in nombres_dia:
            if n in historial_global[-12:]:
                error += 0.1 

        # Guardamos el mejor resultado hasta ahora
        if error < min_error:
            min_error = error
            best_day = (dia_actual, (tk, tp, tc, tl), nombres_dia)
        
        # Si es suficientemente bueno (menos del 8% de error), cortamos acá
        if error < 0.08:
            break

    if best_day:
        # Registramos en el historial para intentar variar en el próximo día
        historial_global.extend(best_day[2])
        return best_day[0], best_day[1]
    
    return None, (0,0,0,0)
