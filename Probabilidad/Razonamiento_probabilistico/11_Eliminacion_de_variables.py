import itertools

print("=== MOTOR DE INFERENCIA: ELIMINACIÓN DE VARIABLES ===\n")

# --- 1. OPERACIONES FUNDAMENTALES DE LOS FACTORES ---

def restringir_evidencia(vars_f, tabla_f, evidencia):
    """ Filtra la tabla dejando solo las filas que coinciden con la evidencia y reduce su tamaño. """
    nuevas_vars = [v for v in vars_f if v not in evidencia]
    nueva_tabla = {}
    
    for tupla_valores, prob in tabla_f.items():
        dicc_valores = dict(zip(vars_f, tupla_valores))
        # Comprobar si la fila coincide con la evidencia que conocemos
        coincide = all(dicc_valores[e] == evidencia[e] for e in evidencia if e in dicc_valores)
        
        if coincide:
            nueva_tupla = tuple(dicc_valores[v] for v in nuevas_vars)
            nueva_tabla[nueva_tupla] = prob
            
    return nuevas_vars, nueva_tabla


def multiplicar_factores(vars_f1, tabla_f1, vars_f2, tabla_f2):
    """ Une dos factores matemáticamente (Producto Punto a Punto). """
    nuevas_vars = vars_f1 + [v for v in vars_f2 if v not in vars_f1]
    nueva_tabla = {}
    
    # Generar todas las combinaciones posibles de True/False para las nuevas variables
    for combinacion in itertools.product([True, False], repeat=len(nuevas_vars)):
        dicc_valores = dict(zip(nuevas_vars, combinacion))
        
        # Extraer las claves específicas para buscar en cada tabla original
        clave1 = tuple(dicc_valores[v] for v in vars_f1)
        clave2 = tuple(dicc_valores[v] for v in vars_f2)
        
        # Multiplicar las probabilidades
        if clave1 in tabla_f1 and clave2 in tabla_f2:
            nueva_tabla[combinacion] = tabla_f1[clave1] * tabla_f2[clave2]
            
    return nuevas_vars, nueva_tabla

def eliminar_variable(vars_f, tabla_f, variable_a_eliminar):
    """ Elimina una variable oculta sumando sus probabilidades (Marginalización). """
    if variable_a_eliminar not in vars_f:
        return vars_f, tabla_f
        
    idx_var = vars_f.index(variable_a_eliminar)
    nuevas_vars = [v for v in vars_f if v != variable_a_eliminar]
    nueva_tabla = {}
    
    for combinacion in itertools.product([True, False], repeat=len(nuevas_vars)):
        # Reconstruimos las claves originales para cuando la variable era True y False
        clave_true = list(combinacion)
        clave_true.insert(idx_var, True)
        
        clave_false = list(combinacion)
        clave_false.insert(idx_var, False)
        
        # SUMAMOS ambos mundos (esto "destruye" y elimina la variable de la ecuación)
        prob_sumada = tabla_f.get(tuple(clave_true), 0) + tabla_f.get(tuple(clave_false), 0)
        nueva_tabla[combinacion] = prob_sumada
        
    return nuevas_vars, nueva_tabla


# --- 2. DEFINIR LA RED BAYESIANA (Los Factores Iniciales) ---
# Usamos el mismo problema: Robo, Terremoto, Alarma, Juan y María

f_R = (['Robo'], {(True,): 0.001, (False,): 0.999})
f_T = (['Terremoto'], {(True,): 0.002, (False,): 0.998})

# (Robo, Terremoto, Alarma)
f_A = (['Robo', 'Terremoto', 'Alarma'], {
    (True, True, True): 0.95,   (True, True, False): 0.05,
    (True, False, True): 0.94,  (True, False, False): 0.06,
    (False, True, True): 0.29,  (False, True, False): 0.71,
    (False, False, True): 0.001,(False, False, False): 0.999
})

# (Alarma, Juan)
f_J = (['Alarma', 'Juan'], {
    (True, True): 0.90, (True, False): 0.10,
    (False, True): 0.05, (False, False): 0.95
})

# (Alarma, Maria)
f_M = (['Alarma', 'Maria'], {
    (True, True): 0.70, (True, False): 0.30,
    (False, True): 0.01, (False, False): 0.99
})

factores = [f_R, f_T, f_A, f_J, f_M]


# --- 3. EJECUTAR EL ALGORITMO ---
evidencia = {'Juan': True, 'Maria': True}
consulta = 'Robo'
orden_eliminacion = ['Terremoto', 'Alarma'] # Variables ocultas que no nos interesan

print(f"Consulta: ¿Probabilidad de {consulta}?")
print(f"Evidencia observada: {evidencia}")
print(f"Variables ocultas a eliminar: {orden_eliminacion}\n")

# Paso A: Aplicar la evidencia reduciendo las tablas
for i in range(len(factores)):
    factores[i] = restringir_evidencia(factores[i][0], factores[i][1], evidencia)
print("-> Paso 1: Evidencia aplicada. Las tablas de Juan y María se han encogido.")

# Paso B: Eliminar variables ocultas una por una
for var_oculta in orden_eliminacion:
    # 1. Encontrar todos los factores que mencionan la variable oculta
    factores_a_multiplicar = [f for f in factores if var_oculta in f[0]]
    factores = [f for f in factores if var_oculta not in f[0]] # Quitar de la lista principal
    
    # 2. Multiplicar esos factores entre sí
    factor_actual = factores_a_multiplicar[0]
    for f in factores_a_multiplicar[1:]:
        factor_actual = multiplicar_factores(factor_actual[0], factor_actual[1], f[0], f[1])
        
    # 3. Eliminar la variable del factor resultante (Sumar)
    factor_actual = eliminar_variable(factor_actual[0], factor_actual[1], var_oculta)
    
    # 4. Guardar el nuevo factor "limpio" en nuestra lista
    factores.append(factor_actual)
    print(f"-> Paso 2: Variable oculta '{var_oculta}' multiplicada y eliminada matemáticamente.")

# Paso C: Multiplicar todo lo que sobra (Debería quedar solo la variable de consulta 'Robo')
factor_final = factores[0]
for f in factores[1:]:
    factor_final = multiplicar_factores(factor_final[0], factor_final[1], f[0], f[1])

# Paso D: Normalización (Alpha)
vars_finales, tabla_final = factor_final
suma_total = sum(tabla_final.values())

print("\n=== RESULTADO DE LA ELIMINACIÓN DE VARIABLES ===")
for combinacion, prob_cruda in tabla_final.items():
    prob_normalizada = prob_cruda / suma_total
    es_robo = combinacion[0]
    print(f"P(Robo = {es_robo} | Juan=True, Maria=True) = {prob_normalizada * 100:.2f}%")