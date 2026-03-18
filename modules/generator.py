# modules/generator.py
import random

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    """
    Genera una combinación de 4 platos (Des, Alm, Mer, Cen) que se ajuste a los macros 
    objetivo mediante un factor de escala de porción.
    """
    best_day = None
    min_error = float('inf')

    # Validación de seguridad: si no hay alimentos, no podemos generar nada
    if not desayunos_pool or not comidas_pool:
        return None, (0,0,0,0)

    # Realizamos 3000 intentos para encontrar la mejor combinación matemática
    for i in range(3000):
        try:
            # Selección aleatoria de platos
            platos = [
                random.choice(desayunos_pool), # Desayuno
                random.choice(comidas_pool),   # Almuerzo
                random.choice(desayunos_pool), # Merienda
                random.choice(comidas_pool)    # Cena
            ]
            
            # Cálculo del factor de escala basado en Kcal
            kcal_base = sum(p['kcal'] for p in platos)
            if kcal_base == 0: continue
            
            factor_teorico = get_obj / kcal_base
            
            # FLEXIBILIDAD DE PORCIÓN: 
            # Si el objetivo es difícil (muchos carbos), permitimos porciones más grandes
            # a medida que avanzan los intentos.
            max_permitido = 3.5 if i > 1500 else 2.5
            factor = max(0.4, min(factor_teorico, max_permitido))
            
            dia_actual = []
            nombres_dia = []
            for p in platos:
                dia_actual.append({
                    "nom": p["nombre"],
                    "kcal": p["kcal"] * factor,
                    "p": p["p"] * factor,
                    "c": p["c"] * factor,
                    "l": p["l"] * factor,
                    "factor": round(factor * 4) / 4 # Redondeo a cuartos (0.25, 0.5, 0.75...)
                })
                nombres_dia.append(p["nombre"])

            # Totales resultantes con el factor aplicado
            tk = sum(x["kcal"] for x in dia_actual)
            tp = sum(x["p"] for x in dia_actual)
            tc = sum(x["c"] for x in dia_actual)
            tl = sum(x["l"] for x in dia_actual)
            
            # Cálculo de error relativo total (Kcal + Proteína + Carbo + Grasa)
            error = (abs(tk-get_obj)/get_obj) + \
                    (abs(tp-p_obj)/p_obj) + \
                    (abs(tc-c_obj)/c_obj) + \
                    (abs(tl-l_obj)/l_obj)
            
            # VARIEDAD: Penalización por repetir platos de días anteriores
            # Si el plato está en los últimos 12 platos servidos, subimos el error.
            if any(n in historial_global[-12:] for n in nombres_dia):
                # Si estamos en aprietos (muchos intentos), bajamos la penalización
                error += 0.4 if i < 1000 else 0.1

            # Guardamos si es el mejor intento hasta ahora
            if error < min_error:
                min_error = error
                best_day = (dia_actual, (tk, tp, tc, tl), nombres_dia)
            
            # UMBRAL DE ÉXITO: 
            # Si el error es menor al 6%, lo damos por bueno y cortamos el bucle.
            # Si ya intentamos mucho, aceptamos un error del 12%.
            umbral_corte = 0.06 if i < 2000 else 0.12
            if error < umbral_corte:
                break
                
        except Exception:
            continue

    # Si logramos armar un día, actualizamos el historial y devolvemos los datos
    if best_day:
        # Solo agregamos al historial si el día es definitivo
        historial_global.extend(best_day[2])
        return best_day[0], best_day[1]
    
    return None, (0,0,0,0)
