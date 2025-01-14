"""Utility functions for the panel_full_calendar package."""


def to_camel_case(string: str) -> str:
    """
    Convert snake_case to camelCase.

    Args:
        string (str): snake_case string

    Returns:
        str: camelCase string
    """
    return "".join(word.capitalize() if i else word for i, word in enumerate(string.split("_")))


def to_camel_case_keys(d: dict) -> dict:
    """
    Convert snake_case keys to camelCase.

    Args:
        d (dict): dictionary with snake_case keys

    Returns:
        dict: dictionary with camelCase keys
    """
    return {to_camel_case(key) if "_" in key else key: val for key, val in d.items()}


def to_snake_case(string: str) -> str:
    """
    Convert camelCase to snake_case.

    Args:
        string (str): camelCase string

    Returns:
        str: snake_case string
    """
    return "".join(f"_{char.lower()}" if char.isupper() else char for char in string)


def to_snake_case_keys(d: dict):
    """
    Convert camelCase keys to snake_case.

    Args:
        d (dict): dictionary with camelCase keys

    Returns:
        dict: dictionary with snake
    """
    return {to_snake_case(key): val for key, val in d.items()}
