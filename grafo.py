from nodo import Nodo
from arista import Arista

class Grafo:
    def __init__(self,direccionado=False):
        self.id = 'grafo'
        self.nodos = {}
        self.aristas = {}
        self.direccionado = direccionado
        
    def get_grado(self):
        return len(self.nodos)
    
    def get_nodos(self):
        pass
    
    def __str__(self):
        dirigido = '-->'
        no_dirigido = '--'
        texto = 'Grafo\n'
        
        texto += 'Nodos:\n'
        for nodo in self.nodos.values():
            texto += f'{nodo.id}\n'
        texto += 'Aristas:\n'
        for arista in self.aristas.values():
            if arista.type == 'Directed':
                texto += f'{arista.n0} {dirigido} {arista.n1}\n'
            if arista.type == 'Undirected':
                texto += f'{arista.n0} {no_dirigido} {arista.n1}\n'
        return texto
    
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
            if v1.id != v2.id and not grafo.existe_arista(v1, v2):
                grafo.add_arista(v1, v2)
                aristas += 1
    
    def generar_nodos(self,grafo):
        for i in range(self.nodos):
            n = nodo.Nodo(i)
            grafo.add_nodo(n)
    
    
        
        

