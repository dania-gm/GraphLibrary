class Nodo:
    def __init__(self,id):
        self.id = id
        self.atr = {
            'aristas': [],
            'nodos_vecinos': []
        }
    
    def get_nodo(self):
        print(self.id)
    
    def add_nodo(self,nodo):
        existe_nodo = self.nodos.get(nodo.id)
        if existe_nodo is None:
            self.nodos[nodo.id] = nodo
    
    
    