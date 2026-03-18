import random
import math
from nodo import Nodo
from grafo import Grafo

def grafoGeografico(n, r):
    g = Grafo()
    
    # 2. Crear n nodos con coordenadas aleatorias en [0, 1] x [0, 1]
    nodos_lista = []
    for i in range(n):
        nodo_id = f'nodo_{i}'
        nod = Nodo(nodo_id)
        # Asignar coordenadas aleatorias uniformes
        nod.atr['x'] = random.uniform(0, 1)
        nod.atr['y'] = random.uniform(0, 1)
        g.add_nodo(nod)
        nodos_lista.append(nod)
    
    # 3. Iterar sobre todos los pares posibles y calcular distancia
    for i in range(n):
        for j in range(i + 1, n):
            nodo_i = nodos_lista[i]
            nodo_j = nodos_lista[j]
            
            # 4. Calcular distancia euclidiana
            dx = nodo_i.atr['x'] - nodo_j.atr['x']
            dy = nodo_i.atr['y'] - nodo_j.atr['y']
            distancia = math.sqrt(dx**2 + dy**2)
            
            # 5. Si la distancia es <= r, crear arista
            if distancia <= r:
                g.add_arista(nodo_i, nodo_j, 'Undirected')
                
    return g
