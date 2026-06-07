# 1. DEFINICION DE LOS NODOS DEL AST
class NodoPrograma:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones


class NodoDeclaracion:
    """Ejemplo: entero x; o cadena nombre;"""
    def __init__(self, tipo_dato, identificador):
        self.tipo_dato = tipo_dato
        self.identificador = identificador


class NodoAsignacion:
    """Ejemplo: x = 10;"""
    def __init__(self, identificador, expresion):
        self.identificador = identificador
        self.expresion = expresion


class NodoOperacionBinaria:
    """Ejemplo: 5 + x"""
    def __init__(self, izq, operador, der):
        self.izq = izq
        self.operador = operador
        self.der = der


class NodoNumero:
    def __init__(self, valor):
        self.valor = valor
        self.tipo_inferido = "entero"


class NodoCadena:
    def __init__(self, valor):
        self.valor = valor
        self.tipo_inferido = "cadena"


class NodoVariable:
    def __init__(self, nombre):
        self.nombre = nombre



# 2. TABLA DE SIMBOLOS (Memoria de Contexto)
class TablaSimbolos:
    """Almacena el registro de todas las variables y sus tipos declarados."""
    def __init__(self):
        self.simbolos = {}


    def declarar(self, nombre, tipo_dato):
        if nombre in self.simbolos:
            raise Exception(f"Error Semantico: La variable '{nombre}' ya fue declarada previamente.")
        self.simbolos[nombre] = tipo_dato


    def obtener_tipo(self, nombre):
        if nombre not in self.simbolos:
            raise Exception(f"Error Semantico: La variable '{nombre}' no ha sido declarada.")
        return self.simbolos[nombre]



# 3. ANALIZADOR SEMANTICO (Visitor)
class AnalizadorSemantico:
    """
    Recorre el AST nodo por nodo para validar reglas de significado y contexto.
    Implementa un sistema de Inferencia de Tipos.
    """
    def __init__(self):
        self.tabla_simbolos = TablaSimbolos()


    def analizar(self, nodo):
        """Metodo despachador que llama a la funcion especifica segun el tipo de nodo."""
        nombre_metodo = 'visitar_' + type(nodo).__name__
        visitador = getattr(self, nombre_metodo, self.error_nodo_desconocido)
        return visitador(nodo)


    def error_nodo_desconocido(self, nodo):
        raise Exception(f"Error interno: No hay logica semantica para el nodo {type(nodo).__name__}")


    def visitar_NodoPrograma(self, nodo):
        for instruccion in nodo.instrucciones:
            self.analizar(instruccion)


    def visitar_NodoDeclaracion(self, nodo):
        # Regla Semantica 1: Registrar variables nuevas
        print(f"[Semantica] Declarando variable '{nodo.identificador}' de tipo '{nodo.tipo_dato}'.")
        self.tabla_simbolos.declarar(nodo.identificador, nodo.tipo_dato)


    def visitar_NodoAsignacion(self, nodo):
        # Regla Semantica 2: La variable asignada debe existir
        tipo_variable = self.tabla_simbolos.obtener_tipo(nodo.identificador)
        

        # Inferencia de tipos evaluando el lado derecho de la igualdad
        tipo_expresion = self.analizar(nodo.expresion)
        

        # Regla Semantica 3: Compatibilidad de tipos
        if tipo_variable != tipo_expresion:
            raise Exception(f"Error Semantico en asignacion: No se puede asignar un valor tipo '{tipo_expresion}' a la variable '{nodo.identificador}' de tipo '{tipo_variable}'.")
        print(f"[Semantica] Asignacion valida: '{nodo.identificador}' = {tipo_expresion}.")


    def visitar_NodoOperacionBinaria(self, nodo):
        tipo_izq = self.analizar(nodo.izq)
        tipo_der = self.analizar(nodo.der)
        

        # Regla Semantica 4: Reglas de operaciones
        if nodo.operador in ('+', '-', '*', '/'):
            if tipo_izq == "entero" and tipo_der == "entero":
                return "entero" # La suma de enteros da un entero
            else:
                raise Exception(f"Error Semantico de Tipos: Operacion '{nodo.operador}' no soportada entre '{tipo_izq}' y '{tipo_der}'.")


    def visitar_NodoNumero(self, nodo):
        return nodo.tipo_inferido


    def visitar_NodoCadena(self, nodo):
        return nodo.tipo_inferido


    def visitar_NodoVariable(self, nodo):
        # Cuando se usa una variable en una expresion, devolvemos su tipo
        return self.tabla_simbolos.obtener_tipo(nodo.nombre)



# DEMOSTRACION: VALIDACION DE CONTEXTO
if __name__ == "__main__":
    # --- ESCENARIO 1: PROGRAMA SEMANTICAMENTE VALIDO ---
    # Codigo original simulado:
    # entero edad;
    # edad = 10 + 5;
    ast_valido = NodoPrograma([
        NodoDeclaracion("entero", "edad"),
        NodoAsignacion("edad", 
            NodoOperacionBinaria(
                NodoNumero(10), 
                "+", 
                NodoNumero(5)
            )
        )
    ])
    

    print("ESCENARIO 1: COMPILACION DE PROGRAMA VALIDO")
    analizador = AnalizadorSemantico()
    try:
        analizador.analizar(ast_valido)
        print(" -> Resultado: Analisis Semantico Exitoso. Codigo limpio.")
    except Exception as e:
        print(e)
        


    # --- ESCENARIO 2: PROGRAMA CON ERRORES DE TIPO ---
    # Codigo original simulado:
    # cadena nombre;
    # nombre = "Juan" + 5;
    ast_invalido = NodoPrograma([
        NodoDeclaracion("cadena", "nombre"),
        NodoAsignacion("nombre", 
            NodoOperacionBinaria(
                NodoCadena("Juan"), 
                "+", 
                NodoNumero(5)
            )
        )
    ])
    


    print("\nESCENARIO 2: DETECCION DE INCOMPATIBILIDAD DE TIPOS")
    analizador_2 = AnalizadorSemantico()
    try:
        analizador_2.analizar(ast_invalido)
    except Exception as e:
        print(e)


    # --- ESCENARIO 3: USO DE VARIABLE NO DECLARADA ---
    # Codigo original simulado:
    # x = 100; (Sin declaracion previa)
    ast_fantasma = NodoPrograma([
        NodoAsignacion("x", NodoNumero(100))
    ])
    


    print("\nESCENARIO 3: DETECCION DE VARIABLE NO DECLARADA")
    analizador_3 = AnalizadorSemantico()
    try:
        analizador_3.analizar(ast_fantasma)
    except Exception as e:
        print(e)