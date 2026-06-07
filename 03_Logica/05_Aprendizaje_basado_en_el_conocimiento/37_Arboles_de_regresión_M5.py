import math
class RegresionLinealSimple:
    """
    Representa el modelo matematico que reside en las hojas del arbol M5.
    Ajusta una ecuacion de la forma: y = mx + b
    """
    def __init__(self):
        self.m = 0.0
        self.b = 0.0
        self.indice_caracteristica = 0



    def calcular_correlacion(self, x, y):
        n = len(x)
        if n <= 1: return 0.0
        media_x = sum(x) / n
        media_y = sum(y) / n
        numerador = sum((x[i] - media_x) * (y[i] - media_y) for i in range(n))
        den_x = sum((x[i] - media_x) ** 2 for i in range(n))
        den_y = sum((y[i] - media_y) ** 2 for i in range(n))
        if den_x == 0 or den_y == 0: 
            return 0.0
        return abs(numerador / math.sqrt(den_x * den_y))



    def entrenar(self, X, y):
        """
        Encuentra la caracteristica mas correlacionada con el objetivo y 
        realiza el ajuste por Minimos Cuadrados Ordinarios (OLS).
        """
        n_muestras = len(X)
        if n_muestras == 0: return 
        n_caracteristicas = len(X[0])
        mejor_correlacion = -1.0


        # 1. Seleccionar el mejor atributo para la regresion lineal
        for i in range(n_caracteristicas):
            columna_x = [fila[i] for fila in X]
            corr = self.calcular_correlacion(columna_x, y)
            if corr > mejor_correlacion:
                mejor_correlacion = corr
                self.indice_caracteristica = i



        # 2. Calcular los coeficientes (m y b)
        x_vals = [fila[self.indice_caracteristica] for fila in X]
        media_x = sum(x_vals) / n_muestras
        media_y = sum(y) / n_muestras
        numerador = sum((x_vals[i] - media_x) * (y[i] - media_y) for i in range(n_muestras))
        denominador = sum((x_vals[i] - media_x) ** 2 for i in range(n_muestras))
        

        if denominador == 0:
            self.m = 0.0
            self.b = media_y
        else:
            self.m = numerador / denominador
            self.b = media_y - (self.m * media_x)


    def predecir(self, fila_x):
        return (self.m * fila_x[self.indice_caracteristica]) + self.b


    def __str__(self):
        return f"y = {self.m:.4f} * X[{self.indice_caracteristica}] + {self.b:.4f}"



