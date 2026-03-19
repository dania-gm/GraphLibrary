from modelo_malla import generar_malla
from export_gephi import exportar_gfd
from modelo_barabasi import grafoBarabasiAlbert
from modelo_dorogovtsev import grafoDorogovtsevMendes
from modelo_erdos_renyi import ModeloErdosRenyi
from modelo_geografico import grafoGeografico
from modelo_gilbert import grafoGilbert

def seleccionar_modelo(modelo,n,m=None):
    tipo = None
    grafo = None
    match modelo:
        case 1:
            tipo = "barabasi"
            grafo = grafoBarabasiAlbert(n,m)
        case 2:
            tipo = "dorogovtsev"
            grafo = grafoDorogovtsevMendes(n)
        case 3:
            tipo = "erdos"
            modelo_erdos = ModeloErdosRenyi(n)
            grafo = modelo_erdos.generar_grafo(n)
        case 4:
            tipo = "geografico"
            grafo = grafoGeografico(n,m)
        case 5:
            tipo = "gilbert"
            grafo = grafoGilbert(n,m)
        case 6:
            tipo = "malla"
            grafo = generar_malla(n,m)
    return tipo, grafo

def generar_grafo(modelo,n,m=None):
    tipo, grafo = seleccionar_modelo(modelo,n,m)
    nodos = len(grafo.nodos)
    exportar_gfd(grafo,tipo,nodos)
    
def menu():
    continuar = True
    print("Bienvenido al Generador de Grafos por Modelos")
    while continuar:
        print("\nSELECCIONE UN MODELO:")
        print("1.- Barabási-Albert")
        print("2.- Dorogovtsev-Mendes")
        print("3.- Erdős-Rényi ")
        print("4.- Geográfico")
        print("5.- Gilbert")
        print("6.- Malla (Grid)")
        print("0.- Salir")
        
        opcion = int(input("\nIngrese el número del modelo: "))
        match opcion:
            case 1: #Barabasi
                n = int(input("Ingrese el valor de n: "))
                d = int(input("Ingrese el valor de d: "))
                generar_grafo(opcion,n,d)
            case 2: #Dorogovtsev
                n = int(input("Ingrese el valor de n: "))
                generar_grafo(opcion,n)
            case 3: #Erdos
                n = int(input("Ingrese el valor de n: "))
                m = int(input("Ingrese el valor de m: "))
                generar_grafo(opcion,n,m)
            case 4: #Geográfico
                n = int(input("Ingrese el valor de n: "))
                r = float(input("Ingrese el valor de r (Entre 0 y 1): "))
                generar_grafo(opcion,n,r)
            case 5: #Gilbert
                n = int(input("Ingrese el valor de n: "))
                p = float(input("Ingrese el valor de p (Entre 0 y 1): "))
                generar_grafo(opcion,n,p)
            case 6: #Malla
                filas = int(input("Ingrese el valor de filas: "))
                columnas = int(input("Ingrese el valor de columnas: "))
                generar_grafo(opcion,filas,columnas)
            case 0:
                break        
        print("Grafo generado, puedes encontrar el archivo .dot en la carpeta del modelo")
        preguntar = int(input('Ingresa un 1 si quieres continuar, 0 si no'))
        if preguntar == 1:
            continuar = True
        else:
            continuar = False

menu()
