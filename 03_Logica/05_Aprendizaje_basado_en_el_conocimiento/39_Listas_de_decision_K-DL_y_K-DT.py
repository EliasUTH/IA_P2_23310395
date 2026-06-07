import itertools
from collections import Counter
class AprendizKDL:
    """
    Algoritmo inductivo para aprender Listas de Decision k (K-DL).
    Utiliza un enfoque de cobertura (Sequential Covering): encuentra una regla 
    pura, extrae los ejemplos cubiertos y repite el proceso sobre los restantes.
    """
    def __init__(self, k):
        self.k = k
        # Lista que almacenara tuplas (diccionario_condiciones, clase_predicha)
        self.lista_decision = []
        self.clase_por_defecto = None


    def _obtener_valores_unicos(self, datos, atributos):
        """Extrae los valores posibles para cada atributo en el dataset."""
        valores = {attr: set() for attr in atributos}
        for fila in datos:
            for attr in atributos:
                valores[attr].add(fila[attr])
        return valores


    def _generar_candidatos(self, valores_unicos):
        """
        Genera todas las conjunciones posibles de tamano 1 hasta k.
        Un candidato es un diccionario de condiciones, ej: {'Clima': 'Lluvia', 'Viento': 'Fuerte'}
        """
        candidatos = []
        pares_attr_val = []
        for attr, vals in valores_unicos.items():
            for val in vals:
                pares_attr_val.append((attr, val))


        # Iteramos desde tamaño 1 hasta el limite k establecido
        for i in range(1, self.k + 1):
            for combinacion in itertools.combinations(pares_attr_val, i):
                # Extraemos los atributos de esta combinacion
                attrs_en_comb = [par[0] for par in combinacion]
                # Validacion: Evitar reglas absurdas que pregunten dos veces por el mismo atributo
                if len(attrs_en_comb) == len(set(attrs_en_comb)):
                    candidatos.append(dict(combinacion))            
        return candidatos


    def entrenar(self, datos, atributos, etiquetas):
        """
        Proceso de induccion. Busca reglas iterativamente.
        """
        print(f"Iniciando induccion de Lista de Decision ({self.k}-DL)...")
        # Unimos datos y etiquetas para manipularlos juntos y poder eliminarlos
        datos_restantes = list(zip(datos, etiquetas))
        valores_unicos = self._obtener_valores_unicos(datos, atributos)
        

        # El espacio de hipotesis a explorar
        candidatos = self._generar_candidatos(valores_unicos)


        while datos_restantes:
            # Condicion de parada 1: Todos los datos restantes pertenecen a la misma clase
            clases_restantes = [etiqueta for _, etiqueta in datos_restantes]
            if len(set(clases_restantes)) == 1:
                self.clase_por_defecto = clases_restantes[0]
                break
            mejor_regla = None
            mayor_cobertura = 0
            

            # Busqueda exhaustiva de la mejor regla en este ciclo
            for candidato in candidatos:
                cubiertos = []
                clases_cubiertas = set()
                

                for fila, etiqueta in datos_restantes:
                    # Verifica si el ejemplo actual cumple con TODAS las condiciones del candidato
                    cumple = all(fila[attr] == val for attr, val in candidato.items())
                    if cumple:
                        cubiertos.append((fila, etiqueta))
                        clases_cubiertas.add(etiqueta)


                # REQUISITO K-DL: La regla debe ser PURA (solo apunta a una clase)
                if len(cubiertos) > 0 and len(clases_cubiertas) == 1:
                    # Maximizamos la cobertura: preferimos reglas que expliquen mas ejemplos
                    if len(cubiertos) > mayor_cobertura:
                        mayor_cobertura = len(cubiertos)
                        mejor_regla = (candidato, list(clases_cubiertas)[0])


            # Evaluacion del ciclo
            if mejor_regla:
                conjuncion, clase_predicha = mejor_regla
                self.lista_decision.append((conjuncion, clase_predicha))   
                # Cobertura Secuencial: Descartamos de la base de datos los ejemplos ya explicados
                datos_restantes = [
                    (f, e) for f, e in datos_restantes 
                    if not all(f[attr] == val for attr, val in conjuncion.items())
                ]
            else:
                # Condicion de parada 2: No existen reglas puras de tamaño k para los datos restantes.
                # Se asume ruido o complejidad superior a k. Establecemos clase mayoritaria y cortamos.
                self.clase_por_defecto = Counter([e for _, e in datos_restantes]).most_common(1)[0][0]
                break


        # Si agotamos los datos pero no fijamos un default final, tomamos el mayoritario del ultimo bloque
        if self.clase_por_defecto is None and datos_restantes:
             self.clase_por_defecto = Counter([e for _, e in datos_restantes]).most_common(1)[0][0]      
        print("Entrenamiento completado.")


    def predecir(self, instancia):
        """
        Clasifica un ejemplo nuevo evaluando la lista de arriba hacia abajo.
        """
        for conjuncion, clase in self.lista_decision:
            cumple = all(instancia.get(attr) == val for attr, val in conjuncion.items())
            if cumple:
                return clase
        return self.clase_por_defecto


    def imprimir_modelo(self):
        print(f"\nESTRUCTURA DEL MODELO ({self.k}-DL):")
        for i, (conjuncion, clase) in enumerate(self.lista_decision, 1):
            condiciones = " Y ".join([f"[{k} = {v}]" for k, v in conjuncion.items()])
            print(f" {i}. SI {condiciones} ENTONCES Clase -> {clase}")
        print(f" {len(self.lista_decision) + 1}. DE LO CONTRARIO ENTONCES Clase -> {self.clase_por_defecto}")



