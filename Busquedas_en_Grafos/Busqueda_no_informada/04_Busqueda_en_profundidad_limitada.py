# Búsqueda en profundidad limitada (DLS) en grafos
grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite):
    camino = []
    visitados = set()

    def dls(nodo_actual, profundidad):
        if profundidad > limite:
            return False

        if nodo_actual in visitados:
            return False

        visitados.add(nodo_actual)
        camino.append(nodo_actual)

        if nodo_actual == objetivo:
            return True

        for vecino in grafo.get(nodo_actual, []):
            if dls(vecino, profundidad + 1):
                return True

        camino.pop()
        visitados.remove(nodo_actual)  
        return False

    encontrado = dls(inicio, 0)
    return camino if encontrado else None


if __name__ == '__main__':
    inicio = 'A'
    objetivo = 'F'
    limite = 3  # Límite de profundidad
    camino = busqueda_profundidad_limitada(grafo, inicio, objetivo, limite)

    if camino:
        print(f"Camino encontrado: {' -> '.join(camino)}")
    else:
        print("No se encontró un camino al objetivo dentro del límite de profundidad.")
