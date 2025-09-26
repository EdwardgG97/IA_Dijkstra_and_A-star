import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import ListedColormap
from typing import List, Set, Optional, Tuple, Dict
import matplotlib.colors as mcolors

from node import Node
from terrain import Terrain

def create_colormap():
    """Crea un mapa de colores para los diferentes tipos de terreno."""
    # Obtener todos los tipos de terreno
    terrains = Terrain.get_available_terrains().values()
    
    # Crear un diccionario de colores
    colors = {}
    for terrain in terrains:
        colors[terrain.name] = terrain.color
    
    # Crear un colormap personalizado
    cmap = ListedColormap([terrain.color for terrain in terrains])
    
    # Crear un mapeo de valores a nombres de terreno
    terrain_to_value = {terrain.name: i for i, terrain in enumerate(terrains)}
    
    return colors, cmap, terrain_to_value

def plot_map(graph, path: List[Node] = None, visited: Set[Node] = None, 
             start_node: Node = None, end_node: Node = None, 
             title: str = "Mapa del Juego", show_grid: bool = True):
    """
    Visualiza el mapa del juego con opciones para mostrar rutas y nodos visitados.
    
    Args:
        graph: Grafo del juego
        path: Lista de nodos que forman el camino óptimo
        visited: Conjunto de nodos visitados durante la búsqueda
        start_node: Nodo de inicio
        end_node: Nodo de destino
        title: Título del gráfico
        show_grid: Si se muestra la cuadrícula
    """
    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Obtener dimensiones del mapa
    width, height = graph.width, graph.height
    
    # Crear matriz para el mapa de terreno
    terrain_map = np.zeros((width, height))
    
    # Obtener el mapeo de terreno a valor
    _, _, terrain_to_value = create_colormap()
    
    # Llenar la matriz con los valores de terreno
    for x in range(width):
        for y in range(height):
            terrain_type = graph.terrain[x][y] or 'normal'
            terrain_map[x, y] = terrain_to_value.get(terrain_type, 0)
    
    # Transponer la matriz para que coincida con las coordenadas de matplotlib
    terrain_map = terrain_map.T
    
    # Crear el mapa de colores
    colors, cmap, _ = create_colormap()
    
    # Mostrar el mapa de terreno
    plt.imshow(terrain_map, cmap=cmap, origin='lower', 
               extent=[-0.5, width-0.5, -0.5, height-0.5],
               aspect='equal')
    
    # Dibujar la cuadrícula si es necesario
    if show_grid:
        ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
        ax.grid(which="minor", color="black", linestyle='-', linewidth=0.5)
        ax.tick_params(which="minor", size=0)
    
    # Dibujar nodos visitados
    if visited:
        visited_x = [node.x for node in visited]
        visited_y = [node.y for node in visited]
        ax.scatter(visited_x, visited_y, color='yellow', alpha=0.3, s=50, 
                  label='Nodos visitados')
    
    # Dibujar el camino
    if path and len(path) > 1:
        path_x = [node.x for node in path]
        path_y = [node.y for node in path]
        ax.plot(path_x, path_y, 'r-', linewidth=2, label='Camino óptimo')
    
    # Dibujar nodo de inicio y fin
    if start_node:
        ax.scatter([start_node.x], [start_node.y], color='lime', s=200, 
                  marker='s', edgecolor='black', label='Inicio')
    
    if end_node:
        ax.scatter([end_node.x], [end_node.y], color='red', s=200, 
                  marker='X', edgecolor='black', label='Destino')
    
    # Configuración del gráfico
    ax.set_xticks(range(width))
    ax.set_yticks(range(height))
    ax.set_xlim(-0.5, width-0.5)
    ax.set_ylim(-0.5, height-0.5)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    
    # Crear leyenda para los tipos de terreno
    legend_elements = []
    for name, color in colors.items():
        legend_elements.append(patches.Patch(facecolor=color, label=name.capitalize()))
    
    # Agregar leyenda de terreno
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Agregar leyenda de elementos adicionales si es necesario
    if path or visited or start_node or end_node:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

