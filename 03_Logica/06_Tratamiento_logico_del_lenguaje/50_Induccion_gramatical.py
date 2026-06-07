from collections import defaultdict
class InductorGramaticalPCFG:
    """
    Inductor de Gramaticas Probabilisticas Libres de Contexto.
    Aprende reglas de produccion y sus probabilidades a partir de un corpus.
    """
    def __init__(self):
        # Diccionario para contar cuantas veces aparece la parte izquierda de una regla (LHS)
        self.conteo_lhs = defaultdict(int)
        # Diccionario para contar cuantas veces ocurre la derivacion exacta (LHS -> RHS)
        self.conteo_reglas = defaultdict(int)
        # Diccionario final que almacenara el conocimiento estructurado
        self.gramatica_probabilistica = {}


    def _extraer_reglas(self, arbol):
        """
        Recorre recursivamente un arbol sintactico de entrenamiento.
        Formato esperado de los nodos: (Etiqueta_Padre, [Hijo1, Hijo2, ...])
        """
        lado_izquierdo = arbol[0]
        nodos_hijos = arbol[1]
        

        # Construimos el lado derecho extrayendo las etiquetas de los hijos
        lado_derecho = []
        for hijo in nodos_hijos:
            if isinstance(hijo, tuple):
                # Es un nodo intermedio (No Terminal)
                lado_derecho.append(hijo[0])
                # Descendemos recursivamente en el arbol
                self._extraer_reglas(hijo)
            else:
                # Es una palabra final (Simbolo Terminal)
                lado_derecho.append(hijo)
        lado_derecho_tupla = tuple(lado_derecho)
        

        # Contabilidad matematica de ocurrencias
        self.conteo_lhs[lado_izquierdo] += 1
        self.conteo_reglas[(lado_izquierdo, lado_derecho_tupla)] += 1


    def entrenar_desde_corpus(self, corpus):
        """
        Procesa multiples arboles y calcula la Estimacion de Maxima Verosimilitud (MLE).
        """
        print("Analizando corpus de entrenamiento...")
        for arbol in corpus:
            self._extraer_reglas(arbol)
            

        # Calculo de probabilidades formales: P(RHS | LHS) = Conteo(LHS -> RHS) / Conteo(LHS)
        for (lhs, rhs), conteo_regla in self.conteo_reglas.items():
            conteo_total_lhs = self.conteo_lhs[lhs]
            probabilidad = conteo_regla / conteo_total_lhs
            

            if lhs not in self.gramatica_probabilistica:
                self.gramatica_probabilistica[lhs] = []
            self.gramatica_probabilistica[lhs].append((rhs, probabilidad))
            

        # Ordenamos las reglas matematicamente (de mayor a menor probabilidad)
        for lhs in self.gramatica_probabilistica:
            self.gramatica_probabilistica[lhs].sort(key=lambda x: x[1], reverse=True)



    def imprimir_gramatica(self):
        print("\nGRAMATICA PROBABILISTICA INDUCIDA (PCFG)")
        for lhs, derivaciones in self.gramatica_probabilistica.items():
            for rhs, probabilidad in derivaciones:
                rhs_str = " ".join(rhs)
                # Formato final de la regla descubierta
                print(f" {lhs:<5} -> {rhs_str:<25} [Probabilidad: {probabilidad:.4f}]")
        print("-" * 53)



# DEMOSTRACION: EXTRACCION DE REGLAS DE UN TREEBANK
if __name__ == "__main__":
    # Un "Treebank" simulado: una coleccion de frases ya analizadas.
    # El sistema no sabe de antemano que es un Sujeto o un Verbo; solo observa patrones.
    corpus_entrenamiento = [
        # Frase 1: "el gato observa un raton"
        ("S", [
            ("NP", [("Det", ["el"]), ("N", ["gato"])]),
            ("VP", [("V", ["observa"]), ("NP", [("Det", ["un"]), ("N", ["raton"])])])
        ]),
        


        # Frase 2: "la mujer ve el gato"
        ("S", [
            ("NP", [("Det", ["la"]), ("N", ["mujer"])]),
            ("VP", [("V", ["ve"]), ("NP", [("Det", ["el"]), ("N", ["gato"])])])
        ]),
        


        # Frase 3: "un perro duerme"
        ("S", [
            ("NP", [("Det", ["un"]), ("N", ["perro"])]),
            ("VP", [("V", ["duerme"])])
        ]),
        


        # Frase 4: "el hombre observa un perro con telescopio"
        ("S", [
            ("NP", [("Det", ["el"]), ("N", ["hombre"])]),
            ("VP", [
                ("V", ["observa"]), 
                ("NP", [("Det", ["un"]), ("N", ["perro"])]),
                ("PP", [("P", ["con"]), ("NP", [("N", ["telescopio"])])])
            ])
        ])
    ]
    print("-----------------------------------------------------")
    print("INDUCTOR DE GRAMATICAS ESTADISTICAS")
    print("-----------------------------------------------------\n")
    print(f"Corpus cargado con {len(corpus_entrenamiento)} oraciones de entrenamiento.")
    inductor = InductorGramaticalPCFG()
    inductor.entrenar_desde_corpus(corpus_entrenamiento)
    

    # Mostrar el conocimiento estructural que la maquina extrajo por si sola
    inductor.imprimir_gramatica()