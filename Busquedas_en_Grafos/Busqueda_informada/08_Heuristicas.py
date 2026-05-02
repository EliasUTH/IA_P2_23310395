import heapq

class Grafo:
    def __init__(self):
        self.grafo = {}

    def agregar_arista(self, u, v, costo):
        if u not in self.grafo:
            self.grafo[u] = []
        if v not in self.grafo:
            self.grafo[v] = []
        self.grafo[u].append((v, costo))
        self.grafo[v].append((u, costo)) 

def heuristica(nodo, goal):
    # Heurística simple: distancia euclidiana (asumiendo coordenadas)
    coordenadas = {
        'A': (0, 0), 'B': (1, 1), 'C': (2, 0), 'D': (3, 1),
        'E': (4, 0), 'F': (5, 1), 'G': (6, 0)
    }
    if nodo in coordenadas and goal in coordenadas:
        x1, y1 = coordenadas[nodo]
        x2, y2 = coordenadas[goal]
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    return 0

def a_estrella(grafo, start, goal):
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0 + heuristica(start, goal), 0, start, []))  # (f, g, nodo, camino)

    visitados = set()
    costo_minimo = {start: 0}

    while cola_prioridad:
        f, g, nodo_actual, camino = heapq.heappop(cola_prioridad)

        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        camino = camino + [nodo_actual]

        if nodo_actual == goal:
            return camino, g

        for vecino, costo in grafo.get(nodo_actual, []):
            nuevo_g = g + costo
            if vecino not in costo_minimo or nuevo_g < costo_minimo[vecino]:
                costo_minimo[vecino] = nuevo_g
                f_nuevo = nuevo_g + heuristica(vecino, goal)
                heapq.heappush(cola_prioridad, (f_nuevo, nuevo_g, vecino, camino))

    return None, float('inf')

# Ejemplo de uso
if __name__ == "__main__":
    g = Grafo()
    g.agregar_arista('A', 'B', 1)
    g.agregar_arista('A', 'C', 4)
    g.agregar_arista('B', 'D', 2)
    g.agregar_arista('B', 'E', 5)
    g.agregar_arista('C', 'F', 3)
    g.agregar_arista('D', 'G', 1)
    g.agregar_arista('E', 'G', 2)
    g.agregar_arista('F', 'G', 1)

    start = 'A'
    goal = 'G'
    camino, costo = a_estrella(g.grafo, start, goal)
    if camino:
        print(f"Camino óptimo: {' -> '.join(camino)}")
        print(f"Costo total: {costo}")
    else:
        print("No se encontró camino.")