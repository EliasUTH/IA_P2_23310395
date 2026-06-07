import copy
class EspacioDeVersiones:
    """
    Simula el algoritmo de Eliminacion de Candidatos.
    Mantiene los limites S (Especifico) y G (General).
    """
    def __init__(self, num_atributos):
        self.num_atributos = num_atributos
        # G empieza totalmente permisivo
        self.G = [['?'] * num_atributos]
        # S empieza totalmente restrictivo (representado con '0' o None)
        self.S = [['0'] * num_atributos]
        self.inicializado = False


    def es_consistente(self, hipotesis, ejemplo):
        """Verifica si un ejemplo cumple con una hipotesis."""
        for h, e in zip(hipotesis, ejemplo):
            if h != '?' and h != e:
                return False
        return True


    def entrenar_paso(self, ejemplo, es_positivo):
        print(f"\nProcesando ejemplo {'[POSITIVO]' if es_positivo else '[NEGATIVO]'}: {ejemplo}")
        

        if es_positivo:
            # 1. Inicializar S con el primer ejemplo positivo
            if not self.inicializado:
                self.S = [list(ejemplo)]
                self.inicializado = True
            else:
                # 2. Generalizar S para incluir el nuevo ejemplo positivo
                nuevos_S = []
                for s in self.S:
                    nuevo_s = list(s)
                    for i in range(self.num_atributos):
                        if nuevo_s[i] != '?' and nuevo_s[i] != ejemplo[i]:
                            nuevo_s[i] = '?'
                    nuevos_S.append(nuevo_s)
                self.S = nuevos_S


            # 3. Eliminar de G cualquier hipotesis que no cubra el ejemplo positivo
            self.G = [g for g in self.G if self.es_consistente(g, ejemplo)]
            

        else:
            # Para un ejemplo negativo:
            # 1. Eliminar de S cualquier hipotesis que cubra el ejemplo negativo
            self.S = [s for s in self.S if not self.es_consistente(s, ejemplo)]
            

            # 2. Especializar G para excluir el ejemplo negativo
            nuevos_G = []
            for g in self.G:
                if self.es_consistente(g, ejemplo):
                    # Generamos especializaciones de G
                    for i in range(self.num_atributos):
                        if g[i] == '?':
                            # Especializamos apuntando al valor del limite S (simplificacion para este simulador)
                            # En un algoritmo completo, se iteran todos los valores posibles del dominio
                            for s in self.S:
                                if s[i] != '?' and s[i] != ejemplo[i]:
                                    nuevo_g = list(g)
                                    nuevo_g[i] = s[i]
                                    if nuevo_g not in nuevos_G:
                                        nuevos_G.append(nuevo_g)
                else:
                    nuevos_G.append(g)
            self.G = nuevos_G


    def imprimir_estado(self):
        print(" -> Limite General (G):", self.G)
        print(" -> Limite Especifico (S):", self.S)



