import streamlit as st
from graph import Graph
import random
import math
from itertools import combinations, permutations

@st.cache_data
def generar_erdos_renyi(n, m, tipo):
    #Validar entradas
    if n < 1 or m < 0:
        raise ValueError('n debe ser >= 1 y m>= 0')
    max_edges = 0
    if tipo=='Directed':
        max_edges=n*(n-1)
    elif tipo=='Undirected':
        max_edges= n*(n-1)//2
    else:
        raise ValueError(f"Tipo de grafo no soportado: {tipo}")
    
    if m > max_edges:
        raise ValueError(f'm excede el máximo posible de aristas ({max_edges})')
    
    g = Graph(tipo)
    #Crear n vertices 
    for i in range(1,n+1):
        g.add_node(i)
    #Generar m aristas
    edges_added = set()
    while len(edges_added) < m:
        n1 = random.randint(1,n)
        n2 = random.randint(1,n)
        if n1 == n2:
            continue
        edge = (min(n1,n2), max(n1,n2)) if tipo=='Undirected' else (n1,n2)
        if edge not in edges_added:
            edges_added.add(edge)
            g.add_edge(n1,n2)
    return g

def generar_gilbert(n,p,tipo):
    if not (0.0 <= p <= 1.0):
        raise ValueError('p debe estar entre 0.0 y 1.0')
    g = Graph(tipo)

    for i in range(1,n+1):
        g.add_node(i)
    
    if tipo == 'Undirected':
        parejas = combinations(range(1, n+1), 2)
    else:
        parejas = permutations(range(1,n+1), 2)
        
    for u,v in parejas:
        if random.random() <= p:
            g.add_edge(u,v)
    
    return g
    
def generar_geografico_simple(n,r,tipo):
    if r <= 0.0:
        raise ValueError('r debe ser mayor a 0.0')
    if r > math.sqrt(2):
        raise ValueError('r no puede exceder la diagonal del cuadrado unitario')
    
    g = Graph(tipo)
    
    for i in range(1,n+1):
        g.add_node(i)
        
    #ubicar nodos
    for nodo in g.nodes.values():
        nodo.position['x'] = random.uniform(0,1)
        nodo.position['y'] = random.uniform(0,1)
    
    nodos_lista = list(g.nodes.values())
    total = len(nodos_lista)
    
    for i in range(total):
        n_1 = nodos_lista[i]
        x_1, y_1 = n_1.position['x'], n_1.position['y']
        
        for j in range(i+1, total):
           n_2 = nodos_lista[j] 
           dx = n_2.position['x'] - x_1
           dy = n_2.position['y'] - y_1
           d = math.sqrt(dx**2 + dy**2)
           if d <= r:
               g.add_edge(n_1.id,n_2.id)
               if tipo == 'Directed':
                   g.add_edge(n_2.id,n_1.id)
    return g

def generar_malla(n,m,tipo):
    if n<1 or m<1:
        raise ValueError('n y m deben ser >=1')
    g = Graph(tipo)
    
    for i in range(n):
        for j in range(m):
            node_id = i * m + j + 1
            g.add_node(node_id)
            g.nodes[node_id].position['x'] = j/(m-1) if m>1 else 0.5
            g.nodes[node_id].position['y'] = i/(n-1) if n>1 else 0.5
            
    # 8 direcciones
    direcciones = [(-1,-1), (-1,0), (-1,1),
                   (0,-1),          (0,1),
                   (1,-1),  (1,0),  (1,1)]
    
    # Conectar cada nodo con sus vecinos válidos
    for i in range(n):
        for j in range(m):
            node_id = i * m + j + 1
            for di, dj in direcciones:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m:
                    neighbor_id = ni * m + nj + 1
                    if node_id < neighbor_id:
                        g.add_edge(node_id, neighbor_id)
                        if tipo == 'Directed':
                            g.add_edge(neighbor_id, node_id)
    
    return g

    