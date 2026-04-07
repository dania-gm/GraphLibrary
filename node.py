class Node:
    def __init__(self,id,x=0,y=0):
        self.id = id
        self.edges = []
        self.position = {
            'x':x,
            'y':y
        }
        self.nivel = 0
 
    def get_node(self):
        print(self.id)
        return f'Nodo(id={self.id}, grado={self.deg()})'
    
    def deg(self):
        return len(self.edges)
    
    def add_edge_ref(self,neighbor_id):
        if neighbor_id not in self.edges:
            self.edges.append(neighbor_id)
    
    
    
    
    