def compare_algorithms(graph, start_node: Node, end_node: Node):
    """
    Compara los algoritmos de búsqueda mostrando los resultados en una sola figura.
    
    Args:
        graph: Grafo del juego
        start_node: Nodo de inicio
        end_node: Nodo de destino
    """
    from graph import PathFinder
    
    # Crear figura con subgráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Ejecutar Dijkstra
    graph.reset_nodes()
    path_dijkstra, visited_dijkstra = PathFinder.dijkstra(graph, start_node, end_node)
    
    # Ejecutar A*
    graph.reset_nodes()
    path_astar, visited_astar = PathFinder.a_star(graph, start_node, end_node)
    
    # Obtener información del mapa de terreno
    terrain_map = np.zeros((graph.width, graph.height))
    _, _, terrain_to_value = create_colormap()
    
    for x in range(graph.width):
        for y in range(graph.height):
            terrain_type = graph.terrain[x][y] or 'normal'
            terrain_map[x, y] = terrain_to_value.get(terrain_type, 0)
    
    # Transponer para visualización
    terrain_map = terrain_map.T
    
    # Dibujar Dijkstra
    ax1.imshow(terrain_map, cmap=plt.cm.tab20, origin='lower', 
               extent=[-0.5, graph.width-0.5, -0.5, graph.height-0.5],
               aspect='equal')
    
    # Dibujar nodos visitados en Dijkstra
    if visited_dijkstra:
        visited_x = [node.x for node in visited_dijkstra]
        visited_y = [node.y for node in visited_dijkstra]
        ax1.scatter(visited_x, visited_y, color='yellow', alpha=0.3, s=50)
    
    # Dibujar camino en Dijkstra
    if path_dijkstra:
        path_x = [node.x for node in path_dijkstra]
        path_y = [node.y for node in path_dijkstra]
        ax1.plot(path_x, path_y, 'r-', linewidth=2)
    
    # Dibujar inicio y fin en Dijkstra
    ax1.scatter([start_node.x], [start_node.y], color='lime', s=200, 
                marker='s', edgecolor='black')
    ax1.scatter([end_node.x], [end_node.y], color='red', s=200, 
                marker='X', edgecolor='black')
    
    # Configurar Dijkstra subplot
    ax1.set_title('Algoritmo de Dijkstra', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Coordenada X')
    ax1.set_ylabel('Coordenada Y')
    ax1.set_xticks(range(graph.width))
    ax1.set_yticks(range(graph.height))
    ax1.grid(True, which='both', color='black', linestyle='-', linewidth=0.5)
    
    # Dibujar A*
    ax2.imshow(terrain_map, cmap=plt.cm.tab20, origin='lower', 
               extent=[-0.5, graph.width-0.5, -0.5, graph.height-0.5],
               aspect='equal')
    
    # Dibujar nodos visitados en A*
    if visited_astar:
        visited_x = [node.x for node in visited_astar]
        visited_y = [node.y for node in visited_astar]
        ax2.scatter(visited_x, visited_y, color='yellow', alpha=0.3, s=50, 
                   label=f'Nodos visitados ({len(visited_astar)})')
    
    # Dibujar camino en A*
    if path_astar:
        path_x = [node.x for node in path_astar]
        path_y = [node.y for node in path_astar]
        ax2.plot(path_x, path_y, 'r-', linewidth=2, 
                label=f'Camino (longitud: {len(path_astar)-1})')
    
    # Dibujar inicio y fin en A*
    ax2.scatter([start_node.x], [start_node.y], color='lime', s=200, 
                marker='s', edgecolor='black', label='Inicio')
    ax2.scatter([end_node.x], [end_node.y], color='red', s=200, 
                marker='X', edgecolor='black', label='Destino')
    
    # Configurar A* subplot
    ax2.set_title('Algoritmo A*', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Coordenada X')
    ax2.set_ylabel('Coordenada Y')
    ax2.set_xticks(range(graph.width))
    ax2.set_yticks(range(graph.height))
    ax2.grid(True, which='both', color='black', linestyle='-', linewidth=0.5)
    
    # Agregar leyenda para A*
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Ajustar diseño y mostrar
    plt.tight_layout()
    plt.show()
    
    # Imprimir estadísticas
    print("\nComparación de algoritmos:")
    print(f"{'Métrica':<20} {'Dijkstra':<15} {'A*':<15}")
    print("-" * 40)
    print(f"{'Nodos visitados:':<20} {len(visited_dijkstra):<15} {len(visited_astar):<15}")
    print(f"{'Longitud del camino:':<20} {len(path_dijkstra)-1 if path_dijkstra else 'N/A':<15} {len(path_astar)-1 if path_astar else 'N/A':<15}")
    
    return path_dijkstra, path_astar, visited_dijkstra, visited_astar
