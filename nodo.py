class Nodo:
    def __init__(self,id):
        self.id = id
        self.atr = {
            'aristas': [],
            'nodos_vecinos': []
        }
    
    def get_nodo(self):
        print(self.id)
    
    
    