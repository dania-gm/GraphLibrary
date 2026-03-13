from nodo import Nodo
from arista import Arista

class Grafo:
    def __init__(self,direccionado=False):
        self.id = 'grafo'
        self.nodos = {}
        self.aristas = {}
        self.direccionado = direccionado
        
    def add_nodo(self,nodo):
        existe_nodo = self.nodos.get(nodo.id)
        if existe_nodo is None:
            self.nodos[nodo.id] = nodo
    
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
    
    def add_arista(self,n0,n1,type='Directed'):
        par = (n0.id, n1.id)
        if par in [(a.n0, a.n1) if a.n0 < a.n1 else (a.n1, a.n0) for a in self.aristas.values()]:
            return  # ya existe, no agregar duplicado

        arista = Arista(n0.id, n1.id, type)
        self.aristas[arista.id] = arista
        
        

