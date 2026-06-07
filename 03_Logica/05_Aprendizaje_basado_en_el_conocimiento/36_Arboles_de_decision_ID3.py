import math
from collections import Counter



class ArbolDecisionID3:
    """
    Implementacion del algoritmo ID3 para aprendizaje inductivo.
    Construye un arbol de decision basado en la Entropia y la Ganancia de Informacion.
    """
    def __init__(self):
        self.arbol = None



    def calcular_entropia(self, datos, atributo_objetivo):
        """
        Calcula la entropia de Shannon para un conjunto de datos.
        Formula: - Sumatoria( p * log2(p) )
        """
        valores_objetivo = [fila[atributo_objetivo] for fila in datos]
        frecuencias = Counter(valores_objetivo)
        total = len(datos)
        entropia = 0.0
        for cuenta in frecuencias.values():
            probabilidad = cuenta / total
            entropia -= probabilidad * math.log2(probabilidad) 
        return entropia



    def calcular_ganancia(self, datos, atributo, atributo_objetivo):
        """
        Calcula la Ganancia de Informacion al dividir los datos por un atributo.
        """
        # 1. Calcular la entropia del conjunto completo antes de dividir
        entropia_total = self.calcular_entropia(datos, atributo_objetivo)
        

        # 2. Calcular la entropia despues de dividir por el atributo
        valores_atributo = [fila[atributo] for fila in datos]
        frecuencias = Counter(valores_atributo)
        total = len(datos)
        entropia_subconjuntos = 0.0
        for valor, cuenta in frecuencias.items():
            # Filtramos los datos que tienen este valor especifico
            subconjunto = [fila for fila in datos if fila[atributo] == valor]
            probabilidad = cuenta / total
            # Sumamos la entropia ponderada de este subconjunto
            entropia_subconjuntos += probabilidad * self.calcular_entropia(subconjunto, atributo_objetivo)    


        # 3. La ganancia es la reduccion del caos
        return entropia_total - entropia_subconjuntos



    def construir_id3(self, datos, atributos, atributo_objetivo):
        """
        Funcion recursiva que construye el arbol de decision.
        """
        valores_objetivo = [fila[atributo_objetivo] for fila in datos]
        

        # CASO BASE 1: Si todos los ejemplos pertenecen a la misma clase, retornar esa clase
        if len(set(valores_objetivo)) == 1:
            return valores_objetivo[0]


        # CASO BASE 2: Si no quedan atributos para evaluar, retornar la clase mas comun
        if not atributos:
            clase_mayoritaria = Counter(valores_objetivo).most_common(1)[0][0]
            return clase_mayoritaria


        # PASO INDUCTIVO: Elegir el mejor atributo basado en la Ganancia de Informacion
        ganancias = {attr: self.calcular_ganancia(datos, attr, atributo_objetivo) for attr in atributos}
        mejor_atributo = max(ganancias, key=ganancias.get)
        

        # Inicializar el nodo del arbol con el mejor atributo
        arbol = {mejor_atributo: {}}
        

        # Remover el atributo elegido de la lista para las siguientes iteraciones
        atributos_restantes = [a for a in atributos if a != mejor_atributo]
        

        # Obtener los valores posibles del mejor atributo en el conjunto actual
        valores_posibles = set([fila[mejor_atributo] for fila in datos])
        

        # Crear una rama para cada valor posible
        for valor in valores_posibles:
            subconjunto = [fila for fila in datos if fila[mejor_atributo] == valor]
            # CASO BASE 3: Si el subconjunto esta vacio, asignar la clase mas comun del nodo padre
            if not subconjunto:
                clase_mayoritaria = Counter(valores_objetivo).most_common(1)[0][0]
                arbol[mejor_atributo][valor] = clase_mayoritaria
            else:
                # Llamada recursiva para construir el sub-arbol de esta rama
                arbol[mejor_atributo][valor] = self.construir_id3(subconjunto, atributos_restantes, atributo_objetivo)           
        return arbol



    def entrenar(self, datos, atributos, atributo_objetivo):
        print("Iniciando induccion del Arbol de Decision (ID3)...")
        self.arbol = self.construir_id3(datos, atributos, atributo_objetivo)
        print("Entrenamiento completado.")



    def clasificar(self, arbol_actual, instancia):
        """
        Navega por el arbol de decision generado para clasificar una nueva instancia.
        """
        # Si el nodo no es un diccionario, significa que llegamos a una hoja (la conclusion)
        if not isinstance(arbol_actual, dict):
            return arbol_actual


        # Extraemos la pregunta actual (el atributo raiz de este sub-arbol)
        atributo_pregunta = list(arbol_actual.keys())[0]
        valor_instancia = instancia.get(atributo_pregunta)
        

        # Obtenemos la siguiente rama basada en el valor de la instancia
        siguiente_rama = arbol_actual[atributo_pregunta].get(valor_instancia)
        

        if siguiente_rama is None:
            return "Indeterminado (Valor no visto en entrenamiento)"  
        # Llamada recursiva para seguir bajando por el arbol
        return self.clasificar(siguiente_rama, instancia)


    def imprimir_arbol(self, arbol_actual, nivel=0):
        """Imprime el arbol en formato de texto anidado."""
        if not isinstance(arbol_actual, dict):
            print(f" -> Conclusion: {arbol_actual}")
            return
        atributo = list(arbol_actual.keys())[0]
        sangria = "    " * nivel
        

        for valor, sub_arbol in arbol_actual[atributo].items():
            print(f"{sangria}Si [{atributo}] es '{valor}':", end="")
            if not isinstance(sub_arbol, dict):
                print(f" -> Conclusion: {sub_arbol}")
            else:
                print()
                self.imprimir_arbol(sub_arbol, nivel + 1)



