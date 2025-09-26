import random
from graph import Graph, PathFinder
from node import Node
from visualization import plot_map, compare_algorithms

def create_random_map(width: int, height: int) -> Graph:
    """
    Crea un mapa aleatorio con diferentes tipos de terreno.
    
    Args:
        width: Ancho del mapa
        height: Alto del mapa
        
    Returns:
        Un grafo que representa el mapa del juego
    """
    # Crear grafo
    graph = Graph(width, height)
    
    # Tipos de terreno disponibles (con sus pesos de aparición)
    terrain_types = [
        ('normal', 0.5),
        ('grass', 0.2),
        ('sand', 0.15),
        ('water', 0.1),
        ('mountain', 0.05),
        ('road', 0.1)
    ]
    
    # Llenar el mapa con terrenos aleatorios
    for x in range(width):
        for y in range(height):
            # Asegurar que los bordes sean transitables
            if x == 0 or y == 0 or x == width-1 or y == height-1:
                graph.set_terrain(x, y, 'normal')
            else:
                # Elegir un tipo de terreno basado en los pesos
                r = random.random()
                cum_prob = 0
                for terrain, prob in terrain_types:
                    cum_prob += prob
                    if r < cum_prob:
                        graph.set_terrain(x, y, terrain)
                        break
    
    # Asegurar que haya caminos conectados
    for _ in range(10):
        x, y = random.randint(1, width-2), random.randint(1, height-2)
        graph.set_terrain(x, y, 'road')
        
        # Conectar caminos
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and random.random() < 0.3:
                graph.set_terrain(nx, ny, 'road')
    
    return graph

def create_manual_map() -> Graph:
    """
    Crea un mapa manual con diferentes tipos de terreno para pruebas.
    
    Returns:
        Un grafo que representa el mapa del juego
    """
    # Crear grafo 15x15
    graph = Graph(15, 15)
    
    # Rellenar con terreno normal
    for x in range(15):
        for y in range(15):
            graph.set_terrain(x, y, 'normal')
    
    # Agregar algunos obstáculos y terrenos especiales
    # Agua (intransitable)
    for x in range(5, 10):
        for y in range(2, 5):
            graph.set_terrain(x, y, 'water')
    
    # Montañas (transitables pero con alto costo)
    for x in range(3, 7):
        for y in range(7, 12):
            graph.set_terrain(x, y, 'mountain')
    
    # Arena (costo moderado)
    for x in range(10, 14):
        for y in range(8, 13):
            graph.set_terrain(x, y, 'sand')
    
    # Césped (costo ligeramente mayor que normal)
    for x in range(2, 13):
        for y in range(3, 4):
            graph.set_terrain(x, y, 'grass')
    
    # Caminos (bajo costo)
    for x in range(15):
        graph.set_terrain(x, 7, 'road')
    for y in range(8, 15):
        graph.set_terrain(7, y, 'road')
    
    return graph

def main():
    print("Sistema de Búsqueda de Rutas para Videojuegos")
    print("======================================\n")
    
    while True:
        print("\nOpciones:")
        print("1. Usar mapa de ejemplo")
        print("2. Generar mapa aleatorio")
        print("3. Salir")
        
        choice = input("\nSeleccione una opción (1-3): ")
        
        if choice == '1':
            # Crear mapa de ejemplo
            graph = create_manual_map()
            
            # Definir nodos de inicio y fin
            start_node = graph.get_node(1, 1)  # Esquina superior izquierda
            end_node = graph.get_node(13, 13)  # Esquina inferior derecha
            
            # Mostrar el mapa sin ruta
            plot_map(graph, title="Mapa del Juego")
            
            # Preguntar si se debe evitar el agua
            avoid_water = input("\n¿Evitar agua a menos que sea la única opción? (s/n): ").lower() == 's'
            
            # Comparar algoritmos
            print("\nComparando algoritmos de búsqueda...")
            path_dijkstra, path_astar, visited_dijkstra, visited_astar = compare_algorithms(
                graph, start_node, end_node, avoid_water=avoid_water
            )
            
            # Mostrar resultados individuales
            input("\nPresione Enter para ver los resultados de Dijkstra...")
            plot_map(graph, path=path_dijkstra, visited=visited_dijkstra,
                    start_node=start_node, end_node=end_node,
                    title=f"Algoritmo de Dijkstra - Nodos visitados: {len(visited_dijkstra)}")
            
            input("\nPresione Enter para ver los resultados de A*...")
            plot_map(graph, path=path_astar, visited=visited_astar,
                    start_node=start_node, end_node=end_node,
                    title=f"Algoritmo A* - Nodos visitados: {len(visited_astar)}")
            
        elif choice == '2':
            # Generar mapa aleatorio
            print("\nGenerando mapa aleatorio...")
            width = random.randint(10, 20)
            height = random.randint(10, 20)
            graph = create_random_map(width, height)
            
            # Elegir nodos de inicio y fin aleatorios
            while True:
                start_node = graph.get_node(
                    random.randint(0, graph.width-1),
                    random.randint(0, graph.height-1)
                )
                end_node = graph.get_node(
                    random.randint(0, graph.width-1),
                    random.randint(0, graph.height-1)
                )
                
                # Asegurarse de que los nodos sean transitables y diferentes
                if (start_node.walkable and end_node.walkable and 
                    start_node != end_node):
                    break
            
            # Mostrar el mapa sin ruta
            plot_map(graph, title="Mapa Aleatorio")
            
            # Preguntar si se debe evitar el agua
            avoid_water = input("\n¿Evitar agua a menos que sea la única opción? (s/n): ").lower() == 's'
            
            # Comparar algoritmos
            print("\nComparando algoritmos de búsqueda...")
            path_dijkstra, path_astar, visited_dijkstra, visited_astar = compare_algorithms(
                graph, start_node, end_node, avoid_water=avoid_water
            )
            
            # Mostrar resultados individuales
            input("\nPresione Enter para ver los resultados de Dijkstra...")
            plot_map(graph, path=path_dijkstra, visited=visited_dijkstra,
                    start_node=start_node, end_node=end_node,
                    title=f"Algoritmo de Dijkstra - Nodos visitados: {len(visited_dijkstra)}")
            
            input("\nPresione Enter para ver los resultados de A*...")
            plot_map(graph, path=path_astar, visited=visited_astar,
                    start_node=start_node, end_node=end_node,
                    title=f"Algoritmo A* - Nodos visitados: {len(visited_astar)}")
            
        elif choice == '3':
            print("\n¡Hasta luego!")
            break
            
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    # Instalar las dependencias necesarias
    try:
        import matplotlib
    except ImportError:
        print("Instalando dependencias necesarias...")
        import sys
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "numpy"])
        print("Dependencias instaladas correctamente.")
    
    main()
