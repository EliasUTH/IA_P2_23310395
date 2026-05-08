import math
print("=== PARTE 1: PROBABILIDAD CONDICIONADA P(A|B) ===\n")
# La probabilidad condicionada es la probabilidad de que ocurra un evento A, 
# sabiendo que ya ocurrió un evento B. P(A|B) = P(A y B) / P(B)

# Imaginemos el dataset de un vehículo autónomo en sus últimos 20 viajes
# Cada registro es un viaje con (Condición del Clima, Hubo Tráfico)
historial_viajes = [
    ("Lluvia", "Trafico"), ("Despejado", "Sin_Trafico"), ("Lluvia", "Trafico"),
    ("Nublado", "Sin_Trafico"), ("Lluvia", "Sin_Trafico"), ("Despejado", "Sin_Trafico"),
    ("Lluvia", "Trafico"), ("Despejado", "Trafico"), ("Nublado", "Trafico"),
    ("Lluvia", "Trafico")
]

# Queremos que la IA responda: ¿Cuál es la probabilidad de que haya Tráfico DADO QUE está lloviendo? P(Trafico | Lluvia)

# 1. Contar cuántas veces llovió en total P(B)
viajes_con_lluvia = [viaje for viaje in historial_viajes if viaje[0] == "Lluvia"]
total_lluvia = len(viajes_con_lluvia)

# 2. Contar cuántas veces llovió Y además hubo tráfico P(A y B)
lluvia_y_trafico = [viaje for viaje in viajes_con_lluvia if viaje[1] == "Trafico"]
total_lluvia_y_trafico = len(lluvia_y_trafico)

# 3. Calcular Probabilidad Condicionada
prob_trafico_dado_lluvia = total_lluvia_y_trafico / total_lluvia

print(f"Total de viajes registrados: {len(historial_viajes)}")
print(f"Viajes con lluvia: {total_lluvia}")
print(f"Viajes con lluvia Y tráfico: {total_lluvia_y_trafico}")
print(f"-> P(Tráfico | Lluvia) = {prob_trafico_dado_lluvia * 100}%\n")
print("Conclusión de la IA: 'Si mis sensores detectan lluvia, estoy 80% segura de que encontraré tráfico.'\n")

print("-" * 50)

print("\n=== PARTE 2: PROBABILIDAD NORMAL (GAUSSIANA) ===\n")
# En IA, no todos los datos son discretos ("Lluvia" o "Soleado"). 
# A veces tenemos datos continuos (ej. Temperatura, Velocidad).
# Para calcular la probabilidad de un dato continuo, usamos la Distribución Normal (Campana de Gauss).

def probabilidad_normal(x, media, desviacion_estandar):
    """
    Calcula la Densidad de Probabilidad de un valor 'x' en una distribución normal.
    """
    # Fórmula de la función de densidad de probabilidad (PDF) Gaussiana
    exponente = math.exp(-((x - media)**2) / (2 * desviacion_estandar**2))
    base = 1 / (desviacion_estandar * math.sqrt(2 * math.pi))
    return base * exponente

# Escenario: Un sistema de IA médica analiza el ritmo cardíaco de un paciente en reposo.
# Históricamente, el ritmo cardíaco de una persona sana sigue una distribución normal:
media_latidos = 70.0        # El promedio normal es de 70 latidos por minuto
desviacion_latidos = 10.0   # La mayoría de la gente varía unos 10 latidos arriba o abajo

paciente_1 = 72.0 # Paciente con 72 latidos por minuto
paciente_2 = 115.0 # Paciente con 115 latidos por minuto

# Calculamos qué tan "normales" (probables) son estos valores según la campana de Gauss
prob_paciente_1 = probabilidad_normal(paciente_1, media_latidos, desviacion_latidos)
prob_paciente_2 = probabilidad_normal(paciente_2, media_latidos, desviacion_latidos)

print(f"Estadísticas de pacientes sanos: Promedio = {media_latidos} lpm, Desviación = ±{desviacion_latidos} lpm\n")

print(f"Paciente 1 ({paciente_1} lpm) -> Densidad de Probabilidad Gaussiana: {prob_paciente_1:.5f}")
print(f"Paciente 2 ({paciente_2} lpm) -> Densidad de Probabilidad Gaussiana: {prob_paciente_2:.5f}\n")

print("Conclusión de la IA:")
print(f"- El Paciente 1 tiene un valor altamente probable (está justo en el pico de la campana normal).")
print(f"- El Paciente 2 tiene un valor matemáticamente casi imposible (anomalía), necesita atención médica.")