# DEMOSTRACION: COMPARATIVA DE COMPLEJIDAD
if __name__ == "__main__":
    # Dataset clasico extendido para provocar fragmentacion en arboles
    atributos = ['Clima', 'Temperatura', 'Humedad', 'Viento']
    

    X_entrenamiento = [
        {'Clima': 'Soleado', 'Temperatura': 'Calor', 'Humedad': 'Alta', 'Viento': 'Fuerte'},
        {'Clima': 'Soleado', 'Temperatura': 'Calor', 'Humedad': 'Alta', 'Viento': 'Debil'},
        {'Clima': 'Soleado', 'Temperatura': 'Frio', 'Humedad': 'Normal', 'Viento': 'Debil'},
        {'Clima': 'Soleado', 'Temperatura': 'Suave', 'Humedad': 'Alta', 'Viento': 'Fuerte'},
        {'Clima': 'Nublado', 'Temperatura': 'Calor', 'Humedad': 'Alta', 'Viento': 'Debil'},
        {'Clima': 'Nublado', 'Temperatura': 'Frio', 'Humedad': 'Normal', 'Viento': 'Fuerte'},
        {'Clima': 'Lluvia', 'Temperatura': 'Suave', 'Humedad': 'Alta', 'Viento': 'Debil'},
        {'Clima': 'Lluvia', 'Temperatura': 'Frio', 'Humedad': 'Normal', 'Viento': 'Debil'},
        {'Clima': 'Lluvia', 'Temperatura': 'Frio', 'Humedad': 'Normal', 'Viento': 'Fuerte'}
    ]
    

    y_entrenamiento = [
        'No Jugar', # Soleado, Alta humedad = No
        'No Jugar', 
        'Jugar',    # Soleado, Normal humedad = Si
        'No Jugar', 
        'Jugar',    # Nublado = Siempre Si
        'Jugar', 
        'Jugar',    # Lluvia, Viento debil = Si
        'Jugar', 
        'No Jugar'  # Lluvia, Viento fuerte = No
    ]
    

    # 1. Inducir un modelo K-DL donde k=2 (Se permiten condiciones como "A y B")
    modelo_2dl = AprendizKDL(k=2)
    modelo_2dl.entrenar(X_entrenamiento, atributos, y_entrenamiento)
    

    # 2. Visualizar la sintaxis plana y legible (El poder de K-DL)
    modelo_2dl.imprimir_modelo()
    

    # 3. Prueba de inferencia logica
    print("\nCLASIFICACION DE CASOS NUEVOS:")
    caso_prueba = {'Clima': 'Lluvia', 'Temperatura': 'Calor', 'Humedad': 'Normal', 'Viento': 'Fuerte'}
    prediccion = modelo_2dl.predecir(caso_prueba)
    print(f"Evaluando: {caso_prueba}")
    print(f" -> Prediccion: {prediccion}")
    print(" (Nota como evalua estrictamente de arriba hacia abajo hasta encontrar una coincidencia)")