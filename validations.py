"""Validation helpers for collectible pieces.

Every function raises an exception when the data is invalid and never prints
anything: the caller decides how to report the error to the user.

Comments tagged "[SKILL n START] ... [SKILL n END]" mark where each workshop
fundamental is applied. The numbering is explained in README.md.
"""
import math
import re

# [SKILL 1 START] Variables and basic data types
# Module-level constants: tuples of strings.
ALLOWED_STATUSES = ("disponible", "reservada", "vendida")
REQUIRED_DESCRIPTION_WORDS = ("usada", "certificada")
# [SKILL 1 END]


# [SKILL 11 START] Early validations
# Every function below checks one rule and stops the flow (raise) as soon as
# the data is wrong, before anything else is built or calculated.


def validate_not_empty(value, field_name):
    """Raise ValueError if the value is None, blank text or an empty collection."""
    # [SKILL 4 START] Checking the type of the stored data (isinstance)
    is_blank_text = isinstance(value, str) and not value.strip()
    is_empty_collection = isinstance(value, (list, tuple, dict, set)) and len(value) == 0
    # [SKILL 4 END]
    # [SKILL 12 START] Raising an exception
    if value is None or is_blank_text or is_empty_collection:
        raise ValueError(f"El campo '{field_name}' no puede estar vacío.")
    # [SKILL 12 END]


def validate_text(value, field_name):
    """Raise ValueError if the value is not a string."""
    # [SKILL 4 START] Checking the type of the stored data (isinstance)
    if not isinstance(value, str):
        raise ValueError(f"El campo '{field_name}' debe ser un texto.")
    # [SKILL 4 END]


def validate_number(value, field_name):
    """Raise ValueError if the value is not a finite int or float."""
    # [SKILL 4 START] Checking the type of the stored data (isinstance)
    # bool is a subclass of int, so it has to be rejected explicitly.
    is_number = isinstance(value, (int, float)) and not isinstance(value, bool)
    # [SKILL 4 END]
    # [SKILL 7 START] Logical operators (or, not)
    if not is_number or not math.isfinite(value):
        raise ValueError(f"El campo '{field_name}' debe ser numérico.")
    # [SKILL 7 END]


def validate_price(price):
    """Raise ValueError if the price is not a number greater than zero."""
    validate_number(price, "precio")
    # [SKILL 7 START] Comparison operator (<=)
    if price <= 0:
        raise ValueError("El precio debe ser mayor que cero.")
    # [SKILL 7 END]


def validate_status(status):
    """Raise ValueError if the status is not one of the allowed statuses."""
    # [SKILL 8 START] Conditional: accept or reject the status
    if status not in ALLOWED_STATUSES:
        allowed = ", ".join(ALLOWED_STATUSES)
        raise ValueError(f"Estado inválido '{status}'. Estados permitidos: {allowed}.")
    # [SKILL 8 END]


def validate_description(description):
    """Raise ValueError if the description lacks the word 'usada' or 'certificada'."""
    if not isinstance(description, str):
        raise ValueError("La descripción debe ser un texto.")
    # [SKILL 5 START] String manipulation (lower, regex to split into words)
    words = set(re.findall(r"\w+", description.lower()))
    # [SKILL 5 END]
    if not words.intersection(REQUIRED_DESCRIPTION_WORDS):
        raise ValueError("La descripción debe contener la palabra 'usada' o 'certificada'.")


def validate_catalog(catalog):
    """Raise TypeError if the catalog is not a list."""
    if not isinstance(catalog, list):
        raise TypeError("El catálogo debe ser una lista de piezas.")


# [SKILL 11 END]
