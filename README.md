# 📊 Biblioteca de Grafos — Dashboard Interactivo

> Dashboard interactivo para la generación, importación y análisis de grafos, construido con **Python + Streamlit**.

---

## 🧩 Descripción

Esta herramienta permite generar grafos sintéticos con distintos modelos teóricos, aplicar algoritmos clásicos de análisis de redes y exportar los resultados en formato `.dot` compatible con Graphviz y Gephi.

Fue desarrollada como herramienta de apoyo para la materia de Diseño y Análisis de Algortimos en el Centro de Investigación en Computación.

---

## 🚀 Características

### Generadores de grafos
| Modelo | Parámetros | Descripción |
|---|---|---|
| Erdős–Rényi | `n`, `m` | Grafo aleatorio con número exacto de aristas |
| Gilbert | `n`, `p` | Grafo aleatorio con probabilidad de conexión |
| Geográfico simple | `n`, `r` | Nodos en espacio unitario conectados por radio |
| Malla | `n × m` | Rejilla rectangular determinista |
| Barabási–Albert | `n`, `d` | Red libre de escala por conexión preferencial |
| Dorogovtsev–Mendes | `n` | Red planar siempre conexa, grado mínimo 2 |

- Soporte para grafos **dirigidos** y **no dirigidos**
- Generación configurable desde la barra lateral
- Vista previa del archivo `.dot` generado
- Descarga directa del archivo de salida

### Algoritmos implementados
- **BFS** — Árbol de búsqueda en anchura
- **DFS Recursivo** — Árbol de búsqueda en profundidad (versión recursiva)
- **DFS Iterativo** — Árbol de búsqueda en profundidad (versión iterativa)
- **Dijkstra** — Caminos más cortos desde un nodo origen
- **Kruskal Directo** — Árbol de expansión mínima (orden ascendente)
- **Kruskal Inverso** — Árbol de expansión mínima (orden descendente)
- **Prim** — Árbol de expansión mínima expansión incremental

### Importación de grafos
- Carga de archivos `.dot` externos
- Compatible con grafos generados por otras herramientas

---

## 🗂️ Estructura del proyecto

```
BIBLI.../
├── BFS/                    # Módulo algoritmo BFS
├── DFS_I/                  # Módulo DFS Iterativo
├── DFS_R/                  # Módulo DFS Recursivo
├── Dijkstra/               # Módulo algoritmo Dijkstra
├── KruskalD/               # Módulo Kruskal Directo
├── KruskalI/               # Módulo Kruskal Inverso
├── Prim/                   # Módulo algoritmo Prim
├── modelo_barabasi/        # Generador Barabási–Albert
├── modelo_dorogovtsev/     # Generador Dorogovtsev–Mendes
├── modelo_erdos_renyi/     # Generador Erdős–Rényi
├── modelo_geografico/      # Generador Geográfico simple
├── modelo_gilbert/         # Generador Gilbert
├── modelo_malla/           # Generador Malla
├── algoritmos_gener...py   # Lógica de generación de grafos
├── dashboard.py            # Interfaz Streamlit principal
├── edge.py                 # Clase Arista
├── export_gephi.py         # Exportación a formato Gephi
├── graph.py                # Clase Grafo
├── main.py                 # Punto de entrada [Sigue en producción]
├── node.py                 # Clase Nodo
└── test.py                 # Pruebas unitarias [Sigue en producción]
```

---


## ▶️ Uso

```bash
streamlit run dashboard.py
```

El dashboard se abrirá automáticamente en `http://localhost:8501`.

### Flujo básico

1. **Configura** el modelo de generación en el panel lateral
2. **Selecciona** tipo de grafo (dirigido / no dirigido)
3. **Ajusta** los parámetros (`n`, y el parámetro específico del modelo)
4. **Presiona** `► Generar grafo`
5. **Descarga** el archivo `.dot` o aplica algoritmos en la sección inferior

---

## 📤 Exportación

Los grafos se exportan en formato **DOT** (`.dot`), compatible con:
- [Graphviz](https://graphviz.org/)
- [Gephi](https://gephi.org/) (vía `export_gephi.py`)

Nombre de archivo generado automáticamente: `{modelo}_{n}nodos.dot`

---

## 📐 Métricas calculadas

Al generar un grafo, el dashboard muestra automáticamente:

| Métrica | Descripción |
|---|---|
| Nodos | Número total de vértices |
| Aristas | Número total de enlaces |
| Grado mínimo | Nodo menos conectado |
| Grado máximo | Nodo más conectado (hub) |
| Grado promedio | Conectividad media de la red |

---

## ✍️ Autor

Desarrollado por Dania Garcia Montiel.
