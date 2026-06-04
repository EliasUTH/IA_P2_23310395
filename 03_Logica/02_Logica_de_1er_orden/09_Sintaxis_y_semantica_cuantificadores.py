print("=== LÓGICA DE PRIMER ORDEN: SINTAXIS Y CUANTIFICADORES ===\n")
# --- 1. SINTAXIS: EL DOMINIO (El Universo de Discurso) ---
# En FOL, no podemos razonar en el vacío. Necesitamos un "Universo" de objetos.
universo = [
    {"nombre": "Sócrates",   "es_humano": True,  "es_mortal": True,  "es_dios": False},
    {"nombre": "Platón",     "es_humano": True,  "es_mortal": True,  "es_dios": False},
    {"nombre": "Zeus",       "es_humano": False, "es_mortal": False, "es_dios": True},
    {"nombre": "Bucéfalo",   "es_humano": False, "es_mortal": True,  "es_dios": False} # Un caballo
]




# --- 2. SINTAXIS: PREDICADOS ---
# Un predicado es una función que toma un objeto y devuelve Verdadero o Falso.
def Humano(x): return x["es_humano"]
def Mortal(x): return x["es_mortal"]
def Dios(x):   return x["es_dios"]

def IMPLICA(p, q):
    """Condicional material: p => q"""
    return (not p) or q



# --- 3. SEMÁNTICA: CUANTIFICADORES ---
# Evaluamos oraciones lógicas complejas iterando sobre nuestro universo.
print("Evaluando sentencias en el Universo Griego...\n")
# SENTENCIA A: "Todos los humanos son mortales"
# Formalización: ∀x (Humano(x) => Mortal(x))
# Semántica en Python: Usamos all() que representa el cuantificador Universal (∀)
sentencia_a = all(IMPLICA(Humano(x), Mortal(x)) for x in universo)
print("A) ¿Todos los humanos son mortales? ∀x (Humano(x) => Mortal(x))")
print(f"   -> {'VERDADERO' if sentencia_a else 'FALSO'}")




# SENTENCIA B: "Todos en el universo son inmortales"
# Formalización: ∀x (NOT Mortal(x))
sentencia_b = all(not Mortal(x) for x in universo)
print("\nB) ¿Todos en el universo son inmortales? ∀x (~Mortal(x))")
print(f"   -> {'VERDADERO' if sentencia_b else 'FALSO'}")




# SENTENCIA C: "Existe al menos un Dios"
# Formalización: ∃x (Dios(x))
# Semántica en Python: Usamos any() que representa el cuantificador Existencial (∃)
sentencia_c = any(Dios(x) for x in universo)
print("\nC) ¿Existe al menos un Dios? ∃x (Dios(x))")
print(f"   -> {'VERDADERO' if sentencia_c else 'FALSO'}")




# SENTENCIA D: "Existe algún humano que no sea mortal"
# Formalización: ∃x (Humano(x) AND NOT Mortal(x))
sentencia_d = any(Humano(x) and not Mortal(x) for x in universo)
print("\nD) ¿Existe algún humano inmortal? ∃x (Humano(x) ^ ~Mortal(x))")
print(f"   -> {'VERDADERO' if sentencia_d else 'FALSO'}")
print("\n=== ANÁLISIS TÉCNICO ===")
print("1. El Dominio: A diferencia de la lógica proposicional, aquí iteramos sobre un conjunto de datos reales.")
print("2. Cuantificador Universal (∀): Se implementa con 'all()'. Solo retorna True si la condición es cierta para TODO objeto.")
print("3. Cuantificador Existencial (∃): Se implementa con 'any()'. Retorna True al encontrar el PRIMER objeto que cumpla la regla.")