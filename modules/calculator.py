def calcular_metricas(sexo, talla, peso_act, edad, pi_real, af_val, p_pro, p_cho, p_lip):
    # Cálculo de TMB (Mifflin-St Jeor)
    tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
    
    # Cálculo de GET
    get = tmb * af_val
    
    # Cálculo de IMC
    imc = peso_act / ((talla/100)**2)
    
    # Gramos de macros
    obj_p = (get * p_pro / 400)
    obj_c = (get * p_cho / 400)
    obj_l = (get * p_lip / 900)
    
    return get, imc, obj_p, obj_c, obj_l
