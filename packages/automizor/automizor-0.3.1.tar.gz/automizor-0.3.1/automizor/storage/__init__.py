from functools import lru_cache

from ._exceptions import AutomizorStorageError
from ._storage import JSON


@lru_cache
def _get_storage():
    from ._storage import Storage

    return Storage()


def get_bytes(name: str) -> bytes:
    """
    Retrieves the specified asset as raw bytes.

    Parameters:
        name: The name identifier of the asset to retrieve.

    Returns:
        The raw byte content of the asset.
    """

    storage = _get_storage()
    return storage.get_bytes(name)


def get_file(name: str, path: str) -> str:
    """
    Downloads the specified asset and saves it to a file.

    Parameters:
        name: The name identifier of the asset to retrieve.
        path: The filesystem path where the file will be saved.

    Returns:
        The path to the saved file, confirming the operation's success.
    """

    storage = _get_storage()
    return storage.get_file(name, path)


def get_json(name: str) -> JSON:
    """
    Retrieves the specified asset and parses it as JSON.

    Parameters:
        name: The name identifier of the asset to retrieve.

    Returns:
        The parsed JSON data, which can be a dict, list, or primitive data type.
    """

    storage = _get_storage()
    return storage.get_json(name)


def get_text(name: str) -> str:
    """
    Retrieves the specified asset as a text string.

    Parameters:
        name: The name identifier of the asset to retrieve.

    Returns:
        The content of the asset as a text string.
    """

    storage = _get_storage()
    return storage.get_text(name)


__all__ = [
    "AutomizorStorageError",
    "get_bytes",
    "get_file",
    "get_json",
    "get_text",
]
