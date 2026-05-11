import random

print("=== INFERENCIA APROXIMADA: MUESTREO DE MONTE CARLO ===\n")

# 1. Definimos una Red Bayesiana sencilla: Clima
# Nublado -> Lluvia
# Nublado -> Aspersor
def generar_muestra_directa():
    """
    Genera UN 'universo paralelo' simulando la red probabilística de arriba hacia abajo.
    Retorna un diccionario con el estado de las 3 variables.
    """
    # 1. Nodo Padre: Nublado (P = 0.5)
    nublado = random.random() < 0.5 
    
    # 2. Nodo Hijo: Lluvia (Depende de Nublado)
    if nublado:
        lluvia = random.random() < 0.80 # 80% de prob de lluvia si está nublado
    else:
        lluvia = random.random() < 0.20 # 20% de prob de lluvia si está despejado
        
    # 3. Nodo Hijo: Aspersor (Depende de Nublado)
    if nublado:
        aspersor = random.random() < 0.10 # 10% de prob de aspersor si está nublado (casi no se riega)
    else:
        aspersor = random.random() < 0.50 # 50% de prob de aspersor si está despejado
        
    return {"Nublado": nublado, "Lluvia": lluvia, "Aspersor": aspersor}

# --- PARTE 1: MUESTREO DIRECTO ---
print("--- 1. MUESTREO DIRECTO (A PRIORI) ---")
num_muestras_directas = 10000
contador_lluvia = 0

print(f"Simulando {num_muestras_directas} universos aleatorios...\n")
for _ in range(num_muestras_directas):
    muestra = generar_muestra_directa()
    if muestra["Lluvia"] == True:
        contador_lluvia += 1

prob_lluvia_general = contador_lluvia / num_muestras_directas
print(f"Probabilidad de Lluvia calculada por Muestreo Directo: {prob_lluvia_general * 100:.2f}%")
print("(Nota teórica: Al ser Nublado 50/50, la prob real es (0.5*0.8)+(0.5*0.2) = 50.00%. La simulación se acerca mucho).\n")


# --- PARTE 2: MUESTREO POR RECHAZO ---
print("-" * 50)
print("\n--- 2. MUESTREO POR RECHAZO ---")

def muestreo_por_rechazo(consulta, evidencia, num_simulaciones):
    """
    Calcula P(Consulta | Evidencia) usando Muestreo por Rechazo.
    """
    muestras_aceptadas = 0
    consulta_cumplida = 0
    muestras_rechazadas = 0
    
    for _ in range(num_simulaciones):
        muestra = generar_muestra_directa()
        
        # 1. VERIFICAR LA EVIDENCIA: ¿Este universo coincide con lo que ya sabemos?
        coincide = True
        for variable, valor in evidencia.items():
            if muestra[variable] != valor:
                coincide = False
                break
                
        # 2. RECHAZO: Si no coincide, tiramos este universo a la basura
        if not coincide:
            muestras_rechazadas += 1
            continue
            
        # 3. ACEPTACIÓN: Si la evidencia coincide, lo guardamos para nuestra estadística
        muestras_aceptadas += 1
        
        # 4. VERIFICAR CONSULTA: En este universo válido, ¿se cumplió lo que estamos buscando?
        if muestra[consulta[0]] == consulta[1]:
            consulta_cumplida += 1
            
    if muestras_aceptadas == 0:
        return 0.0, muestras_aceptadas, muestras_rechazadas
        
    prob_final = consulta_cumplida / muestras_aceptadas
    return prob_final, muestras_aceptadas, muestras_rechazadas


# Escenario: Queremos saber P(Nublado=True | Lluvia=False, Aspersor=True)
consulta_ia = ("Nublado", True)
evidencia_ia = {"Lluvia": False, "Aspersor": True}
total_simulaciones = 50000

print(f"Pregunta a la IA: ¿Cuál es la probabilidad de que esté Nublado")
print(f"SABIENDO QUE (Evidencia): NO está lloviendo y el aspersor SÍ está encendido?\n")

prob, aceptadas, rechazadas = muestreo_por_rechazo(consulta_ia, evidencia_ia, total_simulaciones)

print("=== RESULTADOS DEL ALGORITMO ===")
print(f"Total de simulaciones generadas: {total_simulaciones}")
print(f"Universos RECHAZADOS (No cumplían la evidencia): {rechazadas} (¡{(rechazadas/total_simulaciones)*100:.1f}% tirados a la basura!)")
print(f"Universos ACEPTADOS (Sirven para el cálculo): {aceptadas}")
print(f"-> P(Nublado | Lluvia=F, Aspersor=V) = {prob * 100:.2f}%\n")

print("Conclusión de la IA:")
print("- Como la evidencia es rara (que no llueva pero el aspersor esté prendido),")
print("  el Muestreo por Rechazo desperdició muchísimos cálculos.")
print("- A pesar de eso, entre las pocas muestras que sirvieron, concluye que es ")
print(f"  altamente probable ({prob*100:.2f}%) que el día esté Despejado (Nublado=False).")