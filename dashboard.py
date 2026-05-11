import streamlit as st
import sys
import os
import io
import math
import re

PROJECT_DIR = os.path.join(os.path.dirname(__file__), "graph_lib")
sys.path.insert(0, PROJECT_DIR)

from graph import Graph
from algoritmos_generacion import (
    generar_erdos_renyi,
    generar_gilbert,
    generar_geografico_simple,
    generar_malla,
    generar_barabasi,
    generar_dorogovtsev,
)

def grafo_a_dot(g: Graph) -> str:
    """Convierte un objeto Graph a formato DOT (Graphviz), optimizado para Gephi."""
    es_dirigido = g.tipo == "Directed"
    tipo_str   = "digraph" if es_dirigido else "graph"
    conector   = "->"      if es_dirigido else "--"

    lineas = [f"{tipo_str} G {{"]
    
    # 1. Definir los nodos y sus atributos
    for nodo in g.nodes.values():
        # Extraer posiciones como lo hacías en test.py
        x_val = nodo.position.get("x", 0.5)
        y_val = nodo.position.get("y", 0.5)

        x_scaled = x_val * 1000
        y_scaled = y_val * 1000

        nivel = getattr(nodo, "nivel", -1)
        
        atributos_nodo = (
            f'label="{nodo.id}", '
            f'pos="{x_scaled:.2f},{y_scaled:.2f}", '
            f'nivel="{nivel}", '
            f'style="filled", fillcolor="#A0CBE2"'
        )
        lineas.append(f'    "{nodo.id}" [{atributos_nodo}];')


    for arista in g.edges.values():

        u = arista.n0.id if hasattr(arista.n0, 'id') else arista.n0
        v = arista.n1.id if hasattr(arista.n1, 'id') else arista.n1
        
        peso = getattr(arista,"peso",1)
        
        lineas.append(f'    "{u}" {conector} "{v}" [weight="{peso}", label="{peso}"];')
        
    lineas.append("}")
    return "\n".join(lineas)


def stats_grafo(g: Graph) -> dict:
    """Devuelve estadísticas básicas del grafo."""
    grados = [n.deg() for n in g.nodes.values()]
    return {
        "Nodos": len(g.nodes),
        "Aristas": len(g.edges),
        "Grado mínimo": min(grados) if grados else 0,
        "Grado máximo": max(grados) if grados else 0,
        "Grado promedio": round(sum(grados) / len(grados), 2) if grados else 0,
    }

def mostrar_seccion_dfs_r():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🌳 Generar Árbol DFS Recursivo")
    st.write("Aplica el algoritmo de Búsqueda en Profundidad Recursivo (DFS) para obtener un árbol a partir del grafo actual.")

    # Validar que exista un grafo y tenga nodos
    if "grafo" not in st.session_state or not st.session_state.grafo or not st.session_state.grafo.nodes:
        st.info("Genera primero un grafo en la sección superior para poder aplicar DFS.")
        return

    # Obtener los IDs de los nodos para el selector
    lista_nodos = list(st.session_state.grafo.nodes.keys())
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        nodo_inicio = st.selectbox(
            "Selecciona el nodo inicial (raíz):", 
            options=lista_nodos,
            key="select_dfs_r" # Agregamos una key única para que no choque con el select del BFS
        )
        
    with col2:
        st.write("") 
        st.write("")
        btn_dfs_r = st.button("🚀 Generar Árbol DFS Recursivo", use_container_width=True)

    if btn_dfs_r:
        with st.spinner('Ejecutando algoritmo DFS Recursivo...'):
            st.session_state.grafo_dfs_r = st.session_state.grafo.DFS_R(nodo_inicio)
            st.session_state.dot_dfs_r = grafo_a_dot(st.session_state.grafo_dfs_r)
            st.session_state.dfs_r_root = nodo_inicio

    # Mostrar resultados validando de forma segura
    if "grafo_dfs_r" in st.session_state and st.session_state.grafo_dfs_r is not None:
        g_dfs_r = st.session_state.grafo_dfs_r
        root_dfs = st.session_state.dfs_r_root
        
        st.success(f"¡Árbol DFS Recursivo generado exitosamente desde el nodo {root_dfs}!")
        st.write(f"**Nodos alcanzados:** {len(g_dfs_r.nodes)} | **Aristas del árbol:** {len(g_dfs_r.edges)}")

        with st.expander("📄 Ver vista previa del archivo .dot (DFS Recursivo)"):
            st.code(st.session_state.dot_dfs_r, language="dot")
        
        # Corregido: Usamos root_dfs en lugar de bfs_root
        nombre_archivo_dfs_r = f"DFS_Recursivo_desde_nodo_{root_dfs}.dot"
        st.download_button(
            label=f"⬇️ Descargar {nombre_archivo_dfs_r}",
            data=st.session_state.dot_dfs_r.encode("utf-8"),
            file_name=nombre_archivo_dfs_r,
            mime="text/plain",
            use_container_width=True,
            key="btn_descarga_dfs_r"
        )

