"""Console program to manage a catalog of collectible pieces."""
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


def read_text(prompt):
    """Ask the user for a text and return it without surrounding whitespace."""
    return input(prompt).strip()


def read_price(prompt):
    """Ask the user for a price and return it as a float.

    Raises ValueError if the text cannot be converted to a number.
    """
    raw_price = read_text(prompt).replace(",", ".")
    try:
        return float(raw_price)
    except ValueError:
        raise ValueError("El precio debe ser un número, por ejemplo 450.50.") from None


def format_piece(piece):
    """Return a printable, multi-line description of a piece."""
    return (
        f"[{piece['id']}] {piece['name']} | {piece['category']} | "
        f"${piece['price']:.2f} | {piece['status']}\n"
        f"    {piece['description']}"
    )


def handle_add_piece(catalog):
    piece_id = read_text("Identificador: ")
    if piece_exists(catalog, piece_id):
        raise ValueError(f"Ya existe una pieza con el id '{piece_id}'.")
    name = read_text("Nombre: ")
    category = read_text("Categoría: ")
    price = read_price("Precio: ")
    status = read_text(f"Estado ({', '.join(ALLOWED_STATUSES)}): ").lower()
    description = read_text("Descripción (debe incluir 'usada' o 'certificada'): ")

    piece = add_piece(piece_id, name, category, price, status, description)
    catalog.append(piece)
    print(f"Pieza '{piece['name']}' agregada correctamente.")


def handle_show_all(catalog):
    names = list_pieces(catalog)
    if not names:
        print("El catálogo está vacío.")
        return
    print(f"--- Piezas del catálogo ({len(names)}) ---")
    for number, name in enumerate(names, start=1):
        print(f"{number}. {name}")


def handle_show_available(catalog):
    available_pieces = filter_by_status(catalog, "disponible")
    if not available_pieces:
        print("No hay piezas disponibles.")
        return
    print("--- Piezas disponibles ---")
    for piece in available_pieces:
        print(format_piece(piece))


def handle_show_average(catalog):
    if not catalog:
        print("El catálogo está vacío: no hay precio promedio que mostrar.")
        return
    print(f"Precio promedio: ${get_average_price(catalog):.2f}")


def handle_find_piece(catalog):
    piece_id = read_text("Identificador a buscar: ")
    piece = find_piece_by_id(catalog, piece_id)
    if piece is None:
        print(f"No se encontró ninguna pieza con el id '{piece_id}'.")
    else:
        print(format_piece(piece))


def handle_remove_piece(catalog):
    piece_id = read_text("Identificador a eliminar: ")
    if remove_piece(catalog, piece_id):
        print(f"Pieza '{piece_id}' eliminada correctamente.")
    else:
        print(f"No se encontró ninguna pieza con el id '{piece_id}'.")


MENU_ACTIONS = {
    "1": handle_add_piece,
    "2": handle_show_all,
    "3": handle_show_available,
    "4": handle_show_average,
    "5": handle_find_piece,
    "6": handle_remove_piece,
}


def run_menu(catalog):
    """Show the menu until the user chooses to exit."""
    while True:
        print(MENU)
        option = read_text("Seleccione una opción: ")
        if option == EXIT_OPTION:
            print("¡Hasta pronto!")
            break

        action = MENU_ACTIONS.get(option)
        if action is None:
            print("Error: opción inválida. Elija un número del 1 al 7.")
            continue

        try:
            action(catalog)
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


def main():
    catalog = []
    try:
        run_menu(catalog)
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido por el usuario.")


if __name__ == "__main__":
    main()
