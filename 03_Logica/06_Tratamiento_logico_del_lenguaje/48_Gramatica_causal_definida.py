class GramaticaClausulasDefinidas:
    """
    Simulador de Definite Clause Grammar (DCG) en Python.
    Utiliza listas de diferencia para evaluar el lenguaje.
    Cada regla gramatical es una funcion (clausula logica) que recibe un 
    estado del universo (tokens) y devuelve todos los universos posibles resultantes.
    """
    

    def terminal(self, palabra_esperada, tokens):
        """
        Predicado base. Verifica si la primera palabra de la lista coincide.
        Devuelve una lista con el resto de los tokens si hay coincidencia.
        """
        if tokens and tokens[0] == palabra_esperada:
            return [tokens[1:]] # Consumimos la palabra y devolvemos lo que sobra
        return [] # Falla logica: devuelve una lista vacia de posibilidades


    # EL LEXICON (Diccionario logico)
    def determinante(self, tokens):
        """ det --> [el] | [la] | [un] """
        # La suma de listas en Python simula el operador logico OR (Disyuncion)
        return self.terminal('el', tokens) + \
               self.terminal('la', tokens) + \
               self.terminal('un', tokens)


    def sustantivo(self, tokens):
        """ sust --> [gato] | [perro] | [raton] """
        return self.terminal('gato', tokens) + \
               self.terminal('perro', tokens) + \
               self.terminal('raton', tokens)


    def verbo(self, tokens):
        """ verbo --> [persigue] | [mira] """
        return self.terminal('persigue', tokens) + \
               self.terminal('mira', tokens)


    # REGLAS SINTACTICAS (Clausulas complejas)
    def sintagma_nominal(self, tokens):
        """ 
        NP --> det, sust 
        Logica subyacente: NP(A, C) :- det(A, B), sust(B, C).
        """
        resultados = []
        # Para cada universo donde se encontro un determinante...
        for resto_tras_det in self.determinante(tokens):
            # ...intentamos encontrar un sustantivo inmediatamente despues
            for resto_tras_sust in self.sustantivo(resto_tras_det):
                resultados.append(resto_tras_sust)
        return resultados


    def sintagma_verbal(self, tokens):
        """ 
        VP --> verbo, NP 
        Logica subyacente: VP(A, C) :- verbo(A, B), NP(B, C).
        """
        resultados = []
        for resto_tras_verbo in self.verbo(tokens):
            for resto_tras_np in self.sintagma_nominal(resto_tras_verbo):
                resultados.append(resto_tras_np)
        return resultados


    def oracion(self, tokens):
        """ 
        S --> NP, VP 
        Logica subyacente: S(A, C) :- NP(A, B), VP(B, C).
        """
        resultados = []
        for resto_tras_np in self.sintagma_nominal(tokens):
            for resto_tras_vp in self.sintagma_verbal(resto_tras_np):
                resultados.append(resto_tras_vp)
        return resultados


    # MOTOR DE INFERENCIA
    def analizar(self, frase):
        """
        Punto de entrada. Convierte la frase a tokens y evalua el teorema.
        """
        tokens = frase.lower().split()
        print(f"Evaluando teorema logico para: {tokens}")
        

        # Llamamos al axioma principal (oracion)
        posibles_restos = self.oracion(tokens)
        

        # Si entre todas las ramificaciones logicas existe un caso 
        # donde la lista de tokens quedo vacia ([]), la frase es valida.
        if [] in posibles_restos:
            return True
        return False



# DEMOSTRACION: ANALISIS MEDIANTE DCG
if __name__ == "__main__":
    motor_dcg = GramaticaClausulasDefinidas()
    

    print("GRAMATICA DE CLAUSULAS DEFINIDAS (DCG)\n")
    # Pruebas con lenguaje natural
    frases_prueba = [
        "el gato persigue un raton", # Valida (Det Sust Verbo Det Sust)
        "la perro mira el gato",     # Valida gramaticalmente (aunque incoherente en genero, DCG basica no revisa concordancia)
        "el persigue raton",         # Invalida (Falta el sustantivo en el sujeto)
        "un perro mira un perro",    # Valida
        "gato mira el raton"         # Invalida (Falta el determinante en el sujeto)
    ]
    

    for frase in frases_prueba:
        resultado = motor_dcg.analizar(frase)
        estatus = "VALIDA (Teorema Demostrado)" if resultado else "INVALIDA (Contradiccion/Fallo)"
        print(f" -> Conclusion: {estatus}\n")