def mostrar_seccion_dfs_i():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🌳 Generar Árbol DFS Iterativo")
    st.write("Aplica el algoritmo de Búsqueda en Profundidad Iterativo (DFS) para obtener un árbol a partir del grafo actual.")

    # Validar que exista un grafo y tenga nodos
    if "grafo" not in st.session_state or not st.session_state.grafo or not st.session_state.grafo.nodes:
        st.info("Genera primero un grafo en la sección superior para poder aplicar DFS.")
        return

    # Obtener los IDs de los nodos para el selector
    lista_nodos = list(st.session_state.grafo.nodes.keys())
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        nodo_inicio = st.selectbox(
            "Selecciona el nodo inicial (raíz):", 
            options=lista_nodos,
            key="select_dfs_i" # Agregamos una key única para que no choque con el select del BFS
        )
        
    with col2:
        st.write("") 
        st.write("")
        btn_dfs_i = st.button("🚀 Generar Árbol DFS Iterativo", use_container_width=True)

    if btn_dfs_i:
        with st.spinner('Ejecutando algoritmo DFS Iterativo...'):
            st.session_state.grafo_dfs_i = st.session_state.grafo.DFS_I(nodo_inicio)
            st.session_state.dot_dfs_i = grafo_a_dot(st.session_state.grafo_dfs_i)
            st.session_state.dfs_i_root = nodo_inicio

    # Mostrar resultados validando de forma segura
    if "grafo_dfs_i" in st.session_state and st.session_state.grafo_dfs_i is not None:
        g_dfs_i = st.session_state.grafo_dfs_i
        root_dfs_i = st.session_state.dfs_i_root
        
        st.success(f"¡Árbol DFS Iterativo generado exitosamente desde el nodo {root_dfs_i}!")
        st.write(f"**Nodos alcanzados:** {len(g_dfs_i.nodes)} | **Aristas del árbol:** {len(g_dfs_i.edges)}")

        with st.expander("📄 Ver vista previa del archivo .dot (DFS Iterativo)"):
            st.code(st.session_state.dot_dfs_i, language="dot")
        
        # Corregido: Usamos root_dfs en lugar de bfs_root
        nombre_archivo_dfs_i = f"DFS_Iterativo_desde_nodo_{root_dfs_i}.dot"
        st.download_button(
            label=f"Descargar {nombre_archivo_dfs_i}",
            data=st.session_state.dot_dfs_i.encode("utf-8"),
            file_name=nombre_archivo_dfs_i,
            mime="text/plain",
            use_container_width=True,
            key="btn_descarga_dfs_i"
        )


