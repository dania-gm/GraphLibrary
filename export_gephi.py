import datetime as dt

fecha_actual = dt.datetime.now().strftime('%Y-%m-%d_%H-%M')

def exportar_gfd(grafo, modelo):
    archivo=f'grafo_{modelo}_{fecha_actual}.dot'
    tipo_grafo = 'digraph' if grafo.direccionado else 'graph'
    conector = '->' if grafo.direccionado else '--'
    with open(archivo,'w') as f:
        f.write(f'{tipo_grafo} G {{\n')
        for nodo in grafo.nodos.values():
            f.write(f'    {nodo.id};\n')
        for arista in grafo.aristas.values():
            f.write(f'{arista.n0} {conector} {arista.n1};\n')
        f.write('}\n')