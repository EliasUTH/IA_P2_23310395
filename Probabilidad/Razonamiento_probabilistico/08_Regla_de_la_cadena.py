print("=== IA PROBABILÍSTICA: REGLA DE LA CADENA ===\n")

# ESCENARIO: Un asistente virtual (IA) predice si llegarás tarde al trabajo.
# Hay 3 eventos secuenciales: 
# A: ¿Llueve?
# B: ¿Hay tráfico? (Depende de si llueve)
# C: ¿Llegas tarde? (Depende de si hay tráfico Y de si llueve)

# 1. P(A): Probabilidad a priori del Clima
# Solo necesitamos saber la probabilidad de que llueva.
p_lluvia = {
    True: 0.20,  # 20% de probabilidad de que llueva hoy
    False: 0.80  # 80% de que esté despejado
}

# 2. P(B|A): Probabilidad de Tráfico DADO el Clima
# Diccionario: Clima -> Probabilidad de que haya tráfico
p_trafico_dado_clima = {
    True: 0.85,  # Si llueve (True), hay 85% de probabilidad de tráfico
    False: 0.30  # Si no llueve (False), solo hay 30% de tráfico por la hora pico
}

# 3. P(C|A, B): Probabilidad de Llegar Tarde DADO el Tráfico Y el Clima
# Diccionario: (Clima, Tráfico) -> Probabilidad de llegar tarde
p_tarde_dado_clima_y_trafico = {
    (True, True): 0.95,   # Llueve y hay tráfico: 95% seguro llegas tarde
    (True, False): 0.40,  # Llueve pero no hay tráfico (raro): 40% de llegar tarde (manejar lento)
    (False, True): 0.60,  # No llueve, pero hay tráfico: 60% de llegar tarde
    (False, False): 0.05  # Despejado y sin tráfico: 5% de llegar tarde (te quedaste dormido)
}

def regla_de_la_cadena(llueve, hay_trafico, llegas_tarde):
    """
    Calcula P(A, B, C) usando la Regla de la Cadena: P(A) * P(B|A) * P(C|A, B)
    """
    # Paso 1: P(A)
    prob_A = p_lluvia[llueve]
    
    # Paso 2: P(B|A)
    prob_B_dado_A = p_trafico_dado_clima[llueve] if hay_trafico else (1 - p_trafico_dado_clima[llueve])
    
    # Paso 3: P(C|A, B)
    prob_C_dado_A_y_B = p_tarde_dado_clima_y_trafico[(llueve, hay_trafico)] if llegas_tarde else (1 - p_tarde_dado_clima_y_trafico[(llueve, hay_trafico)])
    
    # REGLA DE LA CADENA: Multiplicamos toda la secuencia
    probabilidad_conjunta = prob_A * prob_B_dado_A * prob_C_dado_A_y_B
    
    return prob_A, prob_B_dado_A, prob_C_dado_A_y_B, probabilidad_conjunta

# --- SIMULACIÓN DEL ASISTENTE VIRTUAL ---

# Queremos calcular el peor escenario posible: 
# "Que hoy llueva, se haga tráfico y en consecuencia llegues tarde."
evento_A = True  # Llueve
evento_B = True  # Hay tráfico
evento_C = True  # Llegas tarde

pA, pB_A, pC_AB, resultado_final = regla_de_la_cadena(evento_A, evento_B, evento_C)

print("Calculando la probabilidad del peor escenario P(Llueve, Tráfico, Tarde)...\n")
print(f"1. P(Llueve): ............................ {pA * 100}%")
print(f"2. P(Tráfico | Llueve): .................. {pB_A * 100}%")
print(f"3. P(Tarde | Llueve, Tráfico): ........... {pC_AB * 100}%\n")

print("Aplicando Regla de la Cadena: P(A) * P(B|A) * P(C|A, B)")
print(f"Multiplicación: {pA} * {pB_A} * {pC_AB}")
print(f"-> Probabilidad Total (Conjunta) = {resultado_final * 100:.2f}%\n")

# Evaluamos un escenario contrastante: Que todo salga perfecto
# No llueve, no hay tráfico, no llegas tarde.
_, _, _, resultado_perfecto = regla_de_la_cadena(False, False, False)

print("Calculando la probabilidad del escenario perfecto P(No Llueve, No Tráfico, No Tarde)...")
print(f"-> Probabilidad Total (Conjunta) = {resultado_perfecto * 100:.2f}%\n")


if resultado_final > resultado_perfecto:
    print("IA: Te recomiendo salir temprano hoy, la probabilidad del caos es mayor a la de un viaje perfecto.")
else:
    print("IA: Las condiciones son favorables hoy, es muy probable que tengas un viaje tranquilo.")