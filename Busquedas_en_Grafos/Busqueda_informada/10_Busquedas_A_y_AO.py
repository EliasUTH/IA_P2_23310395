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

# AO* simplificado para grafos AND-OR (ejemplo básico)
class NodoAO:
    def __init__(self, nombre, tipo='OR', hijos=None):
        self.nombre = nombre
        self.tipo = tipo  # 'OR' o 'AND'
        self.hijos = hijos or []  
        self.costo = float('inf')
        self.solucion = None

def ao_estrella(raiz, heuristica_func):
    # Simplificación: asume grafo pequeño
    def evaluar(nodo):
        if not nodo.hijos:
            nodo.costo = heuristica_func(nodo.nombre)
            nodo.solucion = [nodo.nombre]
            return

        if nodo.tipo == 'OR':
            min_costo = float('inf')
            mejor_sol = None
            for hijo in nodo.hijos:
                evaluar(hijo)
                if hijo.costo < min_costo:
                    min_costo = hijo.costo
                    mejor_sol = hijo.solucion
            nodo.costo = min_costo
            nodo.solucion = [nodo.nombre] + (mejor_sol or [])
        elif nodo.tipo == 'AND':
            total_costo = 0
            sol = [nodo.nombre]
            for sublista in nodo.hijos:
                min_sub = float('inf')
                mejor_sub = None
                for hijo in sublista:
                    evaluar(hijo)
                    if hijo.costo < min_sub:
                        min_sub = hijo.costo
                        mejor_sub = hijo.solucion
                total_costo += min_sub
                sol.extend(mejor_sub or [])
            nodo.costo = total_costo
            nodo.solucion = sol

    evaluar(raiz)
    return raiz.solucion, raiz.costo

# Ejemplo de uso
if __name__ == "__main__":
    # A*
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
    print("A*:")
    if camino:
        print(f"Camino: {' -> '.join(camino)}, Costo: {costo}")
    else:
        print("No encontrado")

    # AO* ejemplo simple
    def heur(nodo):
        return heuristica(nodo, 'G')

    # Construir grafo AND-OR
    g_node = NodoAO('G')
    f_node = NodoAO('F')
    e_node = NodoAO('E')
    d_node = NodoAO('D')
    c_node = NodoAO('C', 'AND', [[f_node]])  # AND con F
    b_node = NodoAO('B', 'OR', [d_node, e_node])  # OR con D o E
    a_node = NodoAO('A', 'OR', [b_node, c_node])  # OR con B o C

    sol, cost = ao_estrella(a_node, heur)
    print("AO*:")
    if sol:
        print(f"Solución: {' -> '.join(sol)}, Costo: {cost}")
    else:
        print("No encontrado")