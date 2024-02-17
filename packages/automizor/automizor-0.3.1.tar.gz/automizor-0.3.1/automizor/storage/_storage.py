import os
from typing import Dict, List, Union

import requests

from ._exceptions import AutomizorStorageError

JSON = Union[str, int, float, bool, None, Dict[str, "JSON"], List["JSON"]]


class Storage:
    """
    `Storage` is a class designed to interact with the `Automizor Platform` for managing
    digital assets, facilitating the retrieval of files in various formats such as bytes,
    files, JSON, and text. It leverages the `Automizor Storage API` to access and download
    these assets securely.

    This class utilizes environment variables for configuration, specifically for setting
    up the API host and API token, which are essential for authenticating requests made
    to the `Automizor Storage API`. These variables are typically configured by the
    `Automizor Agent`.

    To use this class effectively, ensure that the following environment variables are
    set in your environment:

    - ``AUTOMIZOR_API_HOST``: Specifies the host URL of the `Automizor Storage API`.
    - ``AUTOMIZOR_API_TOKEN``: Provides the token required for API authentication.

    Example usage:

    .. code-block:: python

        from automizor import storage

        # To get bytes of an asset
        bytes_data = storage.get_bytes("asset_name")

        # To save an asset to a file
        file_path = storage.get_file("asset_name", "/path/to/save/file")

        # To retrieve an asset as JSON
        json_data = storage.get_json("asset_name")

        # To get the text content of an asset
        text_data = storage.get_text("asset_name")
    """

    def __init__(self):
        self._api_host = os.getenv("AUTOMIZOR_API_HOST")
        self._api_token = os.getenv("AUTOMIZOR_API_TOKEN")

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Token {self._api_token}",
                "Content-Type": "application/json",
            }
        )

    def get_bytes(self, name: str) -> bytes:
        """
        Retrieves the specified asset as raw bytes.

        This function fetches the asset identified by `name` from the storage service
        and returns it as a byte stream. It is useful for binary files or for data
        that is intended to be processed or stored in its raw form.

        Parameters:
            name: The name identifier of the asset to retrieve.

        Returns:
            The raw byte content of the asset.
        """

        url = self._get_asset_url(name)
        return self._download_file(url, mode="content")

    def get_file(self, name: str, path: str) -> str:
        """
        Downloads the specified asset and saves it to a file.

        This function fetches the asset identified by `name` and saves it directly
        to the filesystem at the location specified by `path`. It is useful for
        downloading files that need to be preserved in the file system, such as
        documents, images, or other files.

        Parameters:
            name: The name identifier of the asset to retrieve.
            path: The filesystem path where the file will be saved.

        Returns:
            The path to the saved file, confirming the operation's success.
        """

        url = self._get_asset_url(name)
        content = self._download_file(url, mode="content")
        with open(path, "wb") as file:
            file.write(content)
        return path

    def get_json(self, name: str) -> JSON:
        """
        Retrieves the specified asset and parses it as JSON.

        This function fetches the asset identified by `name` from the storage service
        and parses it as JSON. It is useful for assets stored in JSON format, allowing
        for easy access and manipulation of structured data.

        Parameters:
            name: The name identifier of the asset to retrieve.

        Returns:
            The parsed JSON data, which can be a dict, list, or primitive data type.
        """

        url = self._get_asset_url(name)
        return self._download_file(url, mode="json")

    def get_text(self, name: str) -> str:
        """
        Retrieves the specified asset as a text string.

        This function fetches the asset identified by `name` from the storage service
        and returns it as a text string. It is useful for text-based files, such as
        configuration files, CSVs, or plain text documents.

        Parameters:
            name: The name identifier of the asset to retrieve.

        Returns:
            The content of the asset as a text string.
        """

        url = self._get_asset_url(name)
        return self._download_file(url, mode="text")

    def _download_file(self, url: str, mode: str = "content"):
        try:
            session = requests.Session()
            response = session.get(url, timeout=10)
            response.raise_for_status()

            match mode:
                case "content":
                    return response.content
                case "json":
                    return response.json()
                case "text":
                    return response.text
            raise RuntimeError(f"Invalid mode {mode}")
        except Exception as exc:
            raise AutomizorStorageError(f"Failed to download asset: {exc}") from exc

    def _get_asset_url(self, name: str) -> str:
        url = f"https://{self._api_host}/api/v1/storage/asset/{name}/"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            url = response.json().get("file")
            if url:
                return url
            raise RuntimeError("Url not found")
        except Exception as exc:
            raise AutomizorStorageError(f"Failed to get asset url: {exc}") from exc