# DEMOSTRACION: PREDICCION DE JUEGO DE TENIS
if __name__ == "__main__":
    # Base de datos historica (diccionarios para facilitar la lectura por clave)
    base_de_datos = [
        {'Clima': 'Soleado', 'Temp': 'Calor', 'Humedad': 'Alta', 'Viento': 'Debil', 'Jugar': 'No'},
        {'Clima': 'Soleado', 'Temp': 'Calor', 'Humedad': 'Alta', 'Viento': 'Fuerte', 'Jugar': 'No'},
        {'Clima': 'Nublado', 'Temp': 'Calor', 'Humedad': 'Alta', 'Viento': 'Debil', 'Jugar': 'Si'},
        {'Clima': 'Lluvia', 'Temp': 'Suave', 'Humedad': 'Alta', 'Viento': 'Debil', 'Jugar': 'Si'},
        {'Clima': 'Lluvia', 'Temp': 'Frio', 'Humedad': 'Normal', 'Viento': 'Debil', 'Jugar': 'Si'},
        {'Clima': 'Lluvia', 'Temp': 'Frio', 'Humedad': 'Normal', 'Viento': 'Fuerte', 'Jugar': 'No'},
        {'Clima': 'Nublado', 'Temp': 'Frio', 'Humedad': 'Normal', 'Viento': 'Fuerte', 'Jugar': 'Si'},
        {'Clima': 'Soleado', 'Temp': 'Suave', 'Humedad': 'Alta', 'Viento': 'Debil', 'Jugar': 'No'},
        {'Clima': 'Soleado', 'Temp': 'Frio', 'Humedad': 'Normal', 'Viento': 'Debil', 'Jugar': 'Si'},
        {'Clima': 'Lluvia', 'Temp': 'Suave', 'Humedad': 'Normal', 'Viento': 'Debil', 'Jugar': 'Si'},
        {'Clima': 'Soleado', 'Temp': 'Suave', 'Humedad': 'Normal', 'Viento': 'Fuerte', 'Jugar': 'Si'},
        {'Clima': 'Nublado', 'Temp': 'Suave', 'Humedad': 'Alta', 'Viento': 'Fuerte', 'Jugar': 'Si'},
        {'Clima': 'Nublado', 'Temp': 'Calor', 'Humedad': 'Normal', 'Viento': 'Debil', 'Jugar': 'Si'},
        {'Clima': 'Lluvia', 'Temp': 'Suave', 'Humedad': 'Alta', 'Viento': 'Fuerte', 'Jugar': 'No'}
    ]
    atributos_disponibles = ['Clima', 'Temp', 'Humedad', 'Viento']
    atributo_meta = 'Jugar'
    


    # 1. Instanciar y entrenar el modelo
    modelo_id3 = ArbolDecisionID3()
    modelo_id3.entrenar(base_de_datos, atributos_disponibles, atributo_meta)
    


    # 2. Visualizar el conocimiento inducido
    print("\nESTRUCTURA DEL ARBOL DE DECISION INDUCIDO:")
    modelo_id3.imprimir_arbol(modelo_id3.arbol)
    


    # 3. Poner a prueba el modelo con datos nuevos (Inferencia)
    print("\nCLASIFICANDO NUEVAS INSTANCIAS:")
    dia_nuevo_1 = {'Clima': 'Soleado', 'Temp': 'Frio', 'Humedad': 'Alta', 'Viento': 'Fuerte'}
    dia_nuevo_2 = {'Clima': 'Lluvia', 'Temp': 'Calor', 'Humedad': 'Alta', 'Viento': 'Debil'}
    prediccion_1 = modelo_id3.clasificar(modelo_id3.arbol, dia_nuevo_1)
    prediccion_2 = modelo_id3.clasificar(modelo_id3.arbol, dia_nuevo_2) 
    print(f"Evaluando Dia 1 {dia_nuevo_1}")
    print(f" -> Prediccion: Jugar = {prediccion_1}\n")
    print(f"Evaluando Dia 2 {dia_nuevo_2}")
    print(f" -> Prediccion: Jugar = {prediccion_2}")