class ArbolModeloM5:
    """
    Implementacion del constructor del arbol de regresion basado en SDR.
    """
    def __init__(self, min_instancias=3, umbral_sdr=1e-4):
        self.min_instancias = min_instancias
        self.umbral_sdr = umbral_sdr
        self.arbol = None


    def calcular_desviacion_estandar(self, y):
        n = len(y)
        if n <= 1: return 0.0
        media = sum(y) / n
        varianza = sum((val - media) ** 2 for val in y) / n
        return math.sqrt(varianza)



    def calcular_sdr(self, X, y, indice_columna, valor_corte):
        """
        Calcula la Reduccion de la Desviacion Estandar (SDR) al dividir los datos.
        """
        sd_total = self.calcular_desviacion_estandar(y)
        y_izq = [y[i] for i in range(len(X)) if X[i][indice_columna] <= valor_corte]
        y_der = [y[i] for i in range(len(X)) if X[i][indice_columna] > valor_corte]
        


        if len(y_izq) == 0 or len(y_der) == 0:
            return 0.0    
        proporcion_izq = len(y_izq) / len(y)
        proporcion_der = len(y_der) / len(y)
        sd_izq = self.calcular_desviacion_estandar(y_izq)
        sd_der = self.calcular_desviacion_estandar(y_der)
        # SDR = Desviacion original - Suma ponderada de las desviaciones resultantes
        sdr = sd_total - ((proporcion_izq * sd_izq) + (proporcion_der * sd_der))
        return sdr



    def construir_nodo(self, X, y):
        sd_actual = self.calcular_desviacion_estandar(y)
        # CASO BASE: Pocas instancias o la desviacion ya es infima.
        # En lugar de devolver un promedio, creamos un Modelo Lineal (M5).
        if len(X) <= self.min_instancias or sd_actual < self.umbral_sdr:
            modelo = RegresionLinealSimple()
            modelo.entrenar(X, y)
            return {'es_hoja': True, 'modelo': modelo}    
        mejor_sdr = 0.0
        mejor_corte = None
        n_caracteristicas = len(X[0])
        
    
        # Busqueda exhaustiva del mejor punto de corte numerico
        for i in range(n_caracteristicas):
            valores_unicos = list(set(fila[i] for fila in X))
            for valor in valores_unicos:
                sdr = self.calcular_sdr(X, y, i, valor)
                if sdr > mejor_sdr:
                    mejor_sdr = sdr
                    mejor_corte = (i, valor)


        # Si no logramos reducir la desviacion, forzamos una hoja
        if mejor_sdr < self.umbral_sdr or mejor_corte is None:
            modelo = RegresionLinealSimple()
            modelo.entrenar(X, y)
            return {'es_hoja': True, 'modelo': modelo}



        # Realizar la particion de los datos segun el mejor corte
        idx_corte, val_corte = mejor_corte
        X_izq, y_izq, X_der, y_der = [], [], [], []
        for j in range(len(X)):
            if X[j][idx_corte] <= val_corte:
                X_izq.append(X[j])
                y_izq.append(y[j])
            else:
                X_der.append(X[j])
                y_der.append(y[j])



        # Llamada recursiva para las ramas izquierda y derecha
        return {
            'es_hoja': False,
            'indice_corte': idx_corte,
            'valor_corte': val_corte,
            'izq': self.construir_nodo(X_izq, y_izq),
            'der': self.construir_nodo(X_der, y_der)
        }



    def entrenar(self, X, y):
        print("Iniciando induccion del Arbol de Modelos (M5)...")
        self.arbol = self.construir_nodo(X, y)
        print("Entrenamiento completado.")



    def clasificar(self, nodo_actual, instancia):
        if nodo_actual['es_hoja']:
            # Ejecutamos la ecuacion lineal de la hoja correspondiente
            return nodo_actual['modelo'].predecir(instancia)
        idx = nodo_actual['indice_corte']
        val = nodo_actual['valor_corte']
        if instancia[idx] <= val:
            return self.clasificar(nodo_actual['izq'], instancia)
        else:
            return self.clasificar(nodo_actual['der'], instancia)



    def imprimir_arbol(self, nodo_actual, nivel=0):
        sangria = "    " * nivel
        if nodo_actual['es_hoja']:
            print(f"{sangria} -> Modelo final: {nodo_actual['modelo']}")
        else:
            idx = nodo_actual['indice_corte']
            val = nodo_actual['valor_corte']
            print(f"{sangria}Si Caracteristica[{idx}] <= {val}:")
            self.imprimir_arbol(nodo_actual['izq'], nivel + 1)
            print(f"{sangria}Si Caracteristica[{idx}] > {val}:")
            self.imprimir_arbol(nodo_actual['der'], nivel + 1)



# DEMOSTRACION: PREDECIR CONSUMO DE COMBUSTIBLE
if __name__ == "__main__":
    # Dataset simulado. 
    # Columna 0: Peso del vehiculo (Toneladas)
    # Columna 1: Aerodinamica (Indice)
    # Objetivo (y): Consumo de combustible (Litros/100km)
    X_entrenamiento = [
        [1.0, 0.3], [1.2, 0.35], [1.1, 0.32], [1.3, 0.4], # Vehiculos ligeros
        [2.5, 0.6], [2.6, 0.65], [2.4, 0.62], [2.7, 0.7], # Vehiculos pesados
        [4.0, 0.8], [4.1, 0.82], [4.2, 0.85], [3.9, 0.78] # Camiones
    ]
    

    y_entrenamiento = [
        5.0, 5.5, 5.2, 5.8,  # Consumo bajo
        10.0, 10.4, 9.8, 10.8, # Consumo medio
        18.0, 18.5, 19.0, 17.5 # Consumo alto
    ]
    


    # 1. Entrenar el modelo M5
    modelo = ArbolModeloM5(min_instancias=3)
    modelo.entrenar(X_entrenamiento, y_entrenamiento)
    


    # 2. Visualizar la topologia
    print("\nESTRUCTURA DEL ARBOL DE MODELOS M5:")
    modelo.imprimir_arbol(modelo.arbol)
    


    # 3. Predicciones numericas continuas
    print("\nPREDICCION CONTINUA SOBRE NUEVOS DATOS:")
    


    # Un vehiculo ligero nuevo, un SUV mediano y un camion extra pesado
    casos_prueba = [
        ([1.15, 0.33], "Auto Compacto"),
        ([2.55, 0.63], "SUV Mediana"),
        ([4.50, 0.90], "Camion Pesado")
    ]
    


    for x_prueba, descripcion in casos_prueba:
        prediccion = modelo.clasificar(modelo.arbol, x_prueba)
        print(f"[{descripcion}] Datos: {x_prueba} -> Prediccion: {prediccion:.2f} Litros/100km")