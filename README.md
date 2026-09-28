# Catálogo de coleccionables (Taller 2)

## Objetivo del programa

Programa de consola en Python para gestionar un catálogo básico de piezas coleccionables: registrar piezas, consultarlas, filtrarlas, calcular métricas y validar los datos que ingresa el usuario.

Este taller es la evolución del [Taller 1](https://github.com/moigarcia00/Taller1Python): la misma idea de catálogo, pero ahora con **funciones con parámetros y `return`**, **validaciones tempranas**, **manejo de errores (`try / except`)**, **lanzamiento de excepciones (`raise`)** y **código organizado en módulos**.

## Contexto del catálogo

El catálogo es una lista de piezas. Cada pieza es un diccionario:

```python
{
    "id": "COL-001",
    "name": "Carta Charizard",
    "category": "Cartas",
    "price": 450.0,
    "status": "disponible",
    "description": "Carta usada en buen estado",
}
```

Reglas de negocio:

- Ningún campo puede estar vacío.
- El precio debe ser numérico y mayor que cero.
- Estados permitidos: `disponible`, `reservada`, `vendida`.
- La descripción debe contener la palabra `usada` o `certificada`.

## Estructura del proyecto

```
catalogo_coleccionables/
├── catalog.py       # Operaciones del catálogo (agregar, listar, buscar, quitar, filtrar, métricas)
├── validations.py   # Funciones de validación reutilizables
├── main.py          # Menú interactivo y flujo del programa
└── README.md
```

- `main.py` importa `catalog.py` (y las constantes de `validations.py`).
- `catalog.py` importa `validations.py`: la lógica de validación vive en un solo lugar.

## Funcionalidades implementadas

**`validations.py`** (lanzan `ValueError`, o `TypeError` para el catálogo, y nunca imprimen):
`validate_not_empty`, `validate_text`, `validate_number`, `validate_price`, `validate_status`, `validate_description`, `validate_catalog`.

**`catalog.py`**:

| Función | Qué hace |
|---|---|
| `add_piece` | Valida los datos y retorna el diccionario de la pieza |
| `list_pieces` | Retorna los nombres de todas las piezas |
| `find_piece_by_id` | Retorna la pieza o `None` si no existe |
| `remove_piece` | Elimina la pieza; retorna `True`/`False` |
| `get_catalog_summary` | Retorna un diccionario con la cantidad de piezas por categoría |
| `get_pieces_by_category` | Retorna los nombres de las piezas de una categoría |
| `piece_exists` | Retorna `True`/`False` |
| `filter_by_status` | Retorna las piezas con un estado válido dado |
| `filter_by_min_price` | Retorna las piezas con precio mayor al indicado |
| `get_average_price` | Retorna el precio promedio (`0` si el catálogo está vacío) |

**`main.py`**: menú con las opciones 1) agregar, 2) mostrar todas, 3) mostrar disponibles, 4) precio promedio, 5) buscar por id, 6) eliminar y 7) salir. Captura los errores de las funciones y muestra mensajes claros en español.

### Decisiones de diseño

- **Errores:** las funciones de validación lanzan la excepción y quien las llama decide qué mostrar. `TypeError` se usa cuando el catálogo no es una lista; `ValueError` para datos inválidos.
- **Resultados válidos vs. errores:** no encontrar una pieza (`find_piece_by_id`, `piece_exists`) no es un error, por eso no lanzan excepción.
- **Categorías:** se normalizan al agregar (`"cartas"` y `"Cartas"` cuentan como la misma) y la búsqueda por categoría no distingue mayúsculas.
- **Idioma:** el código está en inglés y los mensajes para el usuario, en español.

## Ejemplo de interacción

```
===== Catálogo de coleccionables =====
1. Agregar una pieza
2. Mostrar todas las piezas
3. Mostrar piezas disponibles
4. Mostrar el precio promedio
5. Buscar una pieza por identificador
6. Eliminar una pieza
7. Salir
Seleccione una opción: 1
Identificador: COL-001
Nombre: Carta Charizard
Categoría: Cartas
Precio: 450
Estado (disponible, reservada, vendida): disponible
Descripción (debe incluir 'usada' o 'certificada'): Carta usada en buen estado
Pieza 'Carta Charizard' agregada correctamente.

Seleccione una opción: 1
Identificador: COL-002
Nombre: Moneda Antigua
Categoría: Monedas
Precio: abc
Error: El precio debe ser un número, por ejemplo 450.50.

Seleccione una opción: 3
--- Piezas disponibles ---
[COL-001] Carta Charizard | Cartas | $450.00 | disponible
    Carta usada en buen estado

Seleccione una opción: 4
Precio promedio: $450.00

Seleccione una opción: 6
Identificador a eliminar: COL-009
No se encontró ninguna pieza con el id 'COL-009'.

Seleccione una opción: 7
¡Hasta pronto!
```

## Tecnologías utilizadas

- Python 3 (solo biblioteca estándar: `math`, `re`)
- Git y GitHub para el control de versiones

## Cómo ejecutar el programa

1. Instala Python 3.8 o superior.
2. Clona el repositorio y entra en la carpeta:

   ```bash
   git clone <URL-DEL-REPOSITORIO>
   cd catalogo_coleccionables
   ```

3. Ejecuta el programa:

   ```bash
   python main.py
   ```

   (En algunos sistemas el comando es `python3 main.py`.)
