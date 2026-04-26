# Búsqueda en profundidad (DFS) en grafos

# Representación del grafo como diccionario de listas de adyacencia
grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}


def busqueda_en_profundidad(grafo, inicio, objetivo):
    camino = []
    visitados = set()

    def dfs(nodo_actual):
        if nodo_actual in visitados:
            return False

        visitados.add(nodo_actual)
        camino.append(nodo_actual)

        if nodo_actual == objetivo:
            return True

        for vecino in grafo.get(nodo_actual, []):
            if dfs(vecino):
                return True

        camino.pop()
        return False

    encontrado = dfs(inicio)
    return camino if encontrado else None


if __name__ == '__main__':
    inicio = 'A'
    objetivo = 'F'
    camino = busqueda_en_profundidad(grafo, inicio, objetivo)

    if camino:
        print(f"Camino encontrado: {' -> '.join(camino)}")
    else:
        print("No se encontró un camino al objetivo.")
