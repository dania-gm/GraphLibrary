from node import Node
from edge import Edge
from collections import deque
import random
import heapq

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
    
    def add_edge(self,n0_id,n1_id, peso=None):
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
        
        if peso is None:
            peso = random.randint(1,50)
        
        arista = Edge(edge_id,n0,n1,self.tipo,peso)
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
    
    def BFS(self, s):
        """
        Ejecuta la Búsqueda en Anchura (BFS) desde el nodo 's'
        y devuelve un nuevo objeto Graph que representa el árbol BFS.
        """
        # 1. Crear el nuevo grafo resultante
        g_bfs = Graph(self.tipo)
        
        # Validar que el nodo inicial exista
        if s not in self.nodes:
            return g_bfs
            
        visitados = {s}
        # La cola guarda tuplas: (nodo_actual, padre, nivel)
        cola = deque([(s, None, 0)]) 
        
        dict_ady = self.dict_adyacencia() # Usamos tu método existente
        
        while cola:
            u, padre, nivel = cola.popleft()
            
            # 2. Añadir el nodo al árbol BFS
            g_bfs.add_node(u)
            g_bfs.nodes[u].nivel = nivel
            
            # (Opcional) Copiar las coordenadas originales para que el .dot se vea igual
            if u in self.nodes:
                g_bfs.nodes[u].position = self.nodes[u].position.copy()
            
            # 3. Si venimos de un padre, CREAR LA ARISTA oficialmente
            if padre is not None:
                # Esto asegura que g_bfs.edges se llene correctamente
                g_bfs.add_edge(padre, u) 
                
            # Explorar vecinos
            for vecino in dict_ady.get(u, []):
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append((vecino, u, nivel + 1))
                    
        return g_bfs              
        
    def DFS_R(self,s):
        visitado = set()
        aristas_dfs = []
        dict_ady = self.dict_adyacencia()
        niveles = {}
        def dfs_recursivo(u,nivel_actual=0):
            visitado.add(u)
            niveles[u]= nivel_actual
            for vecino in dict_ady.get(u,[]):
                if vecino not in visitado:
                    aristas_dfs.append((u,vecino))
                    dfs_recursivo(vecino, nivel_actual + 1)
        
        if s is not None and s in self.nodes:
            dfs_recursivo(s)
            
        dfs_adj = {n:[] for n in visitado}
        for u,v in aristas_dfs:
            dfs_adj[u].append(v)
            if self.tipo == 'Undirected':
                dfs_adj[v].append(u)
                
        g = Graph.to_grafo(dfs_adj,self.tipo)
        for nodo in g.nodes.values():
            nodo.nivel = niveles.get(nodo.id, -1)

        return g   
            
    
    def DFS_I(self,s):
        g_dfs_i = Graph(self.tipo)
        if s is None or s not in self.nodes:
            return g_dfs_i
        
        visitado = set()
        dict_ady = self.dict_adyacencia()    
        pila = [(s, None, 0)]
        
        while pila:
            u, padre, nivel_actual = pila.pop()
            if u not in visitado:
                visitado.add(u)
                g_dfs_i.add_node(u)
                g_dfs_i.nodes[u].nivel = nivel_actual
                    
                if u is not None:
                    g_dfs_i.nodes[u].position = self.nodes[u].position.copy()

                if padre is not None:
                    g_dfs_i.add_edge(padre, u)
                
                for vecino in reversed(dict_ady.get(u, [])):
                    if vecino not in visitado:
                        pila.append((vecino, u, nivel_actual + 1))
                        
        return g_dfs_i
    
    def Dijkstra(self,s):
        g_dijkstra = Graph(self.tipo)
        if s is None or s not in self.nodes:
            return g_dijkstra
        q = []
        S = set()
        distancias = {}
        padres = {}
        
        for n in self.nodes:
            distancias[n] = float('inf')
            padres[n] = None
            
        distancias[s] = 0
        heapq.heappush(q,(0,s))
        while q:
            d_u, u = heapq.heappop(q)
            
            if u in S:
                continue
            
            S.add(u)
            
            vecinos = self.dict_adyacencia().get(u, [])
            for v in vecinos:
                

                if v not in S:

                    if self.tipo == 'Undirected':
                        edge_id = f'{min(u, v)}--{max(u, v)}'
                    else:
                        edge_id = f'{u}--{v}'
                        
                    arista = self.edges.get(edge_id)
                    l_e = getattr(arista, "peso", 1) if arista else 1

                   
                    if distancias[v] > distancias[u] + l_e:
                        distancias[v] = distancias[u] + l_e
                        padres[v] = u
                    
                        heapq.heappush(q, (distancias[v], v))


        mapeo_nombres = {}
        for nodo_id in S:
            d_val = distancias[nodo_id]
            nuevo_nombre = f"{nodo_id} ({d_val:.2f})"
            mapeo_nombres[nodo_id] = nuevo_nombre
            
        for nodo_id in S:
            nuevo_id = mapeo_nombres[nodo_id]
            g_dijkstra.add_node(nuevo_id)
            g_dijkstra.nodes[nuevo_id].distancia = distancias[nodo_id]
            

            if nodo_id in self.nodes:
                g_dijkstra.nodes[nuevo_id].position = self.nodes[nodo_id].position.copy()

        for nodo_id in S:
            padre = padres[nodo_id]
            if padre is not None:
                id_hijo_con_dist = mapeo_nombres[nodo_id]
                id_padre_con_dist = mapeo_nombres[padre]
                
                if self.tipo == 'Undirected':
                    edge_id_original = f'{min(padre, nodo_id)}--{max(padre, nodo_id)}'
                else:
                    edge_id_original = f'{padre}--{nodo_id}'
                
                arista_orig = self.edges.get(edge_id_original)
                peso_original = getattr(arista_orig, "peso", 1) if arista_orig else 1
                
  
                g_dijkstra.add_edge(id_padre_con_dist, id_hijo_con_dist, peso=peso_original)

        return g_dijkstra
        