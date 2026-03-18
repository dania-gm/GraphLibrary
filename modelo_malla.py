from nodo import Nodo
from grafo import Grafo

def generar_malla(filas, columnas):
    grafo = Grafo()
    for m in range(filas):
        for n in range(columnas):
            nodo_id = f'nodo_{m}_{n}'
            nod = Nodo(nodo_id)
            grafo.add_nodo(nod)
    
    for m in range(filas):
        for n in range(columnas):
            nodo_actual = grafo.nodos[f'nodo_{m}_{n}']
            
            if n < columnas - 1:
                nodo_derecha = grafo.nodos[f'nodo_{m}_{n+1}']
                grafo.add_arista(nodo_actual, nodo_derecha, 'Undirected')

            if m < filas - 1:
                nodo_abajo = grafo.nodos[f'nodo_{m+1}_{n}']
                grafo.add_arista(nodo_actual, nodo_abajo, 'Undirected')
    return grafo
