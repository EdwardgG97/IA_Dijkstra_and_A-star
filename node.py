class Node:
    """
    Clase que representa un nodo en el grafo del mapa del juego.
    """
    def __init__(self, x: int, y: int, terrain_type: str = 'normal'):
        """
        Inicializa un nuevo nodo.
        
        Args:
            x (int): Coordenada x en el mapa
            y (int): Coordenada y en el mapa
            terrain_type (str): Tipo de terreno del nodo (afecta el costo de movimiento)
        """
        self.x = x
        self.y = y
        self.terrain_type = terrain_type
        self.g_cost = float('inf')  # Costo desde el inicio hasta este nodo
        self.h_cost = 0            # Heurística (distancia estimada al destino)
        self.parent = None         # Nodo padre en el camino óptimo
        self.walkable = True       # Si el nodo es transitable
    
    @property
    def f_cost(self) -> float:
        """Costo total del nodo (g + h)."""
        return self.g_cost + self.h_cost
    
    def __lt__(self, other):
        """Comparación para ordenar nodos por f_cost."""
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        """Comparación de igualdad basada en coordenadas."""
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        """Hash basado en coordenadas para usar en conjuntos y diccionarios."""
        return hash((self.x, self.y))
    
    def __str__(self):
        """Representación en cadena del nodo."""
        return f'Node({self.x}, {self.y}, {self.terrain_type})'
    
    def __repr__(self):
        """Representación detallada del nodo."""
        return f'Node(x={self.x}, y={self.y}, terrain={self.terrain_type}, g={self.g_cost}, h={self.h_cost}, f={self.f_cost})'
