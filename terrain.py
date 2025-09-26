from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class TerrainType:
    """Clase que representa un tipo de terreno con sus propiedades."""
    name: str
    cost: float
    color: str
    walkable: bool = True

class Terrain:
    """Clase que contiene los diferentes tipos de terreno disponibles."""
    # Definición de tipos de terreno
    NORMAL = TerrainType('normal', 1.0, 'green')
    GRASS = TerrainType('grass', 1.3, 'lightgreen')
    SAND = TerrainType('sand', 1.7, 'sandybrown')
    WATER = TerrainType('water', float('inf'), 'blue', walkable=False)
    MOUNTAIN = TerrainType('mountain', 2.5, 'gray')
    ROAD = TerrainType('road', 0.7, 'darkgray')
    
    # Mapeo de tipos de terreno para búsqueda rápida
    _terrain_types = {
        'normal': NORMAL,
        'grass': GRASS,
        'sand': SAND,
        'water': WATER,
        'mountain': MOUNTAIN,
        'road': ROAD
    }
    
    @classmethod
    def get_terrain(cls, name: str) -> TerrainType:
        """Obtiene un tipo de terreno por su nombre.
        
        Args:
            name: Nombre del terreno a buscar
            
        Returns:
            El tipo de terreno correspondiente o el tipo normal si no se encuentra
        """
        return cls._terrain_types.get(name.lower(), cls.NORMAL)
    
    @classmethod
    def get_terrain_cost(cls, terrain_name: str) -> float:
        """Obtiene el costo de movimiento para un tipo de terreno.
        
        Args:
            terrain_name: Nombre del terreno
            
        Returns:
            El costo de movimiento del terreno
        """
        terrain = cls.get_terrain(terrain_name)
        return terrain.cost if terrain else cls.NORMAL.cost
    
    @classmethod
    def is_walkable(cls, terrain_name: str) -> bool:
        """Verifica si un tipo de terreno es transitable.
        
        Args:
            terrain_name: Nombre del terreno
            
        Returns:
            True si el terreno es transitable, False en caso contrario
        """
        terrain = cls.get_terrain(terrain_name)
        return terrain.walkable if terrain else True
    
    @classmethod
    def get_terrain_color(cls, terrain_name: str) -> str:
        """Obtiene el color asociado a un tipo de terreno.
        
        Args:
            terrain_name: Nombre del terreno
            
        Returns:
            El color en formato string reconocible por matplotlib
        """
        terrain = cls.get_terrain(terrain_name)
        return terrain.color if terrain else 'white'
    
    @classmethod
    def get_available_terrains(cls) -> Dict[str, TerrainType]:
        """Obtiene todos los tipos de terreno disponibles.
        
        Returns:
            Un diccionario con los tipos de terreno disponibles
        """
        return cls._terrain_types.copy()
