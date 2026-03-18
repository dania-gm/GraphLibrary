import random
from nodo import Nodo
from grafo import Grafo

def grafoGilbert(n, p):
    g = Grafo()
    
    # 2. Crear n nodos
    nodos_lista = []
    for i in range(n):
        nodo_id = f'nodo_{i}'
        nod = Nodo(nodo_id)
        g.add_nodo(nod)
        nodos_lista.append(nod)
    
    # 3. Iterar sobre todos los pares posibles
    # Usamos dos bucles para comparar cada nodo con los siguientes
    for i in range(n):
        for j in range(i + 1, n):
            # 4. Generar probabilidad aleatoria
            probabilidad = random.random()
            
            # 5. Si la probabilidad es menor a p, crear arista
            if probabilidad < p:
                g.add_arista(nodos_lista[i], nodos_lista[j], 'Undirected')
                
    return g
