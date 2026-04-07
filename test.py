from algoritmos_generacion import *
import os

# n = 500
# p = 0.1
# g = generar_gilbert(n,p,'Undirected')
# nombre_archivo = 'Gilbert500.dot'
# ruta = os.path.join('/Users/daniagarcia/Documents/biblioteca_grafos/modelo_gilbert/files', nombre_archivo)
# conector = '->' if g.tipo == 'Directed' else '--'
# tipo = 'digraph' if g.tipo == 'Directed' else 'graph'
# lineas = [f'{tipo} G {{']
# for nodo in g.nodes.values():
#     lineas.append(f'    {nodo.id};')
    
# for arista in g.edges.values():
#     lineas.append(f'    {arista.n0.id} {conector} {arista.n1.id};')

# lineas.append('}')
# with open(ruta, 'w', encoding='utf-8') as f:
#     f.write('\n'.join(lineas) + '\n')

# n = 500
# m = 1000
# g = generar_erdos_renyi(n,m,'Undirected')
# nombre_archivo = 'ErdosRenyi500.dot'
# ruta = os.path.join('/Users/daniagarcia/Documents/biblioteca_grafos/modelo_erdos_renyi/files', nombre_archivo)
# conector = '->' if g.tipo == 'Directed' else '--'
# tipo = 'digraph' if g.tipo == 'Directed' else 'graph'
# lineas = [f'{tipo} G {{']
# for nodo in g.nodes.values():
#     lineas.append(f'    {nodo.id};')
    
# for arista in g.edges.values():
#      lineas.append(f'    {arista.n0.id} {conector} {arista.n1.id};')

# lineas.append('}')
# with open(ruta, 'w', encoding='utf-8') as f:
#     f.write('\n'.join(lineas) + '\n')
    
# import xml.etree.ElementTree as ET
# import os

# n = 500
# r = 0.1
# g = generar_geografico_simple(n,r,'Undirected')
# nombre_archivo = 'GeograficoSimple500.gexf'
# ruta = os.path.join('/Users/daniagarcia/Documents/biblioteca_grafos/modelo_geografico/files', nombre_archivo)
# # 🔹 Namespaces oficiales de GEXF 1.2
# NS  = "{http://www.gexf.net/1.2draft}"
# VIZ = "{http://www.gexf.net/1.2draft/viz}"

# # Raíz del documento
# gexf = ET.Element(f"{NS}gexf", version="1.2")
# gexf.set("xmlns:viz", "http://www.gexf.net/1.2draft/viz")

# # Elemento <graph>
# edge_type = "directed" if g.tipo == "Directed" else "undirected"
# graph = ET.SubElement(gexf, f"{NS}graph", defaultedgetype=edge_type)

# # 🔹 Nodos con posición X/Y
# nodes_el = ET.SubElement(graph, f"{NS}nodes")
# for nodo in g.nodes.values():
#     node = ET.SubElement(nodes_el, f"{NS}node", id=str(nodo.id), label=str(nodo.id))
#     if hasattr(nodo, "position"):
#         # Escalamos a [0, 1000] para que Gephi los renderice correctamente
#         x = nodo.position.get("x", 0.5) * 1000
#         y = nodo.position.get("y", 0.5) * 1000
#         ET.SubElement(node, f"{VIZ}position", x=f"{x:.2f}", y=f"{y:.2f}", z="0.0")

# # 🔹 Aristas
# edges_el = ET.SubElement(graph, f"{NS}edges")
# for i, arista in enumerate(g.edges.values()):
#     ET.SubElement(edges_el, f"{NS}edge", 
#                   id=str(i), 
#                   source=str(arista.n0.id), 
#                   target=str(arista.n1.id))

# # Guardar archivo con indentación legible
# tree = ET.ElementTree(gexf)
# ET.indent(tree, space="  ")  # Python 3.9+
# tree.write(ruta, encoding="utf-8", xml_declaration=True)

# import xml.etree.ElementTree as ET
# import os

# n = 50
# m = 10
# g = generar_malla(n,m,'Undirected')
# nombre_archivo = 'Malla500.gexf'
# ruta = os.path.join('/Users/daniagarcia/Documents/biblioteca_grafos/modelo_malla/files', nombre_archivo)
# # 🔹 Namespaces oficiales de GEXF 1.2
# NS  = "{http://www.gexf.net/1.2draft}"
# VIZ = "{http://www.gexf.net/1.2draft/viz}"

# # Raíz del documento
# gexf = ET.Element(f"{NS}gexf", version="1.2")
# gexf.set("xmlns:viz", "http://www.gexf.net/1.2draft/viz")

# # Elemento <graph>
# edge_type = "directed" if g.tipo == "Directed" else "undirected"
# graph = ET.SubElement(gexf, f"{NS}graph", defaultedgetype=edge_type)

# # 🔹 Nodos con posición X/Y
# nodes_el = ET.SubElement(graph, f"{NS}nodes")
# for nodo in g.nodes.values():
#     node = ET.SubElement(nodes_el, f"{NS}node", id=str(nodo.id), label=str(nodo.id))
#     if hasattr(nodo, "position"):
#         # Escalamos a [0, 1000] para que Gephi los renderice correctamente
#         x = nodo.position.get("x", 0.5) * 1000
#         y = nodo.position.get("y", 0.5) * 1000
#         ET.SubElement(node, f"{VIZ}position", x=f"{x:.2f}", y=f"{y:.2f}", z="0.0")

# # 🔹 Aristas
# edges_el = ET.SubElement(graph, f"{NS}edges")
# for i, arista in enumerate(g.edges.values()):
#     ET.SubElement(edges_el, f"{NS}edge", 
#                   id=str(i), 
#                   source=str(arista.n0.id), 
#                   target=str(arista.n1.id))

# # Guardar archivo con indentación legible
# tree = ET.ElementTree(gexf)
# ET.indent(tree, space="  ")  # Python 3.9+
# tree.write(ruta, encoding="utf-8", xml_declaration=True)

n=500
d=3
g= generar_barabasi(n,d,'Undirected')
nombre_archivo = 'Barabasi500.dot'
ruta = os.path.join('/Users/daniagarcia/Documents/biblioteca_grafos/modelo_barabasi/files', nombre_archivo)
conector = '->' if g.tipo == 'Directed' else '--'
tipo = 'digraph' if g.tipo == 'Directed' else 'graph'
lineas = [f'{tipo} G {{']
for nodo in g.nodes.values():
    lineas.append(f'    {nodo.id};')
    
for arista in g.edges.values():
     lineas.append(f'    {arista.n0.id} {conector} {arista.n1.id};')

lineas.append('}')
with open(ruta, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lineas) + '\n')