# modules/generator.py
import random

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    best_day = None
    min_error = float('inf')

    # Seguridad: Si el pool está vacío por filtros, devolvemos error controlado
    if not desayunos_pool or not comidas_pool:
        return None, (0, 0, 0, 0)

    for _ in range(2000):
        # Seleccionamos 4 platos al azar
        platos = [
            random.choice(desayunos_pool), # Desayuno
            random.choice(comidas_pool),   # Almuerzo
            random.choice(desayunos_pool), # Merienda
            random.choice(comidas_pool)    # Cena
        ]
        
        # Ajustamos el factor de porción para que las calorías totales coincidan
        kcal_base = sum(p['kcal'] for p in platos)
        factor = get_obj / kcal_base
        factor = max(0.5, min(factor, 2.5)) # Límites de porción lógica
        
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

        # Calculamos el "Error Total" (Diferencia vs lo pedido por el Nutri)
        tk = sum(x["kcal"] for x in dia_actual)
        tp = sum(x["p"] for x in dia_actual)
        tc = sum(x["c"] for x in dia_actual)
        tl = sum(x["l"] for x in dia_actual)
        
        # Error relativo acumulado
        error = (abs(tk - get_obj) / get_obj) + \
                (abs(tp - p_obj) / p_obj) + \
                (abs(tc - c_obj) / c_obj) + \
                (abs(tl - l_obj) / l_obj)
        
        # Penalización por repetición (para fomentar variedad)
        if any(n in historial_global[-10:] for n in nombres_dia):
            error += 0.5 

        # Si este intento es mejor que el anterior, lo guardamos como "el elegido"
        if error < min_error:
            min_error = error
            best_day = (dia_actual, (tk, tp, tc, tl), nombres_dia)
        
        # Si el error es insignificante (menos del 5%), cortamos la búsqueda
        if error < 0.05:
            break

    if best_day:
        historial_global.extend(best_day[2])
        return best_day[0], best_day[1]
    
    return None, (0, 0, 0, 0)
