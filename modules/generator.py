# modules/generator.py
import random

def generar_dia_estricto(get_obj, p_obj, c_obj, l_obj, desayunos_pool, comidas_pool, historial_global, conteo_uso):
    """
    Generador por aproximación total diaria. 
    Busca que la SUMA del día sea la correcta, no cada comida por separado.
    """
    
    for intento in range(4000): # Más intentos para asegurar éxito
        dia = []
        nombres_dia = []
        
        # 1. Selección al azar de los 4 platos
        # Elegimos 2 del pool de desayunos/meriendas y 2 de comidas/cenas
        d1 = random.choice(desayunos_pool)
        a1 = random.choice(comidas_pool)
        m1 = random.choice(desayunos_pool)
        c1 = random.choice(comidas_pool)
        
        platos_seleccionados = [d1, a1, m1, c1]
        
        # 2. Aplicamos un factor de porción inicial basado en el GET total
        # Calculamos cuántas kcal suman los 4 platos base
        kcal_base_total = sum(p['kcal'] for p in platos_seleccionados)
        factor_ajuste = get_obj / kcal_base_total
        
        # Limitamos el factor para que no sea una porción ridícula (ej: x0.1 o x5)
        if factor_ajuste < 0.5: factor_ajuste = 0.5
        if factor_ajuste > 2.0: factor_ajuste = 2.0
        
        # 3. Construimos el día con ese factor
        for p_base in platos_seleccionados:
            dia.append({
                "nom": p_base["nombre"],
                "kcal": p_base["kcal"] * factor_ajuste,
                "p": p_base["p"] * factor_ajuste,
                "c": p_base["c"] * factor_ajuste,
                "l": p_base["l"] * factor_ajuste,
                "factor": round(factor_ajuste * 4) / 4 # Redondeo nutricional
            })
            nombres_dia.append(p_base["nombre"])
            
        # 4. Totales del día
        tk = sum(x["kcal"] for x in dia)
        tp = sum(x["p"] for x in dia)
        tc = sum(x["c"] for x in dia)
        tl = sum(x["l"] for x in dia)
        
        # 5. Tolerancia evolutiva (Margen de error)
        # Empezamos en 15% y subimos hasta 35% si es muy difícil
        tol = 0.15 + (intento // 800) * 0.05
        
        def check(real, obj, t):
            return abs(real - obj) / obj <= t if obj > 0 else True

        # Solo validamos el TOTAL DIARIO
        if all([check(tk, get_obj, tol), check(tp, p_obj, tol), check(tc, c_obj, tol), check(tl, l_obj, tol)]):
            # Filtro de variedad: si ya se repitió mucho, intentamos de nuevo 
            # (pero solo si estamos en los primeros intentos)
            if intento < 1000 and any(n in historial_global[-8:] for n in nombres_dia):
                continue
                
            historial_global.extend(nombres_dia)
            return dia, (tk, tp, tc, tl)
            
    return None, (0, 0, 0, 0)
