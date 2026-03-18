import random
from nodo import Nodo
from arista import Arista
from grafo import Grafo

def grafoDorogovtsevMendes(n, dirigido=False):
    """
    Genera grafo aleatorio con el modelo Dorogovtsev-Mendes
    :param n: número de nodos (≥ 3)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    # Validar parámetros
    if n < 3:
        raise ValueError("n debe ser al menos 3 para formar el triángulo inicial")
    
    # 1. Crear el grafo base
    g = Grafo(direccionado=dirigido)
    
    # 2. Crear los 3 nodos iniciales
    nodos_lista = []
    for i in range(3):
        nodo_id = f'nodo_{i}'
        nod = Nodo(nodo_id)
        g.add_nodo(nod)
        nodos_lista.append(nod)
    
    # 3. Crear el triángulo inicial (3 aristas)
    g.add_arista(nodos_lista[0], nodos_lista[1], 'Undirected')
    g.add_arista(nodos_lista[1], nodos_lista[2], 'Undirected')
    g.add_arista(nodos_lista[2], nodos_lista[0], 'Undirected')
    
    # 4. Agregar nodos restantes (desde 3 hasta n-1)
    for i in range(3, n):
        # Crear nuevo nodo
        nodo_id = f'nodo_{i}'
        nuevo_nodo = Nodo(nodo_id)
        g.add_nodo(nuevo_nodo)
        nodos_lista.append(nuevo_nodo)
        
        # 5. Seleccionar una arista al azar de las existentes
        aristas_lista = list(g.aristas.values())
        arista_seleccionada = random.choice(aristas_lista)
        
        # 6. Conectar el nuevo nodo a ambos extremos de la arista seleccionada
        nodo_extremo1 = g.nodos[arista_seleccionada.n0]
        nodo_extremo2 = g.nodos[arista_seleccionada.n1]
        
        g.add_arista(nuevo_nodo, nodo_extremo1, 'Undirected')
        g.add_arista(nuevo_nodo, nodo_extremo2, 'Undirected')
    
    return g
