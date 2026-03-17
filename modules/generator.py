# modules/generator.py
import random

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    """
    Motor de generación ultra-flexible con tolerancia evolutiva.
    Si no encuentra la combinación ideal, relaja los parámetros para asegurar el resultado.
    """
    
    # Intentaremos hasta 3000 veces para agotar todas las combinaciones posibles
    for intento in range(3000): 
        dia = []
        nombres_dia = []
        
        # Distribución de energía por comida (Des 20%, Alm 35%, Mer 15%, Cen 30%)
        dist = [get_obj * 0.20, get_obj * 0.35, get_obj * 0.15, get_obj * 0.30]
        
        # --- LÓGICA DE TOLERANCIA EVOLUTIVA ---
        # Empezamos en 12% de margen. Cada 500 intentos fallidos, sumamos 5% de margen.
        # Esto asegura que si el objetivo es difícil, el motor no se rinda.
        tolerancia_actual = 0.12 + (intento // 500) * 0.05
        
        for j in range(4):
            # 0 y 2 son Desayuno/Merienda | 1 y 3 son Almuerzo/Cena
            pool = desayunos_pool if j in [0, 2] else comidas_pool
            
            # Filtro de Variedad: Evita repetir los últimos 8 platos del historial
            pool_variedad = [p for p in pool if p["nombre"] not in historial_global[-8:]]
            seleccion = pool_variedad if pool_variedad else pool
            
            # Elegimos un plato al azar del pool filtrado
            plato_base = random.choice(seleccion)
            
            # Calculamos el factor de porción (redondeado a 0.25 para que sea realista: media porción, una y cuarto, etc.)
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
        
        # Sumamos los totales logrados en este intento
        tk = sum(x["kcal"] for x in dia)
        tp = sum(x["p"] for x in dia)
        tc = sum(x["c"] for x in dia)
        tl = sum(x["l"] for x in dia)
        
        # Función interna para chequear si el valor real está dentro del margen del objetivo
        def check(real, objetivo, tol): 
            if objetivo <= 0: return True
            return abs(real - objetivo) / objetivo <= tol
        
        # Verificamos los 4 pilares: Calorías, Proteínas, Carbohidratos y Lípidos
        if all([
            check(tk, get_obj, tolerancia_actual), 
            check(tp, p_obj, tolerancia_actual), 
            check(tc, c_obj, tolerancia_actual), 
            check(tl, l_obj, tolerancia_actual)
        ]):
            # Si pasa la prueba, guardamos los nombres en el historial y devolvemos el día
            historial_global.extend(nombres_dia)
            return dia, (tk, tp, tc, tl)
            
    # Si después de 3000 intentos no hubo caso, devolvemos None
    return None, (0, 0, 0, 0)
