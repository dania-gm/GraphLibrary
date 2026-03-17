class Arista:
    def __init__(self,n0,n1,type):
        self.id = f'{n0}--{n1}'
        self.n0 = n0
        self.n1 = n1
        self.type = type
    
    def add_arista(self,n0,n1,type='Directed'):
        par = (n0.id, n1.id)
        if par in [(a.n0, a.n1) if a.n0 < a.n1 else (a.n1, a.n0) for a in self.aristas.values()]:
            return  # ya existe, no agregar duplicado

        arista = Arista(n0.id, n1.id, type)
        self.aristas[arista.id] = arista
    
    def existe_arista(self, n0, n1):
        par = (n0.id, n1.id) if n0.id < n1.id else (n1.id, n0.id)

        return par in [
            #tipo graph
            (a.n0, a.n1) if a.n0 < a.n1 else (a.n1, a.n0)
            for a in self.aristas.values()
        ]
    