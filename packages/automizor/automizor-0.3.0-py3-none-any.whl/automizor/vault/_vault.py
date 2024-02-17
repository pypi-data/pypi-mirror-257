import json
import os
from dataclasses import asdict

import requests

from ._exceptions import AutomizorVaultError
from ._secret import Secret


class Vault:
    """
    `Vault` is a secure storage class within the `Automizor Platform` for managing
    secrets such as API keys, passwords, and other sensitive information. It offers
    functionality to securely retrieve and update secrets, either through direct
    interaction with the `Automizor API` or via a local secrets file, depending on
    the operational environment and configuration.

    Configuration for accessing and manipulating these secrets is driven by environment
    variables, which are essential for specifying the API's host and token for
    authentication purposes, alongside the location of a local secrets file, should
    local storage be preferred over API interaction.

    Environment variables requisite for operation include:
    - ``AUTOMIZOR_API_HOST``: The host URL for the `Automizor API`.
    - ``AUTOMIZOR_API_TOKEN``: The token for authenticate against the `Automizor API`.
    - ``AUTOMIZOR_SECRET_FILE``: Optionally specifies the path to a local file where
      secrets are stored, enabling operations in environments where direct API access
      may be restricted or unavailable.

    Example of a local secret file:

    .. code-block:: json

        {
            "my_secret_name": {
                "key": "value"
            }
        }

    Example usage:

    .. code-block:: python

        from automizor import vault

        # Retrieve a secret by its name
        secret = vault.get_secret("my_secret_name")
        print(secret["key"])  # Output: "value"

        # Update a existing secret
        secret = vault.get_secret("my_secret_name")
        secret["new_key"] = "new_value"
        vault.set_secret(secret)
    """

    def __init__(self):
        self._api_host = os.getenv("AUTOMIZOR_API_HOST")
        self._api_token = os.getenv("AUTOMIZOR_API_TOKEN")
        self._secret_file = os.getenv("AUTOMIZOR_SECRET_FILE")

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Token {self._api_token}",
                "Content-Type": "application/json",
            }
        )

    def get_secret(self, name) -> Secret:
        """
        Retrieves a secret by its name. Fetches from a local file or queries the
        `Automizor API`, based on configuration.

        Args:
            name: The name of the secret to retrieve.

        Returns:
            The retrieved secret.

        Raises:
            AutomizorVaultError: If retrieving the secret fails.
        """

        if self._secret_file:
            return self._read_file_secret(name)
        return self._read_vault_secret(name)

    def set_secret(self, secret: Secret) -> Secret:
        """
        Updates an existing secret. Updates to a local file or to the
        `Automizor API`, based on configuration.

        Args:
            secret: The secret to update.

        Returns:
            The updated secret.

        Raises:
            AutomizorVaultError: If updating the secret fails.
        """

        if self._secret_file:
            return self._write_file_secret(secret)
        return self._write_vault_secret(secret)

    def _read_file_secret(self, name: str) -> Secret:
        with open(self._secret_file, "r", encoding="utf-8") as file:
            secrets = json.load(file)
            value = secrets.get(name, {})
        return Secret(name=name, value=value)

    def _read_vault_secret(self, name: str) -> Secret:
        url = f"https://{self._api_host}/api/v1/vault/secret/{name}/"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return Secret(**response.json())
        except Exception as exc:
            raise AutomizorVaultError(f"Failed to get secret: {exc}") from exc

    def _write_file_secret(self, secret: Secret):
        with open(self._secret_file, "r+", encoding="utf-8") as file:
            secrets = json.load(file)
            secrets[secret.name] = secret.value
            file.seek(0)
            file.write(json.dumps(secrets, indent=4))
            file.truncate()
        return secret

    def _write_vault_secret(self, secret: Secret) -> Secret:
        url = f"https://{self._api_host}/api/v1/vault/secret/{secret.name}/"
        try:
            response = self.session.put(url, timeout=10, json=asdict(secret))
            response.raise_for_status()
            return Secret(**response.json())
        except Exception as exc:
            raise AutomizorVaultError(f"Failed to set secret: {exc}") from exc
