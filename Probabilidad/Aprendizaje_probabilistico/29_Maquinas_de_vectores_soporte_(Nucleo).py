import math

print("=== SVM CON TRUCO DE KERNEL (NÚCLEO) ===\n")

# --- 1. DEFINICIÓN DE KERNELS ---

def kernel_lineal(x1, x2):
    """Kernel estándar: producto punto."""
    return sum(a * b for a, b in zip(x1, x2))

def kernel_rbf(x1, x2, gamma=0.1):
    """Kernel RBF (Gaussiano): permite fronteras circulares/curvas."""
    dist_sq = sum((a - b) ** 2 for a, b in zip(x1, x2))
    return math.exp(-gamma * dist_sq)

# --- 2. CLASE SVM SIMPLIFICADA (Descenso de Graduante Pegaso) ---

class SVM_Kernel:
    def __init__(self, kernel_func, lambda_param=0.01):
        self.kernel = kernel_func
        self.lambda_param = lambda_param
        self.alpha = [] # Pesos para cada punto de entrenamiento
        self.X = []
        self.y = []

    def entrenar(self, X, y, iteraciones=100):
        self.X = X
        self.y = y
        self.alpha = [0.0] * len(X)
        
        for t in range(1, iteraciones + 1):
            for i in range(len(X)):
                # Calculamos la predicción usando el Kernel
                prediccion = sum(
                    self.alpha[j] * self.y[j] * self.kernel(self.X[j], self.X[i])
                    for j in range(len(X))
                )
                
                # Condición de margen (Hinge Loss)
                if self.y[i] * prediccion < 1:
                    self.alpha[i] += 1 # Actualizamos si hay error o poco margen

    def predecir(self, x_nuevo):
        puntuacion = sum(
            self.alpha[j] * self.y[j] * self.kernel(self.X[j], x_nuevo)
            for j in range(len(self.X))
        )
        return 1 if puntuacion >= 0 else -1

# --- 3. DATOS DE PRUEBA (2D) ---
# X: [Característica 1, Característica 2], y: [Clase 1 o -1]
X_train = [[1, 2], [2, 3], [3, 3], [10, 11], [11, 12], [12, 12]]
y_train = [-1, -1, -1, 1, 1, 1]

# --- 4. EJECUCIÓN ---

# Probamos con Kernel Lineal
svm = SVM_Kernel(kernel_func=kernel_rbf) # Cambia a kernel_lineal si prefieres
svm.entrenar(X_train, y_train)

# Intentamos clasificar un punto nuevo
punto_test = [9, 9]
resultado = svm.predecir(punto_test)

print(f"Punto a evaluar: {punto_test}")
print(f"Resultado de la clasificación: {'Positivo (1)' if resultado == 1 else 'Negativo (-1)'}")


print("\n=== ANÁLISIS TÉCNICO ===")
print("1. El SVM no guarda una pendiente 'w', guarda los puntos clave (Vectores de Soporte).")
print("2. El Truco del Kernel permite calcular la similitud en altas dimensiones")
print("   sin tener que transformar los datos físicamente, ahorrando memoria.")