class Edge:
    def __init__(self,edge_id,n0,n1,tipo):
        self.id = edge_id
        self.n0 = n0
        self.n1 = n1
        self.tipo = tipo
    
    def get_edge(self):
        return f'Arista(id={self.id}, type={self.tipo})'
    
    def get_nodes(self):
        return self.n0, self.n1
    