class AlgoritmoAQ:
    """
    Implementacion simplificada del algoritmo AQ (Generacion de Estrellas).
    Aprende reglas disyuntivas para un conjunto de ejemplos positivos.
    """
    def __init__(self, num_atributos):
        self.num_atributos = num_atributos
        self.reglas_finales = []


    def _es_cubierto(self, regla, ejemplo):
        for r, e in zip(regla, ejemplo):
            if r != '?' and r != e:
                return False
        return True


    def _especializar_contra_negativo(self, semilla, negativo):
        """
        Genera reglas parciales comparando la semilla con un ejemplo negativo.
        Donde difieran, crea una restriccion para bloquear al negativo.
        """
        extensiones = []
        for i in range(self.num_atributos):
            if semilla[i] != negativo[i]:
                nueva_regla = ['?'] * self.num_atributos
                nueva_regla[i] = semilla[i]
                extensiones.append(nueva_regla)
        return extensiones


    def entrenar(self, positivos, negativos):
        print("\nIniciando induccion mediante Algoritmo AQ...")
        positivos_restantes = copy.deepcopy(positivos)
        

        while positivos_restantes:
            # 1. Tomar el primer ejemplo positivo como Semilla
            semilla = positivos_restantes[0]
            print(f"\nSeleccionando Semilla: {semilla}")
            

            # 2. Generar la 'Estrella' (complejo de hipotesis validas)
            # Empezamos con la hipotesis universal
            estrella = [['?'] * self.num_atributos]
            for negativo in negativos:
                nueva_estrella = []
                for regla_actual in estrella:
                    if self._es_cubierto(regla_actual, negativo):
                        # Si la regla cubre un negativo, debemos especializarla
                        extensiones = self._especializar_contra_negativo(semilla, negativo)
                        

                        # Combinamos la regla actual con la especializacion
                        for ext in extensiones:
                            regla_combinada = list(regla_actual)
                            es_valida = True
                            for i in range(self.num_atributos):
                                if ext[i] != '?':
                                    if regla_combinada[i] == '?':
                                        regla_combinada[i] = ext[i]
                                    elif regla_combinada[i] != ext[i]:
                                        es_valida = False # Contradiccion
                            if es_valida and regla_combinada not in nueva_estrella:
                                nueva_estrella.append(regla_combinada)
                    else:
                        nueva_estrella.append(regla_actual)
                estrella = nueva_estrella   
            print(f"Estrella generada para aislar la semilla de los negativos: {estrella}")
            

            # 3. Seleccionar la mejor regla de la estrella (la mas general)
            # Para este simulador, tomamos la regla que tenga mas comodines '?'
            mejor_regla = max(estrella, key=lambda r: r.count('?'))
            self.reglas_finales.append(mejor_regla)
            print(f"Mejor regla seleccionada: {mejor_regla}")
            

            # 4. Eliminar los ejemplos positivos ya explicados por esta regla
            positivos_restantes = [p for p in positivos_restantes if not self._es_cubierto(mejor_regla, p)]
            print(f"Ejemplos positivos sin explicar restantes: {len(positivos_restantes)}")
        print("\nEntrenamiento AQ completado. Reglas descubiertas:")
        for i, regla in enumerate(self.reglas_finales, 1):
            print(f" Regla {i}: {regla}")



# DEMOSTRACION COMPARATIVA
if __name__ == "__main__":
    # Atributos: [Forma, Color, Tamaño]
    X_entrenamiento = [
        (['Circulo', 'Rojo', 'Grande'], True),   # 0
        (['Triangulo', 'Azul', 'Grande'], False),# 1
        (['Circulo', 'Azul', 'Grande'], True),   # 2
        (['Cuadrado', 'Rojo', 'Pequeño'], False) # 3
    ]
    

    # --- DEMOSTRACION 1: ESPACIO DE VERSIONES ---
    print("ENFOQUE 1: ESPACIO DE VERSIONES (Eliminacion de Candidatos)")
    motor_ev = EspacioDeVersiones(num_atributos=3)
    

    for ejemplo, es_positivo in X_entrenamiento:
        motor_ev.entrenar_paso(ejemplo, es_positivo)
        motor_ev.imprimir_estado()     
    print("\nCONCLUSION ESPACIO DE VERSIONES:")
    print("Si G y S son identicos, el concepto se ha aprendido exactamente.")
    print(f"Concepto final: {motor_ev.S[0]}")


    # --- DEMOSTRACION 2: ALGORITMO AQ ---
    print("\nENFOQUE 2: ALGORITMO AQ (Recubrimiento Secuencial)")
    ejemplos_positivos = [ex for ex, es_pos in X_entrenamiento if es_pos]
    ejemplos_negativos = [ex for ex, es_pos in X_entrenamiento if not es_pos]
    motor_aq = AlgoritmoAQ(num_atributos=3)
    motor_aq.entrenar(ejemplos_positivos, ejemplos_negativos)