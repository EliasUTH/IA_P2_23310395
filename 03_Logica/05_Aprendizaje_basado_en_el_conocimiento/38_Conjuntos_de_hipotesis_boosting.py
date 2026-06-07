import math
class ToconDeDecision:
    """
    Modelo debil (Weak Learner): Un arbol de decision de un solo nivel (Decision Stump).
    Solo puede hacer una pregunta sobre una caracteristica y un punto de corte.
    """
    def __init__(self):
        self.polaridad = 1
        self.indice_caracteristica = None
        self.umbral = None
        self.alfa = None # El poder de voto de este modelo en el conjunto final


    def predecir(self, X):
        n_muestras = len(X)
        predicciones = [1] * n_muestras
        


        for i in range(n_muestras):
            valor_caracteristica = X[i][self.indice_caracteristica]
            # La polaridad determina la direccion de la desigualdad
            if self.polaridad == 1:
                if valor_caracteristica < self.umbral:
                    predicciones[i] = -1
            else:
                if valor_caracteristica >= self.umbral:
                    predicciones[i] = -1         
        return predicciones


class AdaBoost:
    """
    Algoritmo de Boosting que combina multiples Tocones de Decision.
    """
    def __init__(self, n_estimadores=5):
        self.n_estimadores = n_estimadores
        self.modelos = []


    def entrenar(self, X, y):
        print("Iniciando entrenamiento AdaBoost...")
        n_muestras = len(X)
        n_caracteristicas = len(X[0])
        

        # 1. Inicializar los pesos de los datos equitativamente (w = 1/N)
        w = [1 / n_muestras] * n_muestras
        

        for m in range(self.n_estimadores):
            modelo = ToconDeDecision()
            min_error = float('inf')
            

            # Búsqueda del mejor 'Tocon' evaluando todas las caracteristicas y umbrales
            for i in range(n_caracteristicas):
                valores_caracteristica = [fila[i] for fila in X]
                umbrales_unicos = list(set(valores_caracteristica))
                

                for umbral in umbrales_unicos:
                    for polaridad in [1, -1]:
                        predicciones = [1] * n_muestras
                        for j in range(n_muestras):
                            if polaridad == 1:
                                if valores_caracteristica[j] < umbral:
                                    predicciones[j] = -1
                            else:
                                if valores_caracteristica[j] >= umbral:
                                    predicciones[j] = -1


                        # Calcular el error ponderado de esta division
                        error = sum(w[j] for j in range(n_muestras) if predicciones[j] != y[j])        
                        # Guardar la configuracion si es la mejor hasta ahora
                        if error < min_error:
                            min_error = error
                            modelo.polaridad = polaridad
                            modelo.umbral = umbral
                            modelo.indice_caracteristica = i



            # 2. Calcular la cantidad de influencia (Alfa) que tendra este modelo
            # Evitamos division por cero añadiendo un valor infimo (1e-10)
            modelo.alfa = 0.5 * math.log((1.0 - min_error) / (min_error + 1e-10))
            # Generar predicciones con el modelo recien entrenado
            predicciones_modelo = modelo.predecir(X)
            


            # 3. Actualizar los pesos de los datos
            for j in range(n_muestras):
                # Si prediccion_modelo == y[j], el exponente es negativo (el peso disminuye).
                # Si prediccion_modelo != y[j], el exponente es positivo (el peso aumenta).
                w[j] = w[j] * math.exp(-modelo.alfa * y[j] * predicciones_modelo[j])   
            # Normalizar los pesos para que sumen 1
            suma_w = sum(w)
            w = [peso / suma_w for peso in w]
            self.modelos.append(modelo)  
            print(f" - Modelo {m+1} entrenado. Error ponderado: {min_error:.4f} | Voto (Alfa): {modelo.alfa:.4f}")
            # Mostramos un resumen de que puntos tienen mas peso (los mas dificiles)
            indices_pesados = sorted(range(len(w)), key=lambda k: w[k], reverse=True)[:2]
            print(f"   -> Los datos mas dificiles (mayor peso) ahora son los indices: {indices_pesados}")
        print("Entrenamiento completado.")



    def predecir(self, X):
        n_muestras = len(X)
        predicciones_finales = [0.0] * n_muestras
        # El conjunto toma una decision mediante votacion ponderada
        for modelo in self.modelos:
            predicciones_modelo = modelo.predecir(X)
            for i in range(n_muestras):
                predicciones_finales[i] += modelo.alfa * predicciones_modelo[i]            
        # Retornamos el signo de la suma: 1 si es positivo, -1 si es negativo
        return [1 if p >= 0 else -1 for p in predicciones_finales]



# DEMOSTRACION: CLASIFICACION DE PACIENTES
if __name__ == "__main__":
    # Base de datos simulada
    # X: [Nivel de Glucosa, Presion Arterial]
    # y: 1 (Sano), -1 (Enfermo) - AdaBoost requiere clases -1 y 1 matematicamente
    X_entrenamiento = [
        [90,  60],  # 0: Sano
        [100, 70],  # 1: Sano
        [110, 80],  # 2: Sano
        [150, 65],  # 3: Enfermo (Glucosa alta)
        [95, 120],  # 4: Enfermo (Presion alta)
        [105, 115], # 5: Enfermo
        [115, 75],  # 6: Caso borde (Ficticiamente Sano)
        [110, 110]  # 7: Enfermo
    ]
    y_entrenamiento = [1, 1, 1, -1, -1, -1, 1, -1]
    


    # 1. Crear y entrenar el ensamble AdaBoost
    # Usaremos 3 tocónes de decision (3 iteraciones de correccion de errores)
    ensamble = AdaBoost(n_estimadores=3)
    ensamble.entrenar(X_entrenamiento, y_entrenamiento)
    


    # 2. Poner a prueba el conjunto de hipotesis
    print("\nEVALUACION DEL CONJUNTO DE HIPOTESIS:")

    


    # Evaluar los mismos datos para ver si el ensamble aprendio las excepciones
    predicciones = ensamble.predecir(X_entrenamiento)
    correctos = 0
    for i in range(len(y_entrenamiento)):
        estado_real = "Sano" if y_entrenamiento[i] == 1 else "Enfermo"
        estado_predicho = "Sano" if predicciones[i] == 1 else "Enfermo"
        resultado = "[OK]" if y_entrenamiento[i] == predicciones[i] else "[FALLO]"
        

        if y_entrenamiento[i] == predicciones[i]:
            correctos += 1   
        print(f"Paciente {i}: Real = {estado_real:<7} | Prediccion = {estado_predicho:<7} {resultado}")
        

    precision = (correctos / len(y_entrenamiento)) * 100
    print(f"\nPrecision total del conjunto: {precision:.1f}%")