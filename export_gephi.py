import datetime as dt
import grafo
fecha_actual = dt.date.today()
def exportar_gfd(grafo, archivo=f'grafo_{fecha_actual}.dot'):
    tipo_grafo = 'digraph' if grafo.direccionado else 'graph'
    conector = '->' if grafo.direccionado else '--'
    with open(archivo,'w') as f:
        f.write(f'{tipo_grafo} G {{\n')
        for arista in grafo.aristas.values():
            f.write(f'{arista.n0} {conector} {arista.n1};\n')
        f.write('}\n')

g = grafo.Grafo(direccionado=True)
n1 = grafo.Nodo('1')
n2 = grafo.Nodo('2')
n3 = grafo.Nodo('3')
g.add_nodo(n1)
g.add_nodo(n2)
g.add_nodo(n3)
g.add_arista(n1,n2)
g.add_arista(n2,n3)
exportar_gfd(g)