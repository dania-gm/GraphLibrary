import random
from nodo import Nodo
from grafo import Grafo

def grafoBarabasiAlbert(n, d):
    if d >= n:
        raise ValueError("d debe ser menor que n")
    

    g = Grafo()
    
    nodos_lista = []
    for i in range(d):
        nodo_id = f'nodo_{i}'
        nod = Nodo(nodo_id)
        g.add_nodo(nod)
        nodos_lista.append(nod)
    
    for i in range(d):
        for j in range(i + 1, d):
            g.add_arista(nodos_lista[i], nodos_lista[j], 'Undirected')
    
    # 3. Agregar los nodos restantes (desde d hasta n-1)
    for i in range(d, n):
        # Crear nuevo nodo
        nodo_id = f'nodo_{i}'
        nuevo_nodo = Nodo(nodo_id)
        g.add_nodo(nuevo_nodo)
        nodos_lista.append(nuevo_nodo)
        
        # 4. Calcular grados de todos los nodos existentes
        grados = []
        for nodo_existente in nodos_lista[:-1]:  # Todos excepto el nuevo
            grado = 0
            # Contar aristas incidentes
            for arista in g.aristas.values():
                if arista.n0 == nodo_existente.id or arista.n1 == nodo_existente.id:
                    grado += 1
            grados.append(grado)
        
        # 5. Selección preferencial: elegir d nodos basados en su grado
        # Usar weighted random selection
        nodos_seleccionados = set()
        intentos = 0
        max_intentos = 1000  # Evitar bucle infinito
        
        while len(nodos_seleccionados) < d and intentos < max_intentos:
            # Seleccionar un nodo con probabilidad proporcional a su grado
            nodo_seleccionado = random.choices(
                population=nodos_lista[:-1],  # Todos los nodos existentes excepto el nuevo
                weights=grados,
                k=1
            )[0]
            
            if nodo_seleccionado.id not in nodos_seleccionados:
                nodos_seleccionados.add(nodo_seleccionado.id)
            
            intentos += 1
        
        # 6. Conectar el nuevo nodo a los d nodos seleccionados
        for nodo_id_seleccionado in nodos_seleccionados:
            nodo_destino = g.nodos[nodo_id_seleccionado]
            g.add_arista(nuevo_nodo, nodo_destino, 'Undirected')
    
    return g