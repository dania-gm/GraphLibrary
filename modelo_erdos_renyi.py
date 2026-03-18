import nodo
import arista
from grafo import Grafo
import random
import export_gephi

class ModeloErdosRenyi():
    def __init__(self, nodos, type="Directed"):
        self.nodos = nodos
        self.type = type
    
    def elegir_vertices(self,grafo):
        v1 = random.choice(list(grafo.nodos.values()))
        v2 = random.choice(list(grafo.nodos.values()))
        
        while v1 == v2:
            v2 = random.choice(list(grafo.nodos.values()))
        
        return v1,v2

    def calcular_cantidad_aristas(self):
        nodos = self.nodos
        #aristas_totales = (nodos ** 2)/2
        aristas_totales = nodos*(nodos-1)/2
        cantidad_aristas = aristas_totales * .1
        return int(cantidad_aristas)
    
    def generar_aristas(self,grafo):
        n_aristas = self.calcular_cantidad_aristas()
        aristas = 0 
        while aristas < n_aristas:
            v1,v2 = self.elegir_vertices(grafo)
            if v1.id != v2.id and not grafo.existe_arista(v1, v2, self.type):
                grafo.add_arista(v1, v2)
                aristas += 1
    
    def generar_nodos(self,grafo):
        for i in range(self.nodos):
            n = nodo.Nodo(i)
            grafo.add_nodo(n)
    
    def generar_grafo(self,n):
        grafo = Grafo(n)
        self.generar_nodos(grafo)
        self.generar_aristas(grafo)
        return grafo
    

    
    
    