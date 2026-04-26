import heapq

# Representación del grafo como diccionario de diccionarios (nodo: {vecino: costo})
grafo = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 2, 'E': 5},
    'C': {'F': 3},
    'D': {},
    'E': {'F': 1},
    'F': {}
}

def busqueda_costo_uniforme(grafo, inicio, objetivo):
    # Cola de prioridad: (costo_acumulado, nodo)
    cola_prioridad = [(0, inicio)]
    # Diccionario de costos mínimos conocidos
    costo_minimo = {inicio: 0}
    # Diccionario para rastrear el camino
    padre = {inicio: None}

    while cola_prioridad:
        # Extraer el nodo con el menor costo
        costo_actual, nodo_actual = heapq.heappop(cola_prioridad)

        # Si ya encontramos un costo mayor, ignorar
        if costo_actual > costo_minimo.get(nodo_actual, float('inf')):
            continue

        # Si encontramos el objetivo, reconstruir el camino
        if nodo_actual == objetivo:
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = padre[nodo_actual]
            camino.reverse()
            return camino, costo_actual

        # Explorar los vecinos
        for vecino, costo_arista in grafo[nodo_actual].items():
            costo_nuevo = costo_actual + costo_arista
            if costo_nuevo < costo_minimo.get(vecino, float('inf')):
                costo_minimo[vecino] = costo_nuevo
                padre[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (costo_nuevo, vecino))

    # Si no se encuentra el objetivo
    return None, float('inf')

# Ejemplo de uso
inicio = 'A'
objetivo = 'F'
camino, costo = busqueda_costo_uniforme(grafo, inicio, objetivo)
if camino:
    print(f"Camino encontrado: {' -> '.join(camino)}")
    print(f"Costo total: {costo}")
else:
    print("No se encontró un camino al objetivo.")
