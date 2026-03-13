import nodo
import arista
import grafo
import random
import export_gephi

class ModeloErdosRenyi():
    def __init__(self, nodos):
        self.nodos = nodos
        
    def calcular_cantidad_aristas(self):
        nodos = self.nodos
        #aristas_totales = (nodos ** 2)/2
        aristas_totales = nodos*(nodos-1)/2
        cantidad_aristas = aristas_totales * .1
        return int(cantidad_aristas)
    
    def elegir_vertices(self,grafo):
        v1 = random.choice(list(grafo.nodos.values()))
        v2 = random.choice(list(grafo.nodos.values()))
        
        while v1 == v2:
            v2 = random.choice(list(grafo.nodos.values()))
        
        return v1,v2
    
    def generar_aristas(self,grafo):
        n_aristas = self.calcular_cantidad_aristas()
        aristas = 0 
        while aristas < n_aristas:
            v1,v2 = self.elegir_vertices(grafo)
            grafo.add_arista(v1,v2)
            aristas +=1
    
    def generar_nodos(self,grafo):
        for i in range(self.nodos):
            n = nodo.Nodo(i)
            grafo.add_nodo(n)
            
            
g = grafo.Grafo()
modelo = ModeloErdosRenyi(500)
modelo.generar_nodos(g)
modelo.generar_aristas(g)
export_gephi.exportar_gfd(g)

    
    
    