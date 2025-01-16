"""Utility functions for the panel_full_calendar package."""

import datetime

import pandas as pd


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


def normalize_datetimes(
    dt1: str | datetime.datetime | datetime.date | int,
    dt2: str | datetime.datetime | datetime.date | int,
) -> pd.Timestamp | None:
    """
    Normalize two datetime strings or objects to pandas Timestamps.

    Args:
        dt1 (str | datetime.datetime | datetime.date | int): first datetime
        dt2 (str | datetime.datetime | datetime.date | int): second datetime

    Returns:
        pd.Timestamp | None: normalized timestamps
    """
    timestamp1 = pd.to_datetime(dt1)
    timestamp2 = pd.to_datetime(dt2)

    if timestamp1.tz is not None and timestamp2.tz is not None:
        timestamp1 = timestamp1.tz_convert("UTC")
        timestamp2 = timestamp2.tz_convert("UTC")
    elif timestamp1.tz is not None and timestamp2.tz is None:
        timestamp2 = timestamp2.tz_localize(timestamp1.tz)
    elif timestamp2.tz is not None and timestamp1.tz is None:
        timestamp1 = timestamp1.tz_localize(timestamp2.tz)
    return timestamp1, timestamp2
