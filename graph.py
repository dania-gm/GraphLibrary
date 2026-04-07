from node import Node
from edge import Edge
from collections import deque

from typing import Dict

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
    
    
    def dict_adyacencia(self):
        dict_ady = {node_id: [] for node_id in self.nodes}
        for e in self.edges.values():
            u = e.n0.id if isinstance(e.n0, Node) else e.n0
            v = e.n1.id if isinstance(e.n1, Node) else e.n1
            
            #dirigido
            dict_ady.setdefault(u,[]).append(v)
            
            #no dirigido
            if self.tipo == 'Undirected':
                dict_ady.setdefault(v,[]).append(u)
                
        return dict_ady
    
    @staticmethod
    def to_grafo(adyacencia,tipo='Undirected'):
        gn = Graph(tipo)
        nodos_id = set(adyacencia.keys())
        for vecinos in adyacencia.values():
            nodos_id.update(vecinos)
            
        for n in nodos_id:
            gn.add_node(n)
            
        vistas_edges = set()
            
        for u, vecinos in adyacencia.items():
            for v in vecinos:
                #no dirigidos
                par = tuple(sorted([u,v])) if tipo=='Undirected' else (u,v)
                
                if par not in vistas_edges:
                    n0 = gn.nodes[u].id
                    n1 = gn.nodes[v].id
                    gn.add_edge(n0,n1)
                    vistas_edges.add(par)
        return gn
    
    def BFS(self,s):
        dict_ady = self.dict_adyacencia()
        visitado = set()
        nivel = {}
        cola = deque([s])
        visitado.add(s)
        nivel[s] = 0
        
        while cola: #este llena
            n = cola.popleft()
            #recorrer vecinos no visitados
            for vecino in dict_ady.get(n,[]):
                if vecino not in visitado:
                    visitado.add(vecino)
                    cola.append(vecino)
                    nivel[vecino] = nivel[n] + 1
        g = Graph.to_grafo(dict_ady,self.tipo)
        for nodo in g.nodes.values():
            nodo.nivel = nivel.get(nodo.id, -1)
            
        for nodo in g.nodes.values():
            print(nodo.id, nodo.nivel)
        return g               
        
                      
        
    
    def DFS_R(self,s):
        pass
    
    def DFS_I(self,s):
        pass        