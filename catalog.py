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
