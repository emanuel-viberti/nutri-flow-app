# modules/generator.py
import random

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    best_day = None
    min_error = float('inf')

    if not desayunos_pool or not comidas_pool:
        return None, (0,0,0,0)

    # 1000 intentos es el punto justo entre velocidad y precisión
    for i in range(1000):
        # Selección aleatoria de los pools que me pasaste
        platos = [
            random.choice(desayunos_pool), # Desayuno
            random.choice(comidas_pool),   # Almuerzo
            random.choice(desayunos_pool), # Merienda
            random.choice(comidas_pool)    # Cena
        ]
        
        kcal_base = sum(p['kcal'] for p in platos)
        if kcal_base == 0: continue
        
        # Emmanuel, el secreto está en este factor. 
        # Si pedís 1584 kcal, el factor ajusta las porciones de estos platos.
        factor = get_obj / kcal_base
        factor = max(0.4, min(factor, 2.5)) 
        
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
        
        # Calculamos qué tan lejos estamos de tus macros objetivo
        error = (abs(tk-get_obj)/get_obj) + (abs(tp-p_obj)/p_obj) + (abs(tc-c_obj)/c_obj) + (abs(tl-l_obj)/l_obj)
        
        # Variedad: si el plato se usó hace poco, le sumamos "error" para buscar otro
        # Pero si pasamos del intento 500, bajamos esta exigencia para que no tire error amarillo
        penalidad = 0.5 if i < 500 else 0.1
        if any(n in historial_global[-12:] for n in nombres_dia):
            error += penalidad

        if error < min_error:
            min_error = error
            best_day = (dia_actual, (tk, tp, tc, tl), nombres_dia)
        
        # Si encontramos algo con menos del 6% de error, lo tomamos y cerramos
        if error < 0.06: break 

    if best_day:
        historial_global.extend(best_day[2])
        return best_day[0], best_day[1]
    
    return None, (0,0,0,0)
