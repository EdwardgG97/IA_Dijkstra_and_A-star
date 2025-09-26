# Sistema de Búsqueda de Rutas con Sistema Experto

Este proyecto implementa un sistema de búsqueda de rutas en un mapa 2D utilizando algoritmos de búsqueda clásicos (Dijkstra y A*) con un sistema experto que permite tomar decisiones inteligentes sobre el terreno a transitar.

## Características Principales

- **Algoritmos de Búsqueda**:
  - Algoritmo de Dijkstra
  - Algoritmo A* (A estrella)
  
- **Sistema Experto**:
  - Evita automáticamente el agua a menos que sea la única opción
  - Toma decisiones basadas en el tipo de terreno
  
- **Tipos de Terreno**:
  - 🌊 Agua (alto costo, evitable)
  - 🌿 Hierba (bajo costo)
  - 🌲 Bosque (costo medio)
  - 🏔️ Montaña (alto costo)
  - 🏁 Punto de inicio/final

## Requisitos del Sistema

- Python 3.7 o superior
- Bibliotecas requeridas:
  - numpy
  - matplotlib

## Instalación

1. Clona el repositorio o descarga los archivos
2. Instala las dependencias:
   ```
   pip install numpy matplotlib
   ```

## Uso

1. Ejecuta el programa principal:
   ```
   python main.py
   ```

2. Sigue las instrucciones en pantalla para:
   - Seleccionar un mapa (ejemplo o aleatorio)
   - Elegir si deseas evitar el agua
   - Ver los resultados de la búsqueda

## Estructura del Proyecto

- `main.py`: Punto de entrada del programa
- `graph.py`: Implementación del grafo y algoritmos de búsqueda
- `node.py`: Clase Node para representar nodos en el grafo
- `terrain.py`: Definición de tipos de terreno y sus propiedades
- `visualization.py`: Funciones para visualizar el mapa y las rutas

## Ejemplo de Salida

El programa generará una ventana con dos gráficos que muestran:
1. La ruta encontrada por el algoritmo de Dijkstra
2. La ruta encontrada por el algoritmo A*

Cada gráfico muestra:
- Los diferentes tipos de terreno con colores
- El camino óptimo encontrado
- Los nodos visitados durante la búsqueda

## Personalización

Puedes modificar los siguientes aspectos:
- Los costos de movimiento en `terrain.py`
- El tamaño del mapa en `main.py`
- La posición de inicio y fin
- Las reglas del sistema experto en `graph.py`

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
