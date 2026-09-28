"""Console program to manage a catalog of collectible pieces.

Comments tagged "[SKILL n START] ... [SKILL n END]" mark where each workshop
fundamental is applied. The numbering is explained in README.md.
"""
from catalog import (
    add_piece,
    filter_by_status,
    find_piece_by_id,
    get_average_price,
    list_pieces,
    piece_exists,
    remove_piece,
)
from validations import ALLOWED_STATUSES

# [SKILL 1 START] Variables and basic data types (str constants)
EXIT_OPTION = "7"

MENU = """
===== Catálogo de coleccionables =====
1. Agregar una pieza
2. Mostrar todas las piezas
3. Mostrar piezas disponibles
4. Mostrar el precio promedio
5. Buscar una pieza por identificador
6. Eliminar una pieza
7. Salir"""
# [SKILL 1 END]


def read_text(prompt):
    """Ask the user for a text and return it without surrounding whitespace."""
    # [SKILL 2 START] Capturing information from the terminal (input)
    # [SKILL 5 START/END] String manipulation (strip)
    return input(prompt).strip()
    # [SKILL 2 END]


def read_price(prompt):
    """Ask the user for a price and return it as a float.

    Raises ValueError if the text cannot be converted to a number.
    """
    # [SKILL 2 START/END] Capturing information from the terminal (via read_text)
    # [SKILL 5 START/END] String manipulation (replace: "450,50" -> "450.50")
    raw_price = read_text(prompt).replace(",", ".")
    # [SKILL 12 START] Error handling: try / except + raise
    try:
        # [SKILL 3 START/END] Converting text to a number
        return float(raw_price)
    except ValueError:
        raise ValueError("El precio debe ser un número, por ejemplo 450.50.") from None
    # [SKILL 12 END]
