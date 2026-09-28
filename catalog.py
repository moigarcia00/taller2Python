"""Catalog operations for collectible pieces.

A piece is a dictionary with the keys: id, name, category, price, status
and description. The catalog is a plain list of pieces.

Comments tagged "[SKILL n START] ... [SKILL n END]" mark where each workshop
fundamental is applied. The numbering is explained in README.md.
"""
from validations import (
    validate_catalog,
    validate_description,
    validate_not_empty,
    validate_number,
    validate_price,
    validate_status,
    validate_text,
)


def _clean_text(value):
    """Strip surrounding whitespace from text values; leave other types untouched."""
    # [SKILL 5 START] String manipulation (strip)
    return value.strip() if isinstance(value, str) else value
    # [SKILL 5 END]


def add_piece(piece_id, name, category, price, status, description):
    """Build and return a validated piece dictionary.

    Raises ValueError if any field is empty or invalid.
    """
    # [SKILL 5 START] String manipulation (cleaning every text field)
    piece_id, name, category, status, description = (
        _clean_text(field) for field in (piece_id, name, category, status, description)
    )
    # [SKILL 5 END]

    # [SKILL 11 START] Early validations: fail before building anything
    validate_not_empty(piece_id, "identificador")
    validate_not_empty(name, "nombre")
    validate_not_empty(category, "categoría")
    validate_text(piece_id, "identificador")
    validate_text(name, "nombre")
    validate_text(category, "categoría")
    validate_not_empty(price, "precio")
    validate_not_empty(status, "estado")
    validate_not_empty(description, "descripción")
    validate_price(price)
    validate_status(status)
    validate_description(description)
    # [SKILL 11 END]

    # [SKILL 6 START] Working with objects: building a dictionary
    # [SKILL 10 START] Function that delivers its result with return
    return {
        "id": piece_id,
        "name": name,
        "category": category.capitalize(),  # "cartas" and "Cartas" are the same category
        "price": float(price),  # [SKILL 3] converting to a decimal number
        "status": status,
        "description": description,
    }
    # [SKILL 10 END]
    # [SKILL 6 END]


def list_pieces(catalog):
    """Return the names of all pieces in the catalog.

    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)  # [SKILL 11 START/END] early validation
    # [SKILL 6 START] Working with objects: reading a key from every dictionary in a list
    return [piece["name"] for piece in catalog]
    # [SKILL 6 END]


def find_piece_by_id(catalog, piece_id):
    """Return the piece with the given id, or None if there is no match.

    Not finding a piece is a valid result, so no exception is raised for it.
    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)  # [SKILL 11 START/END] early validation
    # [SKILL 9 START] Loop: go through the catalog
    for piece in catalog:
        # [SKILL 8 START] Conditional + comparison operator (==)
        if piece["id"] == piece_id:
            return piece
        # [SKILL 8 END]
    # [SKILL 9 END]
    return None


def remove_piece(catalog, piece_id):
    """Remove the piece with the given id from the catalog (in place).

    Return True if it was removed and False if it was not found.
    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)  # [SKILL 11 START/END] early validation
    # [SKILL 12 START] Error handling: raise + try / except
    try:
        # [SKILL 10 START/END] Reusing find_piece_by_id instead of repeating the search
        piece = find_piece_by_id(catalog, piece_id)
        if piece is None:
            raise LookupError(f"No se encontró ninguna pieza con el id '{piece_id}'.")
        catalog.remove(piece)
    except LookupError:
        return False
    # [SKILL 12 END]
    return True


def get_catalog_summary(catalog):
    """Return a dictionary with the number of pieces per category.

    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)  # [SKILL 11 START/END] early validation
    # [SKILL 6 START] Working with objects: a dictionary used as a counter
    summary = {}
    # [SKILL 9 START] Loop: go through the catalog
    for piece in catalog:
        category = piece["category"]
        # [SKILL 7 START/END] Arithmetic operator (+)
        summary[category] = summary.get(category, 0) + 1
    # [SKILL 9 END]
    # [SKILL 6 END]
    return summary


def get_pieces_by_category(catalog, category):
    """Return the names of the pieces in a category (case-insensitive).

    Return an empty list when nothing matches.
    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)  # [SKILL 11 START/END] early validation
    # [SKILL 5 START/END] String manipulation (strip + casefold to compare ignoring case)
    wanted = str(category).strip().casefold()
    # [SKILL 9 START/END] Loop (list comprehension) with a comparison operator (==)
    return [piece["name"] for piece in catalog if piece["category"].casefold() == wanted]


def piece_exists(catalog, piece_id):
    """Return True if a piece with the given id is in the catalog, else False."""
    # [SKILL 10 START/END] Reusing find_piece_by_id (no duplicated search logic)
    return find_piece_by_id(catalog, piece_id) is not None


def filter_by_status(catalog, status):
    """Return the pieces that have the given status.

    Raises ValueError if the status is not allowed and TypeError if the
    catalog is not a list.
    """
    # [SKILL 11 START] Early validations
    validate_catalog(catalog)
    validate_status(status)
    # [SKILL 11 END]
    return [piece for piece in catalog if piece["status"] == status]


def filter_by_min_price(catalog, min_price):
    """Return the pieces whose price is strictly greater than min_price.

    Raises ValueError if min_price is not numeric and TypeError if the
    catalog is not a list.
    """
    # [SKILL 11 START] Early validations
    validate_catalog(catalog)
    validate_number(min_price, "precio mínimo")
    # [SKILL 11 END]
    # [SKILL 7 START/END] Comparison operator (>)
    return [piece for piece in catalog if piece["price"] > min_price]


def get_average_price(catalog):
    """Return the average price of all pieces, or 0 if the catalog is empty.

    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)  # [SKILL 11 START/END] early validation
    # [SKILL 12 START] Error handling: try / except
    try:
        validate_not_empty(catalog, "catálogo")
    except ValueError:
        return 0
    # [SKILL 12 END]
    # [SKILL 7 START/END] Arithmetic operators (sum, /)
    return sum(piece["price"] for piece in catalog) / len(catalog)
