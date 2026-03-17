import nodo
import arista
import grafo
import random
import export_gephi

class ModeloErdosRenyi():
    def __init__(self, nodos):
        self.nodos = nodos
    
    def elegir_vertices(self,grafo):
        v1 = random.choice(list(grafo.nodos.values()))
        v2 = random.choice(list(grafo.nodos.values()))
        
        while v1 == v2:
            v2 = random.choice(list(grafo.nodos.values()))
        
        return v1,v2

            
            
g = grafo.Grafo()
modelo = ModeloErdosRenyi(100)
modelo.generar_nodos(g)
modelo.generar_aristas(g)
export_gephi.exportar_gfd(g)

    
    
    