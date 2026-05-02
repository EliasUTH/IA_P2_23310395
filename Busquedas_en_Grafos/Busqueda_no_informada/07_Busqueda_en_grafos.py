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

def bfs(grafo, start, goal):
    visitados = set()
    cola = deque([(start, [start])])

    while cola:
        nodo_actual, camino = cola.popleft()
        if nodo_actual == goal:
            return camino
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            for vecino in grafo.get(nodo_actual, []):
                if vecino not in visitados:
                    cola.append((vecino, camino + [vecino]))

    return None

def dfs(grafo, start, goal, visitados=None, camino=None):
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []

    visitados.add(start)
    camino.append(start)

    if start == goal:
        return camino[:]

    for vecino in grafo.get(start, []):
        if vecino not in visitados:
            resultado = dfs(grafo, vecino, goal, visitados, camino)
            if resultado:
                return resultado

    camino.pop()
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

    print("BFS:")
    camino_bfs = bfs(g.grafo, start, goal)
    if camino_bfs:
        print(f"Camino: {' -> '.join(camino_bfs)}")
    else:
        print("No encontrado")

    print("DFS:")
    camino_dfs = dfs(g.grafo, start, goal)
    if camino_dfs:
        print(f"Camino: {' -> '.join(camino_dfs)}")
    else:
        print("No encontrado")