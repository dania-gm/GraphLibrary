import streamlit as st
import sys
import os
import io
import math

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
        
        lineas.append(f'    "{u}" {conector} "{v}";')
        
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
    st.markdown("### Parámetros")
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

# ────────────────────────────────────────────────────────────────────────────
# Estado de sesión
# ────────────────────────────────────────────────────────────────────────────
if "grafo"    not in st.session_state: st.session_state.grafo    = None
if "dot_str"  not in st.session_state: st.session_state.dot_str  = ""
if "modelo"   not in st.session_state: st.session_state.modelo   = ""
if "error"    not in st.session_state: st.session_state.error    = ""

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
        label=f"⬇️  Descargar  {nombre_archivo}",
        data=dot_str.encode("utf-8"),
        file_name=nombre_archivo,
        mime="text/plain",
        use_container_width=True,
    )

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