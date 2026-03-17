# modules/calculator.py

def calcular_metricas(sexo, talla, peso_act, edad, pi_real, af_val, p_pro, p_cho, p_lip):
    # 1. TMB (Mifflin-St Jeor)
    tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
    
    # 2. GET (Gasto Energético Total)
    get = tmb * af_val
    
    # 3. IMC
    imc = peso_act / ((talla/100)**2)
    
    # 4. Cálculo de Gramos Objetivo
    # Multiplicamos GET por el % y dividimos por (100 * kcal por gramo)
    # Proteínas: 4 kcal/g | Carbohidratos: 4 kcal/g | Lípidos: 9 kcal/g
    
    obj_p = (get * (p_pro / 100)) / 4
    obj_c = (get * (p_cho / 100)) / 4
    obj_l = (get * (p_lip / 100)) / 9
    
    return get, imc, obj_p, obj_c, obj_l
