from functools import lru_cache

from ._exceptions import AutomizorVaultError
from ._secret import Secret


@lru_cache
def _get_vault():
    from ._vault import Vault

    return Vault()


def get_secret(name: str) -> Secret:
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

    vault = _get_vault()
    return vault.get_secret(name)


def set_secret(secret: Secret) -> Secret:
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

    vault = _get_vault()
    return vault.set_secret(secret)


__all__ = [
    "AutomizorVaultError",
    "Secret",
    "get_secret",
    "set_secret",
]
