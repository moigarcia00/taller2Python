"""Catalog operations for collectible pieces.

A piece is a dictionary with the keys: id, name, category, price, status
and description. The catalog is a plain list of pieces.
"""
from validations import (
    validate_catalog,
    validate_description,
    validate_not_empty,
    validate_number,
    validate_price,
    validate_status,
)


def _clean_text(value):
    """Strip surrounding whitespace from text values; leave other types untouched."""
    return value.strip() if isinstance(value, str) else value


def add_piece(piece_id, name, category, price, status, description):
    """Build and return a validated piece dictionary.

    Raises ValueError if any field is empty or invalid.
    """
    piece_id, name, category, status, description = (
        _clean_text(field) for field in (piece_id, name, category, status, description)
    )

    # Early validations: fail before building anything.
    validate_not_empty(piece_id, "identificador")
    validate_not_empty(name, "nombre")
    validate_not_empty(category, "categoría")
    validate_not_empty(price, "precio")
    validate_not_empty(status, "estado")
    validate_not_empty(description, "descripción")
    validate_price(price)
    validate_status(status)
    validate_description(description)

    return {
        "id": piece_id,
        "name": name,
        "category": category,
        "price": float(price),
        "status": status,
        "description": description,
    }


def list_pieces(catalog):
    """Return the names of all pieces in the catalog.

    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)
    return [piece["name"] for piece in catalog]


def find_piece_by_id(catalog, piece_id):
    """Return the piece with the given id, or None if there is no match.

    Not finding a piece is a valid result, so no exception is raised for it.
    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)
    for piece in catalog:
        if piece["id"] == piece_id:
            return piece
    return None


def remove_piece(catalog, piece_id):
    """Remove the piece with the given id from the catalog (in place).

    Return True if it was removed and False if it was not found.
    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)
    try:
        piece = find_piece_by_id(catalog, piece_id)
        if piece is None:
            raise LookupError(f"No se encontró ninguna pieza con el id '{piece_id}'.")
        catalog.remove(piece)
    except LookupError:
        return False
    return True


def get_catalog_summary(catalog):
    """Return a dictionary with the number of pieces per category.

    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)
    summary = {}
    for piece in catalog:
        category = piece["category"]
        summary[category] = summary.get(category, 0) + 1
    return summary


def get_pieces_by_category(catalog, category):
    """Return the names of the pieces in a category (case-insensitive).

    Return an empty list when nothing matches.
    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)
    wanted = str(category).strip().casefold()
    return [piece["name"] for piece in catalog if piece["category"].casefold() == wanted]


def piece_exists(catalog, piece_id):
    """Return True if a piece with the given id is in the catalog, else False."""
    return find_piece_by_id(catalog, piece_id) is not None


def filter_by_status(catalog, status):
    """Return the pieces that have the given status.

    Raises ValueError if the status is not allowed and TypeError if the
    catalog is not a list.
    """
    validate_catalog(catalog)
    validate_status(status)
    return [piece for piece in catalog if piece["status"] == status]


def filter_by_min_price(catalog, min_price):
    """Return the pieces whose price is strictly greater than min_price.

    Raises ValueError if min_price is not numeric and TypeError if the
    catalog is not a list.
    """
    validate_catalog(catalog)
    validate_number(min_price, "precio mínimo")
    return [piece for piece in catalog if piece["price"] > min_price]


def get_average_price(catalog):
    """Return the average price of all pieces, or 0 if the catalog is empty.

    Raises TypeError if the catalog is not a list.
    """
    validate_catalog(catalog)
    try:
        validate_not_empty(catalog, "catálogo")
    except ValueError:
        return 0
    return sum(piece["price"] for piece in catalog) / len(catalog)