def mostrar_seccion_bfs():
    """Muestra la sección para generar y exportar el árbol BFS."""
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🌳 Generar Árbol BFS")
    st.write("Aplica el algoritmo de Búsqueda en Anchura (BFS) para obtener un árbol a partir del grafo actual.")

    # Validar que exista un grafo y tenga nodos
    if not st.session_state.grafo or not st.session_state.grafo.nodes:
        st.info("Genera primero un grafo en la sección superior para poder aplicar BFS.")
        return

    # Obtener los IDs de los nodos para el selector
    lista_nodos = list(st.session_state.grafo.nodes.keys())
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        nodo_inicio = st.selectbox(
            "Selecciona el nodo inicial (raíz):", 
            options=lista_nodos,
            key="select_bfs"
        )
        
    with col2:
        st.write("") 
        st.write("")
        btn_bfs = st.button("🚀 Generar Árbol BFS", use_container_width=True)

    # Si se presiona el botón, calculamos el BFS y lo guardamos en session_state
    if btn_bfs:
        with st.spinner('Ejecutando algoritmo BFS...'):
            st.session_state.grafo_bfs = st.session_state.grafo.BFS(nodo_inicio)
            st.session_state.dot_bfs = grafo_a_dot(st.session_state.grafo_bfs)
            st.session_state.bfs_root = nodo_inicio

    # Mostrar resultados guardados en session_state (evita que desaparezcan al dar clic en descargar)
    if st.session_state.grafo_bfs is not None:
        g_bfs = st.session_state.grafo_bfs
        
        st.success(f"¡Árbol BFS generado exitosamente desde el nodo {st.session_state.bfs_root}!")
        st.write(f"**Nodos alcanzados:** {len(g_bfs.nodes)} | **Aristas del árbol:** {len(g_bfs.edges)}")

        with st.expander("📄 Ver vista previa del archivo .dot (BFS)"):
            st.code(st.session_state.dot_bfs, language="dot")
        
        nombre_archivo_bfs = f"BFS_desde_nodo_{st.session_state.bfs_root}.dot"
        st.download_button(
            label=f"⬇️ Descargar {nombre_archivo_bfs}",
            data=st.session_state.dot_bfs.encode("utf-8"),
            file_name=nombre_archivo_bfs,
            mime="text/plain",
            use_container_width=True,
            key="btn_descarga_bfs"
        ) 
        
def mostrar_seccion_dfs_r():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🌳 Generar Árbol DFS Recursivo")
    st.write("Aplica el algoritmo de Búsqueda en Profundidad Recursivo (DFS) para obtener un árbol a partir del grafo actual.")

    # Validar que exista un grafo y tenga nodos
    if "grafo" not in st.session_state or not st.session_state.grafo or not st.session_state.grafo.nodes:
        st.info("Genera primero un grafo en la sección superior para poder aplicar DFS.")
        return

    # Obtener los IDs de los nodos para el selector
    lista_nodos = list(st.session_state.grafo.nodes.keys())
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        nodo_inicio = st.selectbox(
            "Selecciona el nodo inicial (raíz):", 
            options=lista_nodos,
            key="select_dfs_r" # Agregamos una key única para que no choque con el select del BFS
        )
        
    with col2:
        st.write("") 
        st.write("")
        btn_dfs_r = st.button("🚀 Generar Árbol DFS Recursivo", use_container_width=True)

    if btn_dfs_r:
        with st.spinner('Ejecutando algoritmo DFS Recursivo...'):
            st.session_state.grafo_dfs_r = st.session_state.grafo.DFS_R(nodo_inicio)
            st.session_state.dot_dfs_r = grafo_a_dot(st.session_state.grafo_dfs_r)
            st.session_state.dfs_r_root = nodo_inicio

    # Mostrar resultados validando de forma segura
    if "grafo_dfs_r" in st.session_state and st.session_state.grafo_dfs_r is not None:
        g_dfs_r = st.session_state.grafo_dfs_r
        root_dfs = st.session_state.dfs_r_root
        
        st.success(f"¡Árbol DFS Recursivo generado exitosamente desde el nodo {root_dfs}!")
        st.write(f"**Nodos alcanzados:** {len(g_dfs_r.nodes)} | **Aristas del árbol:** {len(g_dfs_r.edges)}")

        with st.expander("📄 Ver vista previa del archivo .dot (DFS Recursivo)"):
            st.code(st.session_state.dot_dfs_r, language="dot")
        
        # Corregido: Usamos root_dfs en lugar de bfs_root
        nombre_archivo_dfs_r = f"DFS_Recursivo_desde_nodo_{root_dfs}.dot"
        st.download_button(
            label=f"⬇️ Descargar {nombre_archivo_dfs_r}",
            data=st.session_state.dot_dfs_r.encode("utf-8"),
            file_name=nombre_archivo_dfs_r,
            mime="text/plain",
            use_container_width=True,
            key="btn_descarga_dfs_r"
        )

