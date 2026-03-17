# modules/calculator.py

def calcular_metricas(sexo, talla, peso_act, edad, pi_real, af_val, p_pro, p_cho, p_lip):
    # 1. TMB (Mifflin-St Jeor) usando Peso Objetivo
    tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
    
    # 2. GET (Gasto Energético Total)
    get = tmb * af_val
    
    # 3. IMC (con Peso Actual)
    imc = peso_act / ((talla/100)**2)
    
    # 4. Gramos Objetivo
    # Proteínas: 4kcal/g | Carbohidratos: 4kcal/g | Grasas: 9kcal/g
    # Usamos max(1, ...) para evitar cualquier error de división posterior
    obj_p = max(1.0, (get * (p_pro / 100)) / 4)
    obj_c = max(1.0, (get * (p_cho / 100)) / 4)
    obj_l = max(1.0, (get * (p_lip / 100)) / 9)
    
    return get, imc, obj_p, obj_c, obj_l
