# modules/generator.py
import random

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    best_day = None
    min_error = float('inf')

    for _ in range(2000):
        dia_actual = []
        nombres_dia = []
        
        # Elegimos 4 platos al azar (2 desayunos/meriendas, 2 almuerzos/cenas)
        platos = [
            random.choice(desayunos_pool), # Desayuno
            random.choice(comidas_pool),   # Almuerzo
            random.choice(desayunos_pool), # Merienda
            random.choice(comidas_pool)    # Cena
        ]
        
        # Ajustamos el factor global del día para que las KCAL cierren
        kcal_base = sum(p['kcal'] for p in platos)
        factor = get_obj / kcal_base
        # Limitamos factor para no tener porciones locas
        factor = max(0.5, min(factor, 2.5)) 
        
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

        # Calculamos error total de este intento (Diferencia vs Objetivo)
        tk = sum(x["kcal"] for x in dia_actual)
        tp = sum(x["p"] for x in dia_actual)
        tc = sum(x["c"] for x in dia_actual)
        tl = sum(x["l"] for x in dia_actual)
        
        error = abs(tk-get_obj)/get_obj + abs(tp-p_obj)/p_obj + abs(tc-c_obj)/c_obj + abs(tl-l_obj)/l_obj
        
        # Si es el mejor error hasta ahora, lo guardamos
        if error < min_error:
            # Penalizamos si el plato ya está en el historial reciente
            penalizacion = 0.5 if any(n in historial_global[-8:] for n in nombres_dia) else 0
            if (error + penalizacion) < min_error:
                min_error = error + penalizacion
                best_day = (dia_actual, (tk, tp, tc, tl), nombres_dia)
        
        # Si el error es casi nulo (menos del 5%), cortamos acá por éxito
        if error < 0.05:
            break

    # Retornamos el mejor resultado que hayamos encontrado
    historial_global.extend(best_day[2])
    return best_day[0], best_day[1]
