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


def format_piece(piece):
    """Return a printable, multi-line description of a piece."""
    # [SKILL 5 START] String manipulation (f-string interpolation and number formatting)
    return (
        f"[{piece['id']}] {piece['name']} | {piece['category']} | "
        f"${piece['price']:.2f} | {piece['status']}\n"
        f"    {piece['description']}"
    )
    # [SKILL 5 END]


# [SKILL 10 START] Separating, encapsulating and reusing logic with functions
# Each handle_* function has one responsibility: one menu option. The real
# work is delegated to functions of catalog.py, so nothing is repeated here.


def handle_add_piece(catalog):
    # [SKILL 2 START] Capturing information from the terminal
    piece_id = read_text("Identificador: ")
    # [SKILL 11 START] Early validation: reject a duplicated id before asking more data
    if piece_exists(catalog, piece_id):
        raise ValueError(f"Ya existe una pieza con el id '{piece_id}'.")
    # [SKILL 11 END]
    name = read_text("Nombre: ")
    category = read_text("Categoría: ")
    price = read_price("Precio: ")
    # [SKILL 5 START/END] String manipulation (lower: "DISPONIBLE" -> "disponible")
    status = read_text(f"Estado ({', '.join(ALLOWED_STATUSES)}): ").lower()
    description = read_text("Descripción (debe incluir 'usada' o 'certificada'): ")
    # [SKILL 2 END]

    piece = add_piece(piece_id, name, category, price, status, description)
    # [SKILL 6 START/END] Working with objects: adding a dictionary to the list
    catalog.append(piece)
    print(f"Pieza '{piece['name']}' agregada correctamente.")


def handle_show_all(catalog):
    names = list_pieces(catalog)
    # [SKILL 8 START] Conditional: empty catalog or not
    if not names:
        print("El catálogo está vacío.")
        return
    # [SKILL 8 END]
    print(f"--- Piezas del catálogo ({len(names)}) ---")
    # [SKILL 9 START] Loop: print every name with a number
    for number, name in enumerate(names, start=1):
        print(f"{number}. {name}")
    # [SKILL 9 END]


def handle_show_available(catalog):
    available_pieces = filter_by_status(catalog, "disponible")
    if not available_pieces:
        print("No hay piezas disponibles.")
        return
    print("--- Piezas disponibles ---")
    # [SKILL 9 START] Loop: print every available piece
    for piece in available_pieces:
        print(format_piece(piece))
    # [SKILL 9 END]


def handle_show_average(catalog):
    if not catalog:
        print("El catálogo está vacío: no hay precio promedio que mostrar.")
        return
    print(f"Precio promedio: ${get_average_price(catalog):.2f}")


def handle_find_piece(catalog):
    piece_id = read_text("Identificador a buscar: ")
    piece = find_piece_by_id(catalog, piece_id)
    # [SKILL 8 START] Conditional: found or not found
    if piece is None:
        print(f"No se encontró ninguna pieza con el id '{piece_id}'.")
    else:
        print(format_piece(piece))
    # [SKILL 8 END]


def handle_remove_piece(catalog):
    piece_id = read_text("Identificador a eliminar: ")
    # [SKILL 8 START] Conditional: removed or not found (True / False from remove_piece)
    if remove_piece(catalog, piece_id):
        print(f"Pieza '{piece_id}' eliminada correctamente.")
    else:
        print(f"No se encontró ninguna pieza con el id '{piece_id}'.")
    # [SKILL 8 END]


# [SKILL 6 START] Working with objects: a dictionary that maps each option to a function
MENU_ACTIONS = {
    "1": handle_add_piece,
    "2": handle_show_all,
    "3": handle_show_available,
    "4": handle_show_average,
    "5": handle_find_piece,
    "6": handle_remove_piece,
}
# [SKILL 6 END]
# [SKILL 10 END]


def run_menu(catalog):
    """Show the menu until the user chooses to exit."""
    # [SKILL 9 START] Loop: repeat the menu until the user exits
    while True:
        print(MENU)
        option = read_text("Seleccione una opción: ")
        # [SKILL 8 START] Conditionals: exit, invalid option or valid option
        if option == EXIT_OPTION:
            print("¡Hasta pronto!")
            break

        action = MENU_ACTIONS.get(option)
        if action is None:
            print("Error: opción inválida. Elija un número del 1 al 7.")
            continue
        # [SKILL 8 END]

        # [SKILL 12 START] Error handling: catch the errors raised by the functions
        try:
            action(catalog)
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")
        # [SKILL 12 END]
    # [SKILL 9 END]


def main():
    # [SKILL 1 START/END] Variables: the catalog starts as an empty list
    catalog = []
    # [SKILL 12 START] Error handling: Ctrl+C or Ctrl+D do not crash the program
    try:
        run_menu(catalog)
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido por el usuario.")
    # [SKILL 12 END]


if __name__ == "__main__":
    main()
