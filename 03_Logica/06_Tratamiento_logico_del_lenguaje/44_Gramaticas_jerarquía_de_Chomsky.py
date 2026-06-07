class AnalizadorChomsky:
    """
    Clasificador de gramáticas formales según la Jerarquía de Chomsky.
    Asume una convención estándar: 
    - Mayúsculas (A-Z) son Símbolos No Terminales.
    - Minúsculas (a-z) y símbolos son Símbolos Terminales.
    - Épsilon (cadena vacía) se representa como una cadena vacía "".
    """
    
    
    @staticmethod
    def es_no_terminal(simbolo):
        return simbolo.isupper()


    @staticmethod
    def es_terminal(simbolo):
        return not simbolo.isupper() and simbolo != ""


    def clasificar_gramatica(self, producciones):
        """
        Recibe una lista de producciones en formato de tuplas: (lado_izquierdo, lado_derecho)
        Devuelve el nivel más restrictivo (el número más alto) de la jerarquía que cumple.
        """
        es_tipo_3 = True
        es_tipo_2 = True
        es_tipo_1 = True
        

        # Validacion base: Toda produccion debe tener al menos un No Terminal en la izquierda
        for izq, der in producciones:
            if not any(self.es_no_terminal(char) for char in izq):
                return "Invalida: El lado izquierdo no contiene Símbolos No Terminales."


        for izq, der in producciones:
            # Evaluacion TIPO 1 (Sensible al contexto): |Lado Izquierdo| <= |Lado Derecho|
            # (Excluimos la regla especial del axioma S -> epsilon por simplicidad de este modelo)
            if der != "" and len(izq) > len(der):
                es_tipo_1 = False


            # Evaluacion TIPO 2 (Independiente del contexto): Lado Izquierdo es exactamente UN No Terminal
            if len(izq) != 1 or not self.es_no_terminal(izq):
                es_tipo_2 = False
                es_tipo_3 = False # Si no es Tipo 2, logicamente no puede ser Tipo 3
            else:
                # Evaluacion TIPO 3 (Regular Lineal por la Derecha): 
                # El lado derecho debe ser: un terminal "a", o un terminal seguido de un No Terminal "aB"
                if es_tipo_3:
                    if len(der) == 0:
                        pass # Epsilon permitido
                    elif len(der) == 1:
                        if not self.es_terminal(der):
                            es_tipo_3 = False
                    elif len(der) == 2:
                        if not (self.es_terminal(der[0]) and self.es_no_terminal(der[1])):
                            es_tipo_3 = False
                    else:
                        es_tipo_3 = False


        # Retornamos la clasificacion descendiendo desde la mas estricta a la mas general
        if es_tipo_3: return "Tipo 3 (Gramatica Regular)"
        if es_tipo_2: return "Tipo 2 (Gramatica Independiente del Contexto)"
        if es_tipo_1: return "Tipo 1 (Gramatica Sensible al Contexto)"
        return "Tipo 0 (Gramatica Recursivamente Enumerable)"



# DEMOSTRACION: EVALUACION DE GRAMATICAS
if __name__ == "__main__":
    analizador = AnalizadorChomsky()
    print("___ANALIZADOR DE JERARQUIA DE CHOMSKY___\n")
    # 1. Gramatica Regular (Tipo 3)
    # Reglas: S -> aA, A -> b
    gramatica_3 = [
        ("S", "aA"),
        ("A", "b")
    ]
    


    # 2. Gramatica Independiente del Contexto (Tipo 2)
    # Reglas: S -> aSb, S -> c (Clasica gramatica para lenguajes como a^n c b^n)
    gramatica_2 = [
        ("S", "aSb"),
        ("S", "c")
    ]
    


    # 3. Gramatica Sensible al Contexto (Tipo 1)
    # Reglas: aA -> aB (A se transforma en B solo si esta precedido por 'a')
    gramatica_1 = [
        ("S", "aAb"),
        ("aA", "aB"),
        ("B", "c")
    ]


    
    # 4. Gramatica Recursivamente Enumerable (Tipo 0)
    # Reglas: AB -> a (Se reduce la longitud de la cadena de forma arbitraria)
    gramatica_0 = [
        ("S", "AB"),
        ("AB", "a")
    ]
    


    casos_prueba = [
        ("Gramatica A (Patrones simples)", gramatica_3),
        ("Gramatica B (Estructuras anidadas / Parentesis)", gramatica_2),
        ("Gramatica C (Dependencia del entorno)", gramatica_1),
        ("Gramatica D (Sustituciones destructivas libres)", gramatica_0)
    ]
    


    for nombre, reglas in casos_prueba:
        print(f"Evaluando {nombre}:")
        for izq, der in reglas:
            der_impreso = der if der != "" else "ε (epsilon)"
            print(f"  {izq} -> {der_impreso}")
        clasificacion = analizador.clasificar_gramatica(reglas)
        print(f"Resultado: {clasificacion}\n")