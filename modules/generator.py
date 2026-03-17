import random
from modules.config import LIMITES_SEMANALES

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    for _ in range(500): 
        dia = []
        nombres_dia = []
        dist = [get_obj * 0.20, get_obj * 0.35, get_obj * 0.15, get_obj * 0.30]
        
        for j in range(4):
            pool = desayunos_pool if j in [0, 2] else comidas_pool
            pool_variedad = [p for p in pool if p["nombre"] not in historial_global[-8:]]
            seleccion = pool_variedad if pool_variedad else pool
            
            plato_base = random.choice(seleccion)
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
        
        tk, tp, tc, tl = sum(x["kcal"] for x in dia), sum(x["p"] for x in dia), sum(x["c"] for x in dia), sum(x["l"] for x in dia)
        
        def check(r, o): return abs(r - o) / o <= 0.07 if o > 0 else True
        if all([check(tk, get_obj), check(tp, p_obj), check(tc, c_obj), check(tl, l_obj)]):
            historial_global.extend(nombres_dia)
            return dia, (tk, tp, tc, tl)
            
    return None, (0, 0, 0, 0)
