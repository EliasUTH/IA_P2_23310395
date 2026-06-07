# 1. DEFINICION DE LOS NODOS DEL ARBOL (AST)
class NodoNumero:
    """Nodo hoja que representa un valor numerico."""
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return f"Numero({self.valor})"


class NodoOperacionBinaria:
    """Nodo interno que representa una operacion matematica."""
    def __init__(self, nodo_izquierdo, operador, nodo_derecho):
        self.izq = nodo_izquierdo
        self.operador = operador
        self.der = nodo_derecho


    def __str__(self):
        return f"Operacion({self.operador})"



# 2. DEFINICION DEL SIMULADOR DE TOKENS
class TokenMoc:
    """Simula los tokens que habria entregado el Analizador Lexico previo."""
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"[{self.tipo}:{self.valor}]"



# 3. EL ANALIZADOR SINTACTICO
class AnalizadorSintactico:
    """
    Motor descendente recursivo.
    Gramatica que implementa:
      Expresion -> Termino (('+' | '-') Termino)*
      Termino   -> Factor (('*' | '/') Factor)*
      Factor    -> NUMERO | '(' Expresion ')'
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = -1
        self.token_actual = None
        self.avanzar()



    def avanzar(self):
        """Consume el token actual y avanza al siguiente en la lista."""
        self.posicion += 1
        if self.posicion < len(self.tokens):
            self.token_actual = self.tokens[self.posicion]
        else:
            self.token_actual = TokenMoc("FIN_ARCHIVO", None)



    def lanzar_error(self, esperado):
        """Maneja las violaciones gramaticales (Errores de Sintaxis)."""
        encontrado = self.token_actual.tipo if self.token_actual else "FIN"
        raise SyntaxError(f"Error Sintactico: Se esperaba {esperado}, pero se encontro {encontrado}")



    #REGLAS GRAMATICALES COMO FUNCIONES
    def factor(self):
        """Factor -> NUMERO | '(' Expresion ')'"""
        token = self.token_actual


        if token.tipo == "NUMERO":
            self.avanzar()
            return NodoNumero(token.valor)
            

        elif token.tipo == "PARENTESIS_IZQ":
            self.avanzar()
            nodo_interno = self.expresion() # Recursividad: Un parentesis abre una nueva expresion
            
            if self.token_actual.tipo == "PARENTESIS_DER":
                self.avanzar()
                return nodo_interno
            else:
                self.lanzar_error("PARENTESIS_DER")     
        self.lanzar_error("NUMERO o PARENTESIS_IZQ")


    def termino(self):
        """Termino -> Factor (('*' | '/') Factor)*"""
        # Un termino siempre empieza con un factor
        nodo_izquierdo = self.factor()


        # Mientras encontremos operadores de multiplicacion/division, expandimos el arbol
        while self.token_actual.tipo in ("MULTIPLICACION", "DIVISION"):
            operador = self.token_actual.valor
            self.avanzar()
            nodo_derecho = self.factor()
            # El nodo anterior se convierte en el hijo izquierdo de la nueva operacion
            nodo_izquierdo = NodoOperacionBinaria(nodo_izquierdo, operador, nodo_derecho)
        return nodo_izquierdo


    def expresion(self):
        """Expresion -> Termino (('+' | '-') Termino)*"""
        # Una expresion siempre empieza con un termino
        nodo_izquierdo = self.termino()


        # Mientras encontremos operadores de suma/resta, expandimos el arbol
        while self.token_actual.tipo in ("SUMA", "RESTA"):
            operador = self.token_actual.valor
            self.avanzar()
            nodo_derecho = self.termino()
            nodo_izquierdo = NodoOperacionBinaria(nodo_izquierdo, operador, nodo_derecho)
        return nodo_izquierdo


    def parsear(self):
        """Punto de entrada principal del analizador."""
        arbol_sintactico = self.expresion()
        # Al terminar de procesar, no deberian quedar tokens sueltos
        if self.token_actual.tipo != "FIN_ARCHIVO":
            self.lanzar_error("FIN_ARCHIVO (hay codigo extra no valido)")
            
        return arbol_sintactico



# HERRAMIENTA DE VISUALIZACION
def imprimir_arbol_ast(nodo, nivel=0):
    """Recorre el arbol en pre-orden para mostrarlo en formato de texto anidado."""
    sangria = "    " * nivel
    if isinstance(nodo, NodoNumero):
        print(f"{sangria} -> {nodo}")
    elif isinstance(nodo, NodoOperacionBinaria):
        print(f"{sangria} -> {nodo}")
        print(f"{sangria}    Lado Izquierdo:")
        imprimir_arbol_ast(nodo.izq, nivel + 1)
        print(f"{sangria}    Lado Derecho:")
        imprimir_arbol_ast(nodo.der, nivel + 1)



# DEMOSTRACION: COMPRENDIENDO LA PRECEDENCIA
if __name__ == "__main__":
    # Vamos a procesar la operacion logica: 3 + 5 * ( 10 - 2 )
    # Aqui emulamos la salida exacta que habria dado nuestro Analizador Lexico anterior
    flujo_tokens_entrada = [
        TokenMoc("NUMERO", 3),
        TokenMoc("SUMA", "+"),
        TokenMoc("NUMERO", 5),
        TokenMoc("MULTIPLICACION", "*"),
        TokenMoc("PARENTESIS_IZQ", "("),
        TokenMoc("NUMERO", 10),
        TokenMoc("RESTA", "-"),
        TokenMoc("NUMERO", 2),
        TokenMoc("PARENTESIS_DER", ")")
    ]
    

    print("ANALIZADOR SINTACTICO (PARSER)")
    print("Cadena de Tokens recibida del Analizador Lexico:")
    print(" ".join([str(t) for t in flujo_tokens_entrada]))
    print("-" * 53)
    

    # Ejecutamos el analisis sintactico
    parser = AnalizadorSintactico(flujo_tokens_entrada)
    arbol_resultante = parser.parsear()
    print("\nEstructura del Arbol de Sintaxis Abstracta (AST) generado:")
    print("Note como el nodo raiz es la SUMA, obligando a que la multiplicacion se resuelva antes.")
    print("-" * 53)
    imprimir_arbol_ast(arbol_resultante)