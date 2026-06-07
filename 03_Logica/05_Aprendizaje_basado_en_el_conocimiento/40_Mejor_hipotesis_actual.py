class MotorMejorHipotesisActual:
    """
    Motor de aprendizaje inductivo que mantiene una unica hipotesis
    y la ajusta dinamicamente mediante generalizacion y especializacion.
    """
    def __init__(self, dominios):
        # Dominios define los valores posibles para cada atributo
        self.dominios = dominios



    def predecir(self, hipotesis, ejemplo):
        """Evalua si un ejemplo cumple con la hipotesis actual."""
        for h, e in zip(hipotesis, ejemplo):
            if h != '?' and h != e:
                return False
        return True



    def generalizar(self, hipotesis, ejemplo_positivo):
        """
        Ante un Falso Negativo, relaja la hipotesis para que cubra el ejemplo.
        """
        nueva_h = list(hipotesis)
        for i in range(len(nueva_h)):
            if nueva_h[i] != '?' and nueva_h[i] != ejemplo_positivo[i]:
                nueva_h[i] = '?'
        return [nueva_h] # Retorna como lista para la estructura de ramificacion



    def especializar(self, hipotesis, ejemplo_negativo):
        """
        Ante un Falso Positivo, restringe la hipotesis evaluando alternativas
        que excluyan explicitamente el rasgo del ejemplo negativo.
        """
        nuevas_hipotesis = []
        for i in range(len(hipotesis)):
            if hipotesis[i] == '?':
                # Probamos todos los valores posibles de este dominio
                for valor in self.dominios[i]:
                    # Excluimos el valor que causo el Falso Positivo
                    if valor != ejemplo_negativo[i]:
                        nueva_h = list(hipotesis)
                        nueva_h[i] = valor
                        nuevas_hipotesis.append(nueva_h)
        return nuevas_hipotesis


    def entrenar(self, datos, etiquetas):
        """
        Algoritmo de busqueda en profundidad (DFS) con Backtracking.
        """
        print("Iniciando Búsqueda de la Mejor Hipótesis Actual...")
        # Pila de exploracion: guarda tuplas de (hipotesis_actual, indice_ejemplo)
        # Partimos de la hipotesis mas general posible
        hipotesis_inicial = ['?'] * len(self.dominios)
        pila = [(hipotesis_inicial, 0)]
        visitados = set() # Historial para evitar ciclos infinitos



        while pila:
            hipotesis, idx = pila.pop()
            

            # Congelamos la lista a tupla para poder guardarla en un Set
            hash_estado = tuple(hipotesis)
            if hash_estado in visitados:
                continue
            visitados.add(hash_estado)


            # Condicion de exito: Logramos procesar todos los ejemplos sin errores
            if idx == len(datos):
                print(f"\n[!] EXITO: La Mejor Hipotesis Actual es {hipotesis}")
                return hipotesis
            ejemplo = datos[idx]
            etiqueta_real = etiquetas[idx]
            prediccion_modelo = self.predecir(hipotesis, ejemplo)
            print(f"Paso {idx} | Hipotesis: {hipotesis} | Evalua: {ejemplo} -> Predice: {prediccion_modelo} (Real: {etiqueta_real})")



            # 1. ACIERTO: La hipotesis es consistente con este ejemplo
            if prediccion_modelo == etiqueta_real:
                pila.append((hipotesis, idx + 1))



            # 2. FALSO NEGATIVO: Se requiere Generalizacion
            elif prediccion_modelo == False and etiqueta_real == True:
                print(f"    -> FALSO NEGATIVO. Generalizando hipotesis...")
                ramas = self.generalizar(hipotesis, ejemplo)
                for nueva_h in ramas:
                    # Al modificar la hipotesis, reiniciamos la validacion desde cero (idx=0)
                    pila.append((nueva_h, 0))



            # 3. FALSO POSITIVO: Se requiere Especializacion
            elif prediccion_modelo == True and etiqueta_real == False:
                print(f"    -> FALSO POSITIVO. Creando ramas de especializacion...")
                ramas = self.especializar(hipotesis, ejemplo)
                for nueva_h in ramas:
                    # Al modificar la hipotesis, reiniciamos la validacion desde cero (idx=0)
                    pila.append((nueva_h, 0))
        print("\nFALLO: El lenguaje de hipotesis no puede representar este concepto sin contradicciones.")
        return None



# DEMOSTRACION DEL ALGORITMO
if __name__ == "__main__":
    # Atributos: [Tamaño, Color, Forma]
    espacio_dominios = {
        0: ['Grande', 'Pequeño'],
        1: ['Rojo', 'Azul'],
        2: ['Circulo', 'Triangulo']
    }
    


    # Objetivo oculto a descubrir: "Cualquier objeto Rojo" -> ['?', 'Rojo', '?']
    X_entrenamiento = [
        ['Pequeño', 'Azul', 'Triangulo'], # 0. Negativo
        ['Grande', 'Rojo', 'Circulo'],    # 1. Positivo
        ['Pequeño', 'Rojo', 'Triangulo'], # 2. Positivo
        ['Grande', 'Azul', 'Circulo']     # 3. Negativo
    ]
    y_entrenamiento = [False, True, True, False]
    motor = MotorMejorHipotesisActual(espacio_dominios)
    motor.entrenar(X_entrenamiento, y_entrenamiento)