class AnalizadorAmbiguedad:
    """
    Analizador Sintactico (Parser) que explora todas las rutas gramaticales.
    Implementa una Gramatica Independiente del Contexto (Tipo 2) ambigua.
    """
    

    def coincidencia_lexica(self, tokens, lista_palabras, etiqueta):
        """Consume un token si coincide con el lexico y devuelve un nodo hoja."""
        if tokens and tokens[0] in lista_palabras:
            nodo = f"[{etiqueta} {tokens[0]}]"
            return [(nodo, tokens[1:])]
        return []



    # LEXICON (Reglas Lexicas)
    def determinante(self, tokens):
        return self.coincidencia_lexica(tokens, ['el', 'un'], 'Det')


    def sustantivo(self, tokens):
        return self.coincidencia_lexica(tokens, ['juan', 'hombre', 'telescopio'], 'N')


    def verbo(self, tokens):
        return self.coincidencia_lexica(tokens, ['vio'], 'V')


    def preposicion(self, tokens):
        return self.coincidencia_lexica(tokens, ['con'], 'P')


    # REGLAS SINTACTICAS (Generadoras de Ambiguedad)
    def sintagma_preposicional(self, tokens):
        """ PP -> P NP """
        resultados = []
        for nodo_p, resto_p in self.preposicion(tokens):
            for nodo_np, resto_np in self.sintagma_nominal(resto_p):
                resultados.append((f"[PP {nodo_p} {nodo_np}]", resto_np))
        return resultados


    def sintagma_nominal(self, tokens):
        """ 
        NP -> N 
        NP -> Det N
        NP -> Det N PP  <-- Regla recursiva: El PP modifica al Sustantivo
        """
        resultados = []
        

        # Opcion 1: Solo Sustantivo (ej. "juan")
        for nodo_n, resto_n in self.sustantivo(tokens):
            resultados.append((f"[NP {nodo_n}]", resto_n))
            

        # Opcion 2 y 3: Determinante + Sustantivo [ + Sintagma Preposicional Opcional ]
        for nodo_det, resto_det in self.determinante(tokens):
            for nodo_n, resto_n in self.sustantivo(resto_det):
                # Opcion 2 (Sin PP)
                resultados.append((f"[NP {nodo_det} {nodo_n}]", resto_n))
                

                # Opcion 3 (Con PP adjunto al sustantivo)
                for nodo_pp, resto_pp in self.sintagma_preposicional(resto_n):
                    resultados.append((f"[NP {nodo_det} {nodo_n} {nodo_pp}]", resto_pp))       
        return resultados


    def sintagma_verbal(self, tokens):
        """ 
        VP -> V NP 
        VP -> V NP PP   <-- Regla recursiva: El PP modifica al Verbo
        """
        resultados = []
        for nodo_v, resto_v in self.verbo(tokens):
            for nodo_np, resto_np in self.sintagma_nominal(resto_v):
                # Opcion 1 (Sin PP)
                resultados.append((f"[VP {nodo_v} {nodo_np}]", resto_np))
                

                # Opcion 2 (Con PP adjunto al verbo)
                for nodo_pp, resto_pp in self.sintagma_preposicional(resto_np):
                    resultados.append((f"[VP {nodo_v} {nodo_np} {nodo_pp}]", resto_pp))           
        return resultados



    def oracion(self, tokens):
        """ S -> NP VP """
        resultados = []
        for nodo_np, resto_np in self.sintagma_nominal(tokens):
            for nodo_vp, resto_vp in self.sintagma_verbal(resto_np):
                resultados.append((f"[S {nodo_np} {nodo_vp}]", resto_vp))
        return resultados


    # MOTOR DE EJECUCION
    def procesar_frase(self, frase):
        tokens = frase.lower().split()
        print(f"Analizando: '{frase}'\n")
        
        # Obtenemos todos los arboles generados por la regla raiz (Oracion)
        arboles_posibles = self.oracion(tokens)
        arboles_validos = []


        # Filtramos solo los arboles que consumieron todos los tokens de la frase
        for arbol, tokens_restantes in arboles_posibles:
            if len(tokens_restantes) == 0:
                arboles_validos.append(arbol)
                

        if len(arboles_validos) == 0:
            print("Error: Frase gramaticalmente invalida.")
        elif len(arboles_validos) == 1:
            print("Frase inequivoca. Un unico arbol de derivacion:")
            print(arboles_validos[0])
        else:
            print(f"¡ALERTA DE AMBIGUEDAD! Se encontraron {len(arboles_validos)} interpretaciones validas:\n")
            for i, arbol in enumerate(arboles_validos, 1):
                print(f"Interpretacion Logica {i}:")
                # Formateo rudimentario para facilitar la lectura de anidamientos
                arbol_formateado = arbol.replace(" [", "\n  [").replace("]]", "]\n]")
                print(arbol)
                print("-" * 60)



# DEMOSTRACION: EL PROBLEMA DE LA AMBIGUEDAD
if __name__ == "__main__":
    analizador = AnalizadorAmbiguedad()
    print("DEMOSTRACION: FRASES INEQUIVOCAS VS AMBIGUAS\n")
    # Caso 1: Una frase simple y directa
    analizador.procesar_frase("juan vio el hombre")
    print("\n" + "="*60 + "\n")


    # Caso 2: Introducimos la frase con el adjunto preposicional (PP)
    analizador.procesar_frase("juan vio el hombre con el telescopio")