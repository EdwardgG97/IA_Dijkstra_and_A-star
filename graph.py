import math
from typing import List, Dict, Set, Tuple, Optional
import heapq
from node import Node
from terrain import Terrain

class Graph:
    """Clase que representa el grafo del mapa del juego."""
    
    def __init__(self, width: int, height: int):
        """
        Inicializa un nuevo grafo con las dimensiones especificadas.
        
        Args:
            width: Ancho del mapa
            height: Alto del mapa
        """
        self.width = width
        self.height = height
        self.nodes = [[Node(x, y) for y in range(height)] for x in range(width)]
        self.terrain = [[None for _ in range(height)] for _ in range(width)]
    
    def get_node(self, x: int, y: int) -> Optional[Node]:
        """Obtiene un nodo en las coordenadas especificadas."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.nodes[x][y]
        return None
    
    def set_terrain(self, x: int, y: int, terrain_type: str):
        """Establece el tipo de terreno para un nodo."""
        if 0 <= x < self.width and 0 <= y < self.height:
            node = self.nodes[x][y]
            node.terrain_type = terrain_type
            node.walkable = Terrain.is_walkable(terrain_type)
            self.terrain[x][y] = terrain_type
    
    def has_alternative_path_without_water(self, current: Node, target: Node) -> bool:
        """
        Verifica si hay un camino alternativo al objetivo que no pase por agua.
        
        Args:
            current: Nodo actual
            target: Nodo objetivo a alcanzar
            
        Returns:
            True si existe un camino alternativo sin agua, False en caso contrario
        """
        # Si el objetivo es agua, no hay alternativa
        if target.terrain_type == 'water':
            return False
            
        # Verificar si hay al menos un vecino que no sea agua
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current.x + dx, current.y + dy
            if (0 <= nx < self.width and 0 <= ny < self.height):
                neighbor = self.nodes[nx][ny]
                if neighbor.walkable and neighbor.terrain_type != 'water' and neighbor != target:
                    return True
        return False

    def get_neighbors(self, node: Node, avoid_water: bool = True) -> List[Node]:
        """
        Obtiene los vecinos transitables de un nodo.
        
        Args:
            node: Nodo del que se obtendrán los vecinos
            avoid_water: Si es True, intentará evitar el agua a menos que sea la única opción
            
        Returns:
            Lista de nodos vecinos transitables
        """
        neighbors = []
        water_neighbors = []
        
        # Coordenadas relativas de los 8 vecinos posibles
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Horizontal/vertical
            (1, 1), (1, -1), (-1, -1), (-1, 1)   # Diagonales
        ]
        
        for dx, dy in directions:
            nx, ny = node.x + dx, node.y + dy
            
            # Verificar límites del mapa
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
                
            neighbor = self.nodes[nx][ny]
            
            # Solo considerar nodos transitables
            if not neighbor.walkable:
                continue
                
            # Separar vecinos de agua
            if neighbor.terrain_type == 'water':
                water_neighbors.append(neighbor)
            else:
                neighbors.append(neighbor)
        
        # Regla del sistema experto: evitar agua a menos que sea la única opción
        if avoid_water and neighbors:
            return neighbors
        
        # Si no hay vecinos normales, devolver los de agua (si los hay)
        return neighbors + water_neighbors
    
    def get_terrain_cost(self, from_node: Node, to_node: Node) -> float:
        """
        Calcula el costo de movimiento entre dos nodos adyacentes.
        
        Args:
            from_node: Nodo de origen
            to_node: Nodo de destino
            
        Returns:
            El costo de movimiento entre los nodos
        """
        # Costo del terreno del nodo de destino
        terrain_cost = Terrain.get_terrain_cost(to_node.terrain_type)
        
        # Si es movimiento diagonal, multiplicar por raíz de 2
        dx = abs(from_node.x - to_node.x)
        dy = abs(from_node.y - to_node.y)
        distance = math.sqrt(2) if dx > 0 and dy > 0 else 1.0
        
        return terrain_cost * distance
    
    def reset_nodes(self):
        """Reinicia los valores de los nodos para una nueva búsqueda."""
        for x in range(self.width):
            for y in range(self.height):
                node = self.nodes[x][y]
                node.g_cost = float('inf')
                node.h_cost = 0
                node.parent = None


class PathFinder:
    """Clase que implementa algoritmos de búsqueda de rutas."""
    
    @staticmethod
    def heuristic(node: Node, end_node: Node) -> float:
        """
        Función heurística para A* (distancia euclidiana).
        
        Args:
            node: Nodo actual
            end_node: Nodo destino
            
        Returns:
            Distancia estimada desde node hasta end_node
        """
        dx = abs(node.x - end_node.x)
        dy = abs(node.y - end_node.y)
        return math.sqrt(dx*dx + dy*dy)
    
    @staticmethod
    def reconstruct_path(current_node: Node) -> List[Node]:
        """
        Reconstruye el camino desde el nodo final hasta el inicial.
        
        Args:
            current_node: Nodo final del camino
            
        Returns:
            Lista de nodos que forman el camino
        """
        path = []
        current = current_node
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # Invertir para ir desde inicio hasta fin
    
    @classmethod
    def dijkstra(cls, graph: Graph, start: Node, end: Node, avoid_water: bool = True) -> Tuple[List[Node], Set[Node]]:
        """
        Implementación del algoritmo de Dijkstra para encontrar el camino más corto.
        
        Args:
            graph: Grafo que representa el mapa
            start: Nodo de inicio
            end: Nodo de destino
            avoid_water: Si es True, intentará evitar el agua a menos que sea la única opción
            
        Returns:
            Tupla con (camino, nodos visitados)
        """
        # Reiniciar los nodos
        graph.reset_nodes()
        
        # Inicializar el nodo de inicio
        start.g_cost = 0
        
        # Conjunto de nodos por visitar
        open_set = [(0, id(start), start)]
        open_set_dict = {id(start): start}
        closed_set = set()
        
        while open_set:
            # Obtener el nodo con menor costo actual
            current_cost, _, current = heapq.heappop(open_set)
            
            # Si llegamos al destino, reconstruir y retornar el camino
            if current == end:
                return cls.reconstruct_path(current), closed_set
            
            # Si ya visitamos este nodo con un costo menor, lo saltamos
            if current in closed_set:
                continue
                
            closed_set.add(current)
            
            # Explorar vecinos con la regla de evitar agua
            for neighbor in graph.get_neighbors(current, avoid_water=avoid_water):
                if neighbor in closed_set:
                    continue
                
                # Calcular nuevo costo
                tentative_g_cost = current.g_cost + graph.get_terrain_cost(current, neighbor)
                
                # Si encontramos un camino mejor al vecino
                if tentative_g_cost < neighbor.g_cost:
                    neighbor.parent = current
                    neighbor.g_cost = tentative_g_cost
                    
                    # Agregar a la cola de prioridad
                    if id(neighbor) not in open_set_dict or open_set_dict[id(neighbor)] != neighbor:
                        heapq.heappush(open_set, (neighbor.g_cost, id(neighbor), neighbor))
                        open_set_dict[id(neighbor)] = neighbor
        
        # Si llegamos aquí, no hay camino
        return [], closed_set
    
    @classmethod
    def a_star(cls, graph: Graph, start: Node, end: Node, avoid_water: bool = True) -> Tuple[List[Node], Set[Node]]:
        """
        Implementación del algoritmo A* para encontrar el camino más corto.
        
        Args:
            graph: Grafo que representa el mapa
            start: Nodo de inicio
            end: Nodo de destino
            avoid_water: Si es True, intentará evitar el agua a menos que sea la única opción
            
        Returns:
            Tupla con (camino, nodos visitados)
        """
        # Reiniciar los nodos
        graph.reset_nodes()
        
        # Inicializar el nodo de inicio
        start.g_cost = 0
        start.h_cost = cls.heuristic(start, end)
        
        # Conjunto de nodos por visitar
        open_set = [(start.f_cost, id(start), start)]
        open_set_dict = {id(start): start}
        closed_set = set()
        
        while open_set:
            # Obtener el nodo con menor f_cost
            _, _, current = heapq.heappop(open_set)
            
            # Si llegamos al destino, reconstruir y retornar el camino
            if current == end:
                return cls.reconstruct_path(current), closed_set
            
            # Si ya visitamos este nodo, lo saltamos
            if current in closed_set:
                continue
                
            closed_set.add(current)
            
            # Explorar vecinos con la regla de evitar agua
            for neighbor in graph.get_neighbors(current, avoid_water=avoid_water):
                if neighbor in closed_set:
                    continue
                
                # Calcular nuevo costo
                tentative_g_cost = current.g_cost + graph.get_terrain_cost(current, neighbor)
                
                # Si encontramos un camino mejor al vecino
                if tentative_g_cost < neighbor.g_cost:
                    neighbor.parent = current
                    neighbor.g_cost = tentative_g_cost
                    neighbor.h_cost = cls.heuristic(neighbor, end)
                    
                    # Agregar a la cola de prioridad
                    if id(neighbor) not in open_set_dict or open_set_dict[id(neighbor)] != neighbor:
                        heapq.heappush(open_set, (neighbor.f_cost, id(neighbor), neighbor))
                        open_set_dict[id(neighbor)] = neighbor
        
        # Si llegamos aquí, no hay camino
        return [], closed_set
