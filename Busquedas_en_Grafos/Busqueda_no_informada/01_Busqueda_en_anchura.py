from collections import deque

grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

def busqueda_en_anchura(grafo, inicio, objetivo):

    cola = deque([inicio])
    visitados = set([inicio])
    padre = {inicio: None}

    while cola:
        nodo_actual = cola.popleft()

        if nodo_actual == objetivo:
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = padre[nodo_actual]
            camino.reverse()
            return camino

        for vecino in grafo[nodo_actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
                padre[vecino] = nodo_actual

    return None

inicio = 'A'
objetivo = 'F'
camino = busqueda_en_anchura(grafo, inicio, objetivo)
if camino:
    print(f"Camino encontrado: {' -> '.join(camino)}")
else:
    print("No se encontró un camino al objetivo.")
