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
    
    def KruskalD(self):
        if self.tipo != 'Undirected':
            raise ValueError('El algoritmo de Kruskal se aplica típicamente a grafos no dirigidos')
        
        mst_graph = Graph(tipo='Undirected')
        for node_id in self.nodes:
            mst_graph.add_node(node_id)
            
        parent = {node_id: node_id for node_id in self.nodes}
        rank = {node_id: 0 for node_id in self.nodes}
        
        def find(item):
            if parent[item] != item:
                parent[item] = find(parent[item])
            return parent[item]
        
        def union(item1,item2):
            root1 = find(item1)
            root2 = find(item2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                elif rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    rank[root1] += 1
                return True
            return False

        aristas_ordenadas = sorted(self.edges.values(), key=lambda edge: edge.peso)

        costo_total = 0
        aristas_añadidas = 0
        num_nodos = len(self.nodes)

        for edge in aristas_ordenadas:
            u_id = edge.n0.id
            v_id = edge.n1.id

            if union(u_id, v_id):
                mst_graph.add_edge(u_id, v_id, peso=edge.peso)
                costo_total += edge.peso
                aristas_añadidas += 1

                if aristas_añadidas == num_nodos - 1:
                    break

        return mst_graph, costo_total

    def KruskalI(self):
        if self.tipo != 'Undirected':
            raise ValueError("El algoritmo de Kruskal Inverso se aplica a grafos no dirigidos.")

        # 1. Clonar el grafo original por completo
        mst_graph = Graph(tipo='Undirected')
        for node_id in self.nodes:
            mst_graph.add_node(node_id)
            mst_graph.nodes[node_id].position = self.nodes[node_id].position.copy()
            
        for edge in self.edges.values():
            mst_graph.add_edge(edge.n0.id, edge.n1.id, peso=edge.peso)

        # 2. Ordenar las aristas de MAYOR a MENOR peso
        aristas_ordenadas = sorted(list(mst_graph.edges.values()), key=lambda edge: edge.peso, reverse=True)

        # 3. Evaluar el borrado de cada arista
        for edge in aristas_ordenadas:
            u_id = edge.n0.id
            v_id = edge.n1.id
            edge_id = edge.id
            
            # Guardamos la referencia del objeto original
            edge_obj = mst_graph.edges[edge_id]
            
            # Simulamos el borrado temporal
            del mst_graph.edges[edge_id]
            mst_graph.nodes[u_id].edges.remove(edge_obj)
            mst_graph.nodes[v_id].edges.remove(edge_obj)
            
            # RECORRIDO LOCAL: Ejecutamos el BFS desde uno de los extremos de la arista (u_id)
            arbol_bfs = mst_graph.BFS(u_id)
            
            # ESTRATEGIA INMUNE: Si el otro extremo (v_id) YA NO es alcanzable desde u_id,
            # significa que esta arista era el único puente que los unía. ¡No se puede borrar!
            if v_id not in arbol_bfs.nodes:
                # La reinsertamos de inmediato
                mst_graph.edges[edge_id] = edge_obj
                mst_graph.nodes[u_id].edges.append(edge_obj)
                mst_graph.nodes[v_id].edges.append(edge_obj)

        # 4. Calcular costo total
        costo_total = sum(e.peso for e in mst_graph.edges.values())
        return mst_graph, costo_total
    
    def Prim(self, nodo_inicio=None):
        if self.tipo != 'Undirected':
            raise ValueError("El algoritmo de Prim se aplica a grafos no dirigidos.")
            
        if not self.nodes:
            return Graph(tipo='Undirected'), 0

        if nodo_inicio is None:
            nodo_inicio = list(self.nodes.keys())[0]
            
        if nodo_inicio not in self.nodes:
            raise ValueError(f"El nodo inicial {nodo_inicio} no existe en el grafo.")

        # Inicializar el grafo del MST
        mst_graph = Graph(tipo='Undirected')
        mst_graph.add_node(nodo_inicio)
        
        # Estructuras de control
        visitados = set([nodo_inicio])
        costo_total = 0
        
        # La cola de prioridad (heap) guardará tuplas con el formato:
        # (peso, nodo_origen, nodo_destino, objeto_arista)
        cola_prioridad = []

        # Función auxiliar para meter al heap las aristas de un nodo recién visitado
        def registrar_aristas_de(nodo_id):
            nodo_obj = self.nodes[nodo_id]
            for edge in nodo_obj.edges: # edge es un objeto de tu clase Edge
                # Averiguar cuál extremo es el vecino
                vecino_id = edge.n1.id if edge.n0.id == nodo_id else edge.n0.id
                if vecino_id not in visitados:
                    # Empujamos al heap (Python ordena automáticamente por el primer elemento: el peso)
                    heapq.heappush(cola_prioridad, (edge.peso, nodo_id, vecino_id, edge))

        # Registrar las opciones iniciales desde nuestro punto de partida
        registrar_aristas_de(nodo_inicio)

        # Bucle principal: expandir la raíz
        while cola_prioridad and len(visitados) < len(self.nodes):
            peso, origen, destino, edge_obj = heapq.heappop(cola_prioridad)
            
            # Si el nodo destino ya fue visitado por otro camino más barato, ignoramos esta arista
            if destino in visitados:
                continue
                
            visitados.add(destino)
            mst_graph.add_node(destino)
            mst_graph.add_edge(origen, destino, peso=peso)
            costo_total += peso
            
            # Expandimos nuestras opciones agregando las aristas del nuevo nodo descubierto
            registrar_aristas_de(destino)

        return mst_graph, costo_total