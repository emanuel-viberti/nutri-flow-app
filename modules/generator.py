# modules/generator.py
import random

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    best_day = None
    min_error = float('inf')

    if not desayunos_pool or not comidas_pool:
        return None, (0,0,0,0)

    # Probamos con 5000 como dice GPT, pero con lógica de "escape"
    for i in range(5000):
        try:
            platos = [
                random.choice(desayunos_pool),
                random.choice(comidas_pool),
                random.choice(desayunos_pool),
                random.choice(comidas_pool)
            ]
            
            kcal_base = sum(p['kcal'] for p in platos)
            if kcal_base == 0: continue
            
            factor = get_obj / kcal_base
            # Un rango un poco más amplio para que las 1584 kcal sean más fáciles de alcanzar
            factor = max(0.4, min(factor, 3.0)) 
            
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
            
            # Error matemático puro
            error = (abs(tk-get_obj)/get_obj) + (abs(tp-p_obj)/p_obj) + (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
            
            # Bajamos la penalización por repetición drásticamente después de 2000 intentos
            penalizacion = 0.3 if i < 2000 else 0.05
            if any(n in historial_global[-12:] for n in nombres_dia):
                error += penalizacion

            if error < min_error:
                min_error = error
                best_day = (dia_actual, (tk, tp, tc, tl), nombres_dia)
            
            # Si el error es bajísimo, cortamos antes de llegar a los 5000
            if error < 0.06: break 

        except Exception:
            continue

    if best_day:
        historial_global.extend(best_day[2])
        return best_day[0], best_day[1]
    
    return None, (0,0,0,0)
