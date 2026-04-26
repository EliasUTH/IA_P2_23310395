from collections import deque

# Representación del grafo como diccionario de listas de adyacencia
grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

def busqueda_en_anchura(grafo, inicio, objetivo):
    # Cola para los nodos a explorar
    cola = deque([inicio])
    # Conjunto de nodos visitados
    visitados = set([inicio])
    # Diccionario para rastrear el camino
    padre = {inicio: None}

    while cola:
        # Sacar el primer nodo de la cola
        nodo_actual = cola.popleft()

        # Si encontramos el objetivo, reconstruir el camino
        if nodo_actual == objetivo:
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = padre[nodo_actual]
            camino.reverse()
            return camino

        # Explorar los vecinos
        for vecino in grafo[nodo_actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
                padre[vecino] = nodo_actual

    # Si no se encuentra el objetivo
    return None

# Ejemplo de uso
inicio = 'A'
objetivo = 'F'
camino = busqueda_en_anchura(grafo, inicio, objetivo)
if camino:
    print(f"Camino encontrado: {' -> '.join(camino)}")
else:
    print("No se encontró un camino al objetivo.")
