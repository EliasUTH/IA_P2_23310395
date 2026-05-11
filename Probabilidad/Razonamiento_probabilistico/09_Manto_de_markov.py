print("=== RED BAYESIANA: EL MANTO DE MARKOV ===\n")

# 1. Definimos la estructura de la Red Bayesiana (El Grafo)
# Nublado -> Aspersor
# Nublado -> Lluvia
# Aspersor -> Pasto_Mojado
# Lluvia -> Pasto_Mojado

# Diccionario de Padres (Causas de cada nodo)
padres = {
    "Nublado": [],
    "Aspersor": ["Nublado"],
    "Lluvia": ["Nublado"],
    "Pasto_Mojado": ["Aspersor", "Lluvia"]
}

# Diccionario de Hijos (Efectos de cada nodo)
hijos = {
    "Nublado": ["Aspersor", "Lluvia"],
    "Aspersor": ["Pasto_Mojado"],
    "Lluvia": ["Pasto_Mojado"],
    "Pasto_Mojado": []
}

def obtener_manto_de_markov(nodo_objetivo):
    """
    Encuentra el Manto de Markov de un nodo específico en la red.
    Consiste en: Sus Padres, sus Hijos, y los Padres de sus Hijos (Co-padres).
    """
    # 1. Obtener los Padres
    manto_padres = set(padres[nodo_objetivo])
    
    # 2. Obtener los Hijos
    manto_hijos = set(hijos[nodo_objetivo])
    
    # 3. Obtener los Co-padres (Cónyuges)
    # Buscamos quiénes más son padres de los hijos de nuestro nodo
    manto_copadres = set()
    for hijo in manto_hijos:
        for padre_del_hijo in padres[hijo]:
            # No nos queremos agregar a nosotros mismos como co-padres
            if padre_del_hijo != nodo_objetivo:
                manto_copadres.add(padre_del_hijo)
                
    # Unir todo el manto
    manto_total = manto_padres.union(manto_hijos).union(manto_copadres)
    
    return manto_padres, manto_hijos, manto_copadres, manto_total

# --- ESCENARIO DE EXTRACCIÓN DEL MANTO ---


# Queremos analizar el nodo "Aspersor"
nodo_a_analizar = "Aspersor"

print(f"Analizando el Manto de Markov para el nodo: [{nodo_a_analizar}]\n")

p, h, cp, manto_completo = obtener_manto_de_markov(nodo_a_analizar)

print("1. Padres (Causas del Aspersor):")
print(f"   -> {p if p else 'Ninguno'}")

print("2. Hijos (Efectos del Aspersor):")
print(f"   -> {h if h else 'Ninguno'}")

print("3. Co-padres (Otras causas del Pasto Mojado):")
print(f"   -> {cp if cp else 'Ninguno'}\n")

print(f"=== MANTO DE MARKOV COMPLETO DE '{nodo_a_analizar}' ===")
print(list(manto_completo))
print("\nConclusión de la IA:")
print(f"Si la IA conoce exactamente el estado de {list(manto_completo)},")
print(f"entonces cualquier otro nodo que agreguemos a la red en el futuro")
print(f"será matemáticamente IRRELEVANTE para predecir el estado del '{nodo_a_analizar}'.")