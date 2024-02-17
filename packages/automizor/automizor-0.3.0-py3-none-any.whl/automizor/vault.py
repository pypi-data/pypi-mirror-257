import json
import os
from dataclasses import asdict, dataclass

import requests


class AutomizorVaultError(RuntimeError):
    """Exception raised for errors encountered while interacting with the Vault."""


@dataclass
class Secret:
    """
    Represents a secret, comprising a name and its associated values.

    Attributes:
        name (str): The name of the secret.
        value (dict): The secret's values, stored in a dictionary as key-value pairs.
    """

    name: str
    value: dict

    def get(self, key, default=None):
        """Return the value for key if key is in the dictionary, else default."""
        return self.value.get(key, default)

    def items(self):
        """secret.items() -> a set-like object providing a view on secret's items."""
        return self.value.items()

    def update(self, pairs: dict) -> None:
        self.value.update(pairs)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def __contains__(self, key):
        return key in self.value

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)

    def __repr__(self):
        keys = ", ".join(self.value.keys())
        return f"Secret(name={self.name}, keys={keys})"


class Vault:
    """
    `Vault` is a library to manage secrets within an the `Automizor Platform`,
    providing functionality to retrieve and update secrets. It supports interaction
    with the `Vault API` (by default) or a local file for secret storage, determined
    by environment variable configuration.

    The Vault class uses environment variables to configure the API host, API token,
    which are set by the `Automizor Agent`.

    You may want to set the environment variables in your local environment for testing
    purposes. The variables which must exist are:

    - ``AUTOMIZOR_API_HOST``: The host URL of the `Automizor API`
    - ``AUTOMIZOR_API_TOKEN``: The token used for authenticating with the `Automizor API`

    In addition, you can set the following environment variable to use a local file for
    secret storage:

    - ``AUTOMIZOR_SECRET_FILE``: The path to a local file where secrets are stored.

    Example of a local secret file:

    .. code-block:: json

        {
            "my_secret_name": {
                "key": "value"
            }
        }

    Example usage:

    .. code-block:: python

        from automizor.vault import Vault

        vault = Vault()

        def read_secret():
            secret = vault.get_secret("my_secret_name")
            print(secret["key"])  # Output: "value"

        def update_secret():
            secret = vault.get_secret("my_secret_name")
            secret["new_key"] = "new_value"
            vault.set_secret(secret)

    """

    def __init__(self):
        self._api_host = os.getenv("AUTOMIZOR_API_HOST")
        self._api_token = os.getenv("AUTOMIZOR_API_TOKEN")
        self._secret_file = os.getenv("AUTOMIZOR_SECRET_FILE")

    @property
    def headers(self) -> dict:
        """Headers for API requests, including Authorization and Content-Type."""
        return {
            "Authorization": f"Token {self._api_token}",
            "Content-Type": "application/json",
        }

    def get_secret(self, name) -> Secret:
        """
        Retrieves a secret by its name. Fetches from a local file or queries the
        `Automizor API`, based on configuration.

        Args:
            name (str): The name of the secret to retrieve.

        Returns:
            Secret: The retrieved secret.

        Raises:
            AutomizorVaultError: If retrieving the secret fails.
        """

        if self._secret_file:
            return self._read_file_secret(name)
        return self._read_vault_secret(name)

    def set_secret(self, secret: Secret) -> Secret:
        """
        Updates a secret. Writes to a local file or sends to the `Automizor API`,
        based on configuration.

        Args:
            secret (Secret): The secret to update.

        Returns:
            Secret: The updated secret.

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
            response = requests.get(url, headers=self.headers, timeout=10)
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
            response = requests.put(
                url, headers=self.headers, timeout=10, json=asdict(secret)
            )
            response.raise_for_status()
            return Secret(**response.json())
        except Exception as exc:
            raise AutomizorVaultError(f"Failed to set secret: {exc}") from exc
