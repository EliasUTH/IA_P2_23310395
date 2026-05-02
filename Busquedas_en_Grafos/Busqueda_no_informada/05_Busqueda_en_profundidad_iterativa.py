# Búsqueda en profundidad iterativa (IDDFS) en grafos

grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite):
    """Función auxiliar DLS"""
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

def busqueda_profundidad_iterativa(grafo, inicio, objetivo, max_profundidad=10):
    for limite in range(max_profundidad + 1):
        camino = busqueda_profundidad_limitada(grafo, inicio, objetivo, limite)
        if camino:
            return camino, limite
    return None, None

if __name__ == '__main__':
    inicio = 'A'
    objetivo = 'F'
    camino, profundidad = busqueda_profundidad_iterativa(grafo, inicio, objetivo)

    if camino:
        print(f"Camino encontrado: {' -> '.join(camino)}")
        print(f"Profundidad: {profundidad}")
    else:
        print("No se encontró un camino al objetivo.")
