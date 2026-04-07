import random
from node import Nodo
from graph import Grafo

def grafoBarabasiAlbert(n, d):
    if d >= n:
        raise ValueError("d debe ser menor que n")
    
    g = Grafo()
    nodo_id = f'nodo_{0}'
    nod = Nodo(nodo_id)
    g.add_nodo(nod)
    
    for u in range(1,n):
        nodo_id = f'nodo_{u}'
        nuevo_nodo = Nodo(nodo_id)
        g.add_nodo(nuevo_nodo)
        
        randomNodos = g.randomArray(u)
        for v in range(u):
            nodo_id = f'nodo_{randomNodos[v]}'
            nodo_destino = Nodo(nodo_id)
            g.add_nodo(nodo_destino)
            deg = g.get_grado(nodo_destino)
            
        p = 1 - deg / d
        
        if random.random() < p:
            if randomNodos[v] != u:
                g.add_arista(nuevo_nodo, nodo_destino, 'Undirected')

    return g