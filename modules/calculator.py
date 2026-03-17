# modules/calculator.py

def calcular_metricas(sexo, talla, peso_act, edad, pi_real, af_val, p_pro, p_cho, p_lip):
    """
    Calcula TMB, GET, IMC y los gramos objetivo de cada macronutriente.
    """
    # 1. Cálculo de TMB (Fórmula de Mifflin-St Jeor)
    # Es la base calórica según peso objetivo, talla y edad
    tmb = (10 * pi_real) + (6.25 * talla) - (5 * edad) + (5 if sexo == "Masculino" else -161)
    
    # 2. Cálculo de GET (Gasto Energético Total)
    # Aplicamos el factor de actividad física
    get = tmb * af_val
    
    # 3. Cálculo de IMC (Índice de Masa Corporal)
    # Basado en el peso actual del paciente
    imc = peso_act / ((talla/100)**2)
    
    # 4. Cálculo de Gramos Objetivo por Macronutriente
    # p_pro, p_cho, p_lip vienen como números enteros (ej: 25, 50, 25)
    
    # Proteínas: 4 kcal por gramo
    obj_p = (get * (p_pro / 100)) / 4
    
    # Carbohidratos: 4 kcal por gramo
    obj_c = (get * (p_cho / 100)) / 4
    
    # Lípidos (Grasas): 9 kcal por gramo
    obj_l = (get * (p_lip / 100)) / 9
    
    return get, imc, obj_p, obj_c, obj_l
