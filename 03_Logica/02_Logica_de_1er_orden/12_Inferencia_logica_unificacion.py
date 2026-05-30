print("=== INFERENCIA EN 1ER ORDEN: UNIFICACIÓN LÓGICA ===\n")
# --- 1. REGLAS DE SINTAXIS ---
# Convención: 
# - Las Variables empiezan con minúscula (ej. 'x', 'y').
# - Las Constantes y Predicados/Funciones empiezan con Mayúscula (ej. 'Juan', 'Madre').
# - Las sentencias compuestas son tuplas (ej. ('Conoce', 'Juan', 'x')).



def es_variable(termino):
    """Verifica si un término es una variable lógica (empieza con minúscula)."""
    return isinstance(termino, str) and termino.islower()
def es_compuesto(termino):
    """Verifica si un término es una función o predicado (una tupla)."""
    return isinstance(termino, tuple)



# --- 2. EL PROBLEMA DE LA RECURSIÓN INFINITA (Occurs Check) ---
def ocurre_en(var, x, theta):
    """
    Verifica si la variable 'var' ocurre dentro del término 'x'.
    Previene asignaciones imposibles como x = f(x), que causarían bucles infinitos.
    """
    if var == x:
        return True
    elif es_compuesto(x):
        # Si es compuesto, buscamos en todos sus argumentos
        return any(ocurre_en(var, arg, theta) for arg in x)
    elif es_variable(x) and x in theta:
        # Si 'x' es una variable ya asignada, revisamos a qué está asignada
        return ocurre_en(var, theta[x], theta)
    return False



# --- 3. ALGORITMO CORE DE UNIFICACIÓN ---
def unificar_variable(var, x, theta):
    """Unifica una variable con otro término."""
    if var in theta:
        # Si la variable ya tiene un valor asignado, intentamos unificar ese valor con 'x'
        return unificar(theta[var], x, theta)
    elif es_variable(x) and x in theta:
        # Si 'x' es variable y ya tiene valor, unificamos 'var' con el valor de 'x'
        return unificar(var, theta[x], theta)
    elif ocurre_en(var, x, theta):
        # Fallo por la prueba de ocurrencia
        return None
    else:
        # ¡Éxito! Agregamos la nueva asignación al diccionario de sustituciones
        theta_nueva = theta.copy()
        theta_nueva[var] = x
        return theta_nueva



def unificar(x, y, theta={}):
    """
    Intenta encontrar una sustitución (theta) que haga que x e y sean idénticos.
    Retorna el diccionario de sustituciones o None si es imposible.
    """
    # Si ya falló en un paso anterior, propagamos el fallo
    if theta is None:
        return None
        


    # Si son exactamente iguales (ej. 'Juan' == 'Juan'), no hay nada que hacer
    elif x == y:
        return theta
        

    # Si el lado izquierdo es variable
    elif es_variable(x):
        return unificar_variable(x, y, theta)
        

    # Si el lado derecho es variable
    elif es_variable(y):
        return unificar_variable(y, x, theta)
        

    # Si ambos son términos compuestos (ej. Predicados o Funciones)
    elif es_compuesto(x) and es_compuesto(y) and len(x) == len(y):
        # Unificamos el primer elemento (ej. el nombre del predicado)
        theta_actualizada = unificar(x[0], y[0], theta)
        # Unificamos el resto de los argumentos recursivamente usando el theta actualizado
        return unificar(x[1:], y[1:], theta_actualizada)
    # Si chocan constantes diferentes (ej. 'Juan' unificando con 'Maria')
    else:
        return None



# --- 4. PRUEBAS DE LABORATORIO ---
def probar_unificacion(exp1, exp2):
    print(f"Unificando: {exp1}")
    print(f"       Con: {exp2}")
    resultado = unificar(exp1, exp2, {})
    if resultado is None:
        print("-> FALLO: Las expresiones son lógicamente incompatibles.\n")
    else:
        print(f"-> ÉXITO: Sustitución (Theta) = {resultado}\n")



print("--- CASO 1: Constante a Variable ---")
# ¿Quién conoce a Juan? -> Juan conoce a x.
probar_unificacion(("Conoce", "Juan", "x"), ("Conoce", "Juan", "Maria"))


print("--- CASO 2: Variable a Variable ---")
# Ambos conocen a alguien, forzamos a que x e y sean la misma persona.
probar_unificacion(("Conoce", "Juan", "x"), ("Conoce", "Juan", "y"))


print("--- CASO 3: Unificación Compleja con Funciones ---")
# Juan conoce a x. "y" conoce a la madre de "y".
# Para igualarlos, "y" debe ser Juan, y "x" debe ser la madre de Juan.
probar_unificacion(("Conoce", "Juan", "x"), ("Conoce", "y", ("Madre", "y")))


print("--- CASO 4: Fallo por Choque de Constantes ---")
# Intentar unificar a Juan con Pedro
probar_unificacion(("Conoce", "Juan", "x"), ("Conoce", "Pedro", "Maria"))


print("--- CASO 5: Fallo por el 'Occurs Check' ---")
# Intentar decir que 'x' es el padre de 'x' crea una paradoja recursiva.
probar_unificacion(("Padre", "x", "x"), ("Padre", "x", ("Padre", "x")))



print("=== ANÁLISIS TÉCNICO ===")
print("1. Sustitución (Theta): El diccionario resultante es la 'respuesta' a la consulta lógica.")
print("2. Occurs Check: Es la defensa del motor contra bucles infinitos. Matemáticamente, x no puede ser igual a f(x).")
print("3. Motor de Prolog: Este algoritmo de unificación, combinado con la resolución (Backtracking), es exactamente cómo funciona el lenguaje de programación lógica Prolog bajo el capó.")