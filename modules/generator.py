# modules/generator.py
import random

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    best_day = None
    min_error = float('inf')

    # Seguridad por si las listas están vacías
    if not desayunos_pool or not comidas_pool:
        return None, (0,0,0,0)

    # Intentamos 1500 combinaciones al azar
    for _ in range(1500):
        try:
            platos = [
                random.choice(desayunos_pool), # Des
                random.choice(comidas_pool),   # Alm
                random.choice(desayunos_pool), # Mer
                random.choice(comidas_pool)    # Cen
            ]
            
            kcal_base = sum(p['kcal'] for p in platos)
            factor = get_obj / kcal_base
            factor = max(0.5, min(factor, 2.5)) # Factores de porción realistas
            
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

            # Cálculo de error acumulado vs lo pedido por Emmanuel
            tk = sum(x["kcal"] for x in dia_actual)
            tp = sum(x["p"] for x in dia_actual)
            tc = sum(x["c"] for x in dia_actual)
            tl = sum(x["l"] for x in dia_actual)
            
            error = (abs(tk-get_obj)/get_obj) + (abs(tp-p_obj)/p_obj) + (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
            
            # Penalizamos si el plato se repite en la semana
            if any(n in historial_global[-12:] for n in nombres_dia):
                error += 0.4

            if error < min_error:
                min_error = error
                best_day = (dia_actual, (tk, tp, tc, tl), nombres_dia)
            
            if error < 0.05: break # Éxito total, cortamos búsqueda
        except:
            continue

    if best_day:
        historial_global.extend(best_day[2])
        return best_day[0], best_day[1]
    
    return None, (0,0,0,0)
