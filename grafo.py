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
    
    def add_nodo(self,nodo):
        existe_nodo = self.nodos.get(nodo.id)
        if existe_nodo is None:
            self.nodos[nodo.id] = nodo
            
    def add_arista(self, n0, n1, type='Directed'):
        v0 = n0.id
        v1 = n1.id
        if self.existe_arista(v0,v1,type):
             pass
        else:
            arista = Arista(v0, v1, type)
            self.aristas[arista.id] = arista
    
    def existe_arista(self, n0, n1,type):
        existe = None
        
        if type == 'Directed':
            par_busqueda = (n0, n1)
            existe = False
            
            for a in self.aristas.values():
                if (a.n0, a.n1) == par_busqueda:
                    existe = True
                    break 
    
        else:
            id_min = min(n0, n1)
            id_max = max(n0, n1)
            par_busqueda = (id_min, id_max)
            existe = False
            
            for a in self.aristas.values():
                if (min(a.n0,a.n1),max(a.n0,a.n1)) == par_busqueda:    
                    existe = True
                    break

        return existe
    
        
        

