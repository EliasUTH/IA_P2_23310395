from collections import deque

class Grafo:
    def __init__(self):
        self.grafo = {}

    def agregar_arista(self, u, v):
        if u not in self.grafo:
            self.grafo[u] = []
        if v not in self.grafo:
            self.grafo[v] = []
        self.grafo[u].append(v)
        self.grafo[v].append(u)  

def busqueda_bidireccional(grafo, start, goal):
    if start == goal:
        return [start]

    visitados_start = set([start])
    visitados_goal = set([goal])

    cola_start = deque([(start, [start])])  
    cola_goal = deque([(goal, [goal])])

    padres_start = {start: None}
    padres_goal = {goal: None}

    while cola_start and cola_goal:
        if cola_start:
            nodo_actual, camino_actual = cola_start.popleft()
            for vecino in grafo.get(nodo_actual, []):
                if vecino not in visitados_start:
                    visitados_start.add(vecino)
                    padres_start[vecino] = nodo_actual
                    nuevo_camino = camino_actual + [vecino]
                    cola_start.append((vecino, nuevo_camino))
                    if vecino in visitados_goal:
                        camino_goal = []
                        actual = vecino
                        while actual is not None:
                            camino_goal.append(actual)
                            actual = padres_goal[actual]
                        camino_goal.reverse()
                        return camino_actual + camino_goal[1:]  

        if cola_goal:
            nodo_actual, camino_actual = cola_goal.popleft()
            for vecino in grafo.get(nodo_actual, []):
                if vecino not in visitados_goal:
                    visitados_goal.add(vecino)
                    padres_goal[vecino] = nodo_actual
                    nuevo_camino = camino_actual + [vecino]
                    cola_goal.append((vecino, nuevo_camino))
                    if vecino in visitados_start:
                        camino_start = []
                        actual = vecino
                        while actual is not None:
                            camino_start.append(actual)
                            actual = padres_start[actual]
                        camino_start.reverse()
                        return camino_start + camino_actual[1:]  
    return None  


# Ejemplo de uso
if __name__ == "__main__":
    g = Grafo()
    g.agregar_arista('A', 'B')
    g.agregar_arista('A', 'C')
    g.agregar_arista('B', 'D')
    g.agregar_arista('B', 'E')
    g.agregar_arista('C', 'F')
    g.agregar_arista('D', 'G')
    g.agregar_arista('E', 'G')
    g.agregar_arista('F', 'G')

    start = 'A'
    goal = 'G'
    camino = busqueda_bidireccional(g.grafo, start, goal)
    if camino:
        print(f"Camino encontrado: {' -> '.join(camino)}")
    else:
        print("No se encontró un camino.")