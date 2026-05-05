import random

print("=== MODELO DE APRENDIZAJE BAYESIANO (Actualización de Creencia) ===\n")

class AprendizBayesiano:
    def __init__(self):
        # Nuestra creencia inicial (Prior): No sabemos nada.
        # Asumimos que la moneda tiene 1 cara por cada 1 cruz (50/50)
        self.exitos = 1  # Caras observadas (alfa)
        self.intentos = 1 # Cruces observadas (beta)

    def aprender(self, resultado):
        """Actualiza la creencia basada en un nuevo dato (Evidencia)"""
        if resultado == "Cara":
            self.exitos += 1
        else:
            self.intentos += 1

    def obtener_creencia(self):
        """Calcula la probabilidad estimada actual"""
        total = self.exitos + self.intentos
        probabilidad_cara = self.exitos / total
        # Calculamos la certidumbre basada en cuántos datos hemos visto
        confianza = "Baja" if total < 10 else "Media" if total < 50 else "Alta"
        return probabilidad_cara, confianza

# --- SIMULACIÓN ---

# Supongamos que tenemos una moneda TRUCADA que sale cara el 80% de las veces
PROB_REAL_OCULTA = 0.8
aprendiz = AprendizBayesiano()

print(f"Objetivo: La IA debe descubrir que la probabilidad real es {PROB_REAL_OCULTA * 100}%")
print("-" * 70)
print(f"{'Dato #':<10} | {'Resultado':<12} | {'Estimación IA':<15} | {'Confianza'}")
print("-" * 70)

for i in range(1, 101):
    # Generamos un dato del mundo real ruidoso
    resultado = "Cara" if random.random() < PROB_REAL_OCULTA else "Cruz"
    
    # La IA aprende del dato
    aprendiz.aprender(resultado)
    
    # Cada 10 datos mostramos qué ha aprendido
    if i % 10 == 0:
        estimacion, nivel = aprendiz.obtener_creencia()
        print(f"{i:<10} | {resultado:<12} | {estimacion*100:>13.2f}% | {nivel}")


print("\n=== ANÁLISIS DEL APRENDIZAJE ===")
print("1. Prior: La IA empezó creyendo que era 50/50 (ignorancia inicial).")
print("2. Verosimilitud: Cada lanzamiento es una evidencia que desafía o apoya la creencia.")
print("3. Posterior: Al final, tras 100 datos, la estimación está muy cerca del 80% real.")
print("La IA no 'memorizó' los datos, sino que actualizó su modelo interno del mundo.")