def mostrar_seccion_dijkstra():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🗺️ Calcular Caminos Más Cortos (Dijkstra)")
    st.write("Aplica el algoritmo de Dijkstra para encontrar los caminos más cortos y visualizar las distancias acumuladas desde un nodo de origen.")

    # Validar que exista un grafo y tenga nodos
    if "grafo" not in st.session_state or not st.session_state.grafo or not st.session_state.grafo.nodes:
        st.info("Genera o importa primero un grafo en la sección superior para poder aplicar Dijkstra.")
        return

    # Obtener los IDs de los nodos originales para el selector
    lista_nodos = list(st.session_state.grafo.nodes.keys())
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        nodo_inicio = st.selectbox(
            "Selecciona el nodo origen:", 
            options=lista_nodos,
            key="select_dijkstra" # Key única para no chocar con BFS o DFS
        )
        
    with col2:
        st.write("") 
        st.write("")
        btn_dijkstra = st.button("🚀 Ejecutar Dijkstra", use_container_width=True)

    # Lógica de ejecución
    if btn_dijkstra:
        with st.spinner('Calculando distancias óptimas...'):
            # Ejecutamos el algoritmo llamando al método que creamos
            st.session_state.grafo_dijkstra = st.session_state.grafo.Dijkstra(nodo_inicio)
            
            # Convertimos el grafo resultante a formato DOT
            st.session_state.dot_dijkstra = grafo_a_dot(st.session_state.grafo_dijkstra)
            
            # Guardamos el nodo raíz para los mensajes
            st.session_state.dijkstra_root = nodo_inicio

    # Mostrar resultados validando de forma segura
    if "grafo_dijkstra" in st.session_state and st.session_state.grafo_dijkstra is not None:
        g_dijkstra = st.session_state.grafo_dijkstra
        root_dijkstra = st.session_state.dijkstra_root
        
        st.success(f"¡Árbol de caminos más cortos generado exitosamente desde el nodo origen: {root_dijkstra}!")
        st.write(f"**Nodos alcanzados:** {len(g_dijkstra.nodes)} | **Rutas calculadas (Aristas):** {len(g_dijkstra.edges)}")

        # Expander para ver el código
        with st.expander("📄 Ver vista previa del archivo .dot (Dijkstra)"):
            st.code(st.session_state.dot_dijkstra, language="dot")
        
        # Botón de descarga
        nombre_archivo_dijkstra = f"Dijkstra_desde_{root_dijkstra}.dot"
        st.download_button(
            label=f"⬇️ Descargar {nombre_archivo_dijkstra}",
            data=st.session_state.dot_dijkstra.encode("utf-8"),
            file_name=nombre_archivo_dijkstra,
            mime="text/plain",
            use_container_width=True,
            key="btn_descarga_dijkstra"
        )

def cargar_grafo_desde_dot_texto(contenido: str) -> Graph:
    """
    Lee el contenido de un archivo .dot en formato texto y reconstruye el objeto Graph.
    """
    # 1. Determinar el tipo de grafo leyendo la primera línea
    primera_linea = contenido.split('\n')[0].strip().lower()
    es_dirigido = "digraph" in primera_linea
    tipo = 'Directed' if es_dirigido else 'Undirected'
    
    g = Graph(tipo)

    # 2. Definir los patrones de búsqueda (Regex)
    patron_nodo = re.compile(r'^\s*"([^"]+)"\s+\[(.*?)\];', re.MULTILINE)
    patron_arista = re.compile(r'^\s*"([^"]+)"\s+(?:--|->)\s+"([^"]+)"(?:.*?\[(.*?)\])?\s*;', re.MULTILINE)

    # 3. Extraer Nodos
    for match in patron_nodo.finditer(contenido):
        nodo_id = match.group(1)
        atributos_str = match.group(2)
        
        g.add_node(nodo_id)
        nodo_obj = g.nodes[nodo_id]

        # Extraer posición (pos="x,y")
        match_pos = re.search(r'pos="([\d\.-]+),([\d\.-]+)"', atributos_str)
        if match_pos:
            # Dividimos entre 1000 para regresar a la escala original [0, 1] que usa tu test.py
            nodo_obj.position['x'] = float(match_pos.group(1)) / 1000.0
            nodo_obj.position['y'] = float(match_pos.group(2)) / 1000.0

        # Extraer el nivel (nivel="X")
        match_nivel = re.search(r'nivel="([\d\.-]+)"', atributos_str)
        if match_nivel:
            nodo_obj.nivel = int(match_nivel.group(1))

    # 4. Extraer Aristas
    for match in patron_arista.finditer(contenido):
        u = match.group(1)
        v = match.group(2)
        atributos_str = match.group(3)
        peso = 1
        if atributos_str:
            match_peso = re.search(r'weight="([\d\.-]+)"', atributos_str)
            if match_peso:
                peso_val = float(match_peso.group(1))
                peso = int(peso_val) if peso_val.is_integer() else peso_val
        g.add_edge(u, v)

    return g

st.set_page_config(
    page_title="Generador de Grafos",
    page_icon="🕸️",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
 
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
        background-color: #f4f3fb !important;
        color: #2d2b4e;
    }
    .stApp { background-color: #f4f3fb !important; }
 
    /* Cabecera hero */
    .hero {
        background: #ffffff;
        border-radius: 24px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 4px 24px rgba(236,72,153,0.08);
        display: flex;
        align-items: center;
        gap: 1.2rem;
    }
    .hero-icon {
        background: linear-gradient(135deg, #f9a8d4, #ec4899);
        border-radius: 18px;
        width: 54px; height: 54px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.7rem; flex-shrink: 0;
    }
    .hero h1 {
        font-size: 1.75rem; font-weight: 900;
        color: #0B1957; margin: 0 0 .1rem; letter-spacing: -.5px;
    }
    .hero p { color: #9896b8; font-size: 0.98rem; margin: 0; font-weight: 600; }
 
    /* Tarjetas de estadísticas */
    .stat-card {
        background: #ffffff; border-radius: 20px;
        padding: 1.2rem 1rem; text-align: center;
        box-shadow: 0 2px 16px rgba(100,80,180,0.07);
    }
    .stat-value { font-size: 2rem; font-weight: 900; color: #1e1b40; line-height: 1; }
    .stat-value span { color: #ec4899; }
    .stat-label {
        font-size: 0.72rem; font-weight: 700; color: #b0aecf;
        text-transform: uppercase; letter-spacing: 1.2px; margin-top: .4rem;
    }
 
    /* Panel DOT */
    .dot-box {
        background: #fdf5fa; border: 1.5px solid #fce7f3; border-radius: 16px;
        padding: 1.1rem 1.3rem; font-family: 'Courier New', monospace;
        font-size: 0.78rem; color: #6b5b8e; max-height: 300px;
        overflow-y: auto; white-space: pre; line-height: 1.6;
    }
 
    /* Botón generar */
    div.stButton > button {
        background: linear-gradient(135deg, #f472b6, #ec4899);
        color: #fff; border: none; border-radius: 14px;
        font-family: 'Nunito', sans-serif; font-weight: 800; font-size: 0.95rem;
        padding: .7rem 1.8rem; width: 100%; cursor: pointer;
        box-shadow: 0 6px 20px rgba(236,72,153,0.32);
        transition: box-shadow .2s, transform .1s;
    }
    div.stButton > button:hover {
        box-shadow: 0 8px 28px rgba(236,72,153,0.45); transform: translateY(-1px);
    }
 
    /* Botón descarga */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #f472b6, #ec4899);
        color: #fff; border: none; border-radius: 14px;
        font-family: 'Nunito', sans-serif; font-weight: 800; font-size: 0.95rem;
        padding: .7rem 1.8rem; width: 100%; cursor: pointer;
        box-shadow: 0 6px 20px rgba(236,72,153,0.32);
        transition: box-shadow .2s, transform .1s;
    }
    div.stDownloadButton > button:hover { 
        box-shadow: 0 8px 28px rgba(236,72,153,0.45); transform: translateY(-1px);
    }
 
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff !important; border-right: 1.5px solid #f0edf8;
    }
    [data-testid="stSidebar"] label {
        color: #7b78a8 !important; font-size: 0.83rem; font-weight: 700;
    }
    [data-testid="stSidebar"] h3 { color: #1e1b40 !important; font-weight: 800; }
 
    /* Divider */
    hr { border-color: #ede9f8; margin: 1.2rem 0; }
 
    /* Sección título */
    .section-title { font-size: 1rem; font-weight: 800; color: #1e1b40; margin-bottom: .6rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Generador de Grafos</h1>
        <p>Configura el modelo → Genera el grafo → Descarga el archivo .dot</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ────────────────────────────────────────────────────────────────────────────
# Sidebar – Configuración del modelo
# ────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # ────────────────────────────────────────────────────────────────────────────
    # Reiniciar dashboard
    # ────────────────────────────────────────────────────────────────────────────
    if st.button("🔄 Reiniciar Dashboard", use_container_width=True):
        # Limpia todas las variables guardadas en la memoria
        st.session_state.clear()
        # Recarga la página instantáneamente
        st.rerun()
    st.markdown("---")
    #Parametros
    st.markdown("### ⚙️ Parámetros")
    st.markdown("---")

    MODELOS = {
        "Erdős–Rényi  (n, m)":        "erdos",
        "Gilbert  (n, p)":             "gilbert",
        "Geográfico simple  (n, r)":   "geografico",
        "Malla  (n × m)":              "malla",
        "Barabási–Albert  (n, d)":     "barabasi",
        "Dorogovtsev–Mendes  (n)":     "dorogovtsev",
    }

    modelo_label = st.selectbox("Modelo de generación", list(MODELOS.keys()))
    modelo_key   = MODELOS[modelo_label]

    tipo_grafo = st.radio(
        "Tipo de grafo",
        ["Undirected", "Directed"],
        horizontal=True,
        help="Solo aplica a los modelos que lo admiten.",
    )

    st.markdown("---")

    # ── Parámetros según modelo ──────────────────────────────────────────
    params = {}

    if modelo_key == "erdos":
        params["n"] = st.number_input("n  (nodos)", min_value=2, max_value=5000, value=50, step=1)
        max_m = params["n"] * (params["n"] - 1) // (1 if tipo_grafo == "Directed" else 2)
        params["m"] = st.number_input("m  (aristas)", min_value=0, max_value=max_m, value=min(80, max_m), step=1)

    elif modelo_key == "gilbert":
        params["n"] = st.number_input("n  (nodos)", min_value=2, max_value=5000, value=50, step=1)
        params["p"] = st.slider("p  (probabilidad de arista)", 0.0, 1.0, 0.15, 0.01)

    elif modelo_key == "geografico":
        params["n"] = st.number_input("n  (nodos)", min_value=2, max_value=5000, value=50, step=1)
        params["r"] = st.slider("r  (radio de conexión)", 0.01, round(math.sqrt(2), 4), 0.30, 0.01)

    elif modelo_key == "malla":
        params["n"] = st.number_input("Filas", min_value=1, max_value=200, value=5, step=1)
        params["m"] = st.number_input("Columnas", min_value=1, max_value=200, value=5, step=1)

    elif modelo_key == "barabasi":
        params["n"] = st.number_input("n  (nodos)", min_value=2, max_value=5000, value=50, step=1)
        params["d"] = st.number_input("d  (grado inicial)", min_value=1, max_value=max(1, int(params.get("n", 50)) - 1), value=3, step=1)

    elif modelo_key == "dorogovtsev":
        params["n"] = st.number_input("n  (nodos)", min_value=3, max_value=5000, value=50, step=1)

    st.markdown("---")
    generar_btn = st.button("▶  Generar grafo", use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📂 Importar Grafo")
    st.markdown("---")
    
    archivo_dot = st.file_uploader("Sube un archivo .dot", type=["dot"])
    cargar_btn = st.button("📥 Cargar archivo", use_container_width=True)
    


# ────────────────────────────────────────────────────────────────────────────
# Estado de sesión
# ────────────────────────────────────────────────────────────────────────────
if "grafo"    not in st.session_state: st.session_state.grafo    = None
if "dot_str"  not in st.session_state: st.session_state.dot_str  = ""
if "modelo"   not in st.session_state: st.session_state.modelo   = ""
if "error"    not in st.session_state: st.session_state.error    = ""
if "grafo_bfs" not in st.session_state: st.session_state.grafo_bfs = None
if "dot_bfs"   not in st.session_state: st.session_state.dot_bfs   = ""
if "bfs_root"  not in st.session_state: st.session_state.bfs_root  = None
if "grafo_dfs_r" not in st.session_state: st.session_state.grafo_dfs_r = None
if "dot_dfs_r"   not in st.session_state: st.session_state.dot_dfs_r   = ""
if "dfs_r_root" not in st.session_state: st.session_state.dfs_r_root = None
if "grafo_dfs_i" not in st.session_state: st.session_state.grafo_dfs_i = None
if "dot_dfs_i"   not in st.session_state: st.session_state.dot_dfs_i   = ""
if "dfs_i_root" not in st.session_state: st.session_state.dfs_i_root = None
if "grafo_dijkstra" not in st.session_state: st.session_state.grafo_dijkstra = None
if "dot_dijkstra"   not in st.session_state: st.session_state.dot_dijkstra   = ""
if "root_dijkstra" not in st.session_state: st.session_state.root_dijkstra = None

# ────────────────────────────────────────────────────────────────────────────
# Generación
# ────────────────────────────────────────────────────────────────────────────
if generar_btn:
    st.session_state.error = ""
    try:
        g: Graph

        if modelo_key == "erdos":
            g = generar_erdos_renyi(int(params["n"]), int(params["m"]), tipo_grafo)

        elif modelo_key == "gilbert":
            g = generar_gilbert(int(params["n"]), float(params["p"]), tipo_grafo)

        elif modelo_key == "geografico":
            g = generar_geografico_simple(int(params["n"]), float(params["r"]), tipo_grafo)

        elif modelo_key == "malla":
            g = generar_malla(int(params["n"]), int(params["m"]), tipo_grafo)

        elif modelo_key == "barabasi":
            g = generar_barabasi(int(params["n"]), int(params["d"]), tipo_grafo)

        elif modelo_key == "dorogovtsev":
            g = generar_dorogovtsev(int(params["n"]), tipo_grafo)

        st.session_state.grafo   = g
        st.session_state.dot_str = grafo_a_dot(g)
        st.session_state.modelo  = modelo_label

    except ValueError as e:
        st.session_state.error = str(e)
        st.session_state.grafo = None

# ────────────────────────────────────────────────────────────────────────────
# Cargar
# ────────────────────────────────────────────────────────────────────────────
if cargar_btn:
    st.session_state.error = ""
    if archivo_dot is not None:
        try:
            # Leer el archivo como texto utf-8
            contenido = archivo_dot.getvalue().decode("utf-8")
            
            # Reconstruir el grafo
            g_importado = cargar_grafo_desde_dot_texto(contenido)
            
            # Limpiamos árboles de algoritmos previos
            st.session_state.grafo_bfs = None 
            st.session_state.grafo_dfs_r = None
            
            # Guardamos el grafo importado en la sesión
            st.session_state.grafo   = g_importado
            st.session_state.dot_str = contenido
            st.session_state.modelo  = "Grafo importado desde .dot"
            
        except Exception as e:
            st.session_state.error = f"Error al procesar el archivo .dot: {e}"
            st.session_state.grafo = None
    else:
        st.session_state.error = "Por favor selecciona un archivo antes de presionar 'Cargar'."

# ────────────────────────────────────────────────────────────────────────────
# Resultados
# ────────────────────────────────────────────────────────────────────────────
if st.session_state.error:
    st.error(f"❌ {st.session_state.error}")

elif st.session_state.grafo is not None:
    g       = st.session_state.grafo
    dot_str = st.session_state.dot_str
    stats   = stats_grafo(g)

    # ── Estadísticas ─────────────────────────────────────────────────────
    st.markdown(f"#### Grafo generado · `{st.session_state.modelo}`")
    cols = st.columns(5)
    labels = list(stats.keys())
    values = list(stats.values())
    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f'<div class="stat-card">'
                f'<div class="stat-value">{values[i]}</div>'
                f'<div class="stat-label">{labels[i]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("**📄 Vista previa del archivo `.dot`**")
    # Mostrar solo las primeras 60 líneas para no saturar
    lineas = dot_str.split("\n")
    preview = "\n".join(lineas[:60])
    if len(lineas) > 60:
        preview += f"\n... ({len(lineas) - 60} líneas más)"
    st.markdown(f'<div class="dot-box">{preview}</div>', unsafe_allow_html=True)


    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Descarga ──────────────────────────────────────────────────────────
    nombre_archivo = f"{modelo_key}_{stats['Nodos']}nodos.dot"
    st.download_button(
        label=f"Descargar  {nombre_archivo}",
        data=dot_str.encode("utf-8"),
        file_name=nombre_archivo,
        mime="text/plain",
        use_container_width=True,
    )
    
    #--BFS--
    mostrar_seccion_bfs()
    #--DFS Recursivo--
    mostrar_seccion_dfs_r()
    #--DFS iterativo--
    mostrar_seccion_dfs_i()
    
    mostrar_seccion_dijkstra()

else:
    # Estado vacío
    st.markdown(
        """
        <div style="text-align:center; padding:4rem 2rem; color:#4a3d70;">
            <div style="font-size:4rem;">💡</div>
            <div style="font-family:'Space Mono',monospace; font-size:1rem; margin-top:1rem;">
                Selecciona un modelo en el panel lateral<br>y presiona <b>Generar grafo</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
