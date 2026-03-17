# modules/generator.py
import random

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    best_day = None
    min_error = float('inf')

    if not desayunos_pool or not comidas_pool:
        return None, (0,0,0,0)

    # Aumentamos a 2000 intentos para dar margen a la relajación
    for i in range(2000):
        try:
            platos = [
                random.choice(desayunos_pool), # Des
                random.choice(comidas_pool),   # Alm
                random.choice(desayunos_pool), # Mer
                random.choice(comidas_pool)    # Cen
            ]
            
            kcal_base = sum(p['kcal'] for p in platos)
            factor = get_obj / kcal_base
            factor = max(0.4, min(factor, 2.8)) # Un pelín más de rango de porción
            
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
            
            # Error base
            error = (abs(tk-get_obj)/get_obj) + (abs(tp-p_obj)/p_obj) + (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
            
            # RELAJACIÓN GRADUAL:
            # Si pasaron 1000 intentos y no hay éxito, bajamos la penalización por repetir
            penalizacion_repetido = 0.4 if i < 1000 else 0.1
            
            if any(n in historial_global[-12:] for n in nombres_dia):
                error += penalizacion_repetido

            if error < min_error:
                min_error = error
                best_day = (dia_actual, (tk, tp, tc, tl), nombres_dia)
            
            # Si el error es menor al 5% (o 10% si estamos en modo emergencia), cortamos
            umbral_exito = 0.05 if i < 1200 else 0.15
            if error < umbral_exito: break 

        except Exception:
            continue

    # Si después de todo NO hay nada, bajamos la guardia total y devolvemos el mejor intento
    if best_day:
        # Solo agregamos al historial si no queremos repetir TAN seguido
        historial_global.extend(best_day[2])
        return best_day[0], best_day[1]
    
    return None, (0,0,0,0)
