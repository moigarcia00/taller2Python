"""Validation helpers for collectible pieces.

Every function raises an exception when the data is invalid and never prints
anything: the caller decides how to report the error to the user.
"""
import math
import re

ALLOWED_STATUSES = ("disponible", "reservada", "vendida")
REQUIRED_DESCRIPTION_WORDS = ("usada", "certificada")


def validate_not_empty(value, field_name):
    """Raise ValueError if the value is None, blank text or an empty collection."""
    is_blank_text = isinstance(value, str) and not value.strip()
    is_empty_collection = isinstance(value, (list, tuple, dict, set)) and len(value) == 0
    if value is None or is_blank_text or is_empty_collection:
        raise ValueError(f"El campo '{field_name}' no puede estar vacío.")


def validate_text(value, field_name):
    """Raise ValueError if the value is not a string."""
    if not isinstance(value, str):
        raise ValueError(f"El campo '{field_name}' debe ser un texto.")


def validate_number(value, field_name):
    """Raise ValueError if the value is not a finite int or float."""
    # bool is a subclass of int, so it has to be rejected explicitly.
    is_number = isinstance(value, (int, float)) and not isinstance(value, bool)
    if not is_number or not math.isfinite(value):
        raise ValueError(f"El campo '{field_name}' debe ser numérico.")


def validate_price(price):
    """Raise ValueError if the price is not a number greater than zero."""
    validate_number(price, "precio")
    if price <= 0:
        raise ValueError("El precio debe ser mayor que cero.")


def validate_status(status):
    """Raise ValueError if the status is not one of the allowed statuses."""
    if status not in ALLOWED_STATUSES:
        allowed = ", ".join(ALLOWED_STATUSES)
        raise ValueError(f"Estado inválido '{status}'. Estados permitidos: {allowed}.")


def validate_description(description):
    """Raise ValueError if the description lacks the word 'usada' or 'certificada'."""
    if not isinstance(description, str):
        raise ValueError("La descripción debe ser un texto.")
    words = set(re.findall(r"\w+", description.lower()))
    if not words.intersection(REQUIRED_DESCRIPTION_WORDS):
        raise ValueError("La descripción debe contener la palabra 'usada' o 'certificada'.")


def validate_catalog(catalog):
    """Raise TypeError if the catalog is not a list."""
    if not isinstance(catalog, list):
        raise TypeError("El catálogo debe ser una lista de piezas.")
