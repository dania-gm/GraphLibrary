import datetime as dt
import os

fecha_actual = dt.datetime.now().strftime('%Y-%m-%d_%H:%M')
carpeta = ""
nombre_base = ""

def exportar_gfd(grafo,modelo,nodos):
    match modelo:
        case "barabasi":
            carpeta_rel = "modelo_barabasi/files"
            nombre_base = "modelo_barabasi"
        case "dorogovtsev":
            carpeta_rel = "modelo_dorogovtsev/files"
            nombre_base = "modelo_dorogovtsev"
        case "erdos":
            carpeta_rel = "modelo_erdos_renyi/files"
            nombre_base = "modelo_erdos"
        case "geografico":
            carpeta_rel = "modelo_geografico/files"
            nombre_base = "modelo_geografico"
        case "gilbert":
            carpeta_rel = "modelo_gilbert/files"
            nombre_base = "modelo_gilbert"
        case "malla":
            carpeta_rel = "modelo_malla/files"
            nombre_base = "modelo_malla"
        case _:
            carpeta_rel = "files"
            nombre_base = "grafo_desconocido"
        
    os.makedirs(carpeta_rel, exist_ok=True)
    nombre_archivo = f"{nombre_base}_{nodos}_{fecha_actual}.dot"
    archivo = os.path.join(carpeta_rel, nombre_archivo)
    
    tipo_grafo = 'digraph' if grafo.direccionado else 'graph'
    conector = '->' if grafo.direccionado else '--'
    with open(archivo,'w') as f:
        f.write(f'{tipo_grafo} G {{\n')
        for nodo in grafo.nodos.values():
            f.write(f'    {nodo.id};\n')
        for arista in grafo.aristas.values():
            f.write(f'{arista.n0} {conector} {arista.n1};\n')
        f.write('}\n')