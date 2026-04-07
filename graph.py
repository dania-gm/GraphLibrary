from node import Node
from edge import Edge

from typing import Dict
from collections import Counter

class Graph:
    def __init__(self,tipo='Undirected'):
        self.nodes : Dict[str, Node] = {}
        self.edges : Dict[str, Edge] = {}
        self.tipo = tipo
        
    def add_node(self,node_id):
        if node_id in self.nodes:
            return False
        self.nodes[node_id] = Node(node_id)
        return True
    
    def add_edge(self,n0_id,n1_id):
        if n0_id not in self.nodes or n1_id not in self.nodes:
            raise ValueError('Ambos nodos deben existir antes de crear la arista')
        
        n0 = self.nodes[n0_id]
        n1 = self.nodes[n1_id]
        
        if self.tipo == 'Undirected':
            edge_id = f'{min(n0_id,n1_id)}--{max(n0_id,n1_id)}'
        else:
            edge_id = f'{n0_id}--{n1_id}'
            
        if edge_id in self.edges:
            return False
        
        arista = Edge(edge_id,n0,n1,self.tipo)
        self.edges[edge_id] = arista
        
        n0.add_edge_ref(arista)
        if self.tipo == 'Undirected':
            n1.add_edge_ref(arista)
        return True
    
    def get_orden(self):
        return f'Grafo de orden: {len(self.nodes)}'

    def __str__(self):
        if self.tipo == 'Directed':
            flecha = '-->'
        elif self.tipo == 'Undirected':
            flecha = '--'
        else:
            raise ValueError(f"Tipo de grafo no soportado: {self.tipo}")
        
        lineas = [
            'Grafo',
            f'Orden: {self.get_orden()}',
            ''
        ]
        for e in self.edges.values():
                lineas.append(f'{e.n0}{flecha}{e.n1}')
        return '\n'.join(lineas)

                