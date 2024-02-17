from dataclasses import dataclass


@dataclass
class Secret:
    """
    Represents a secret, comprising a name and its associated values.

    Attributes:
        name: The name of the secret.
        value: The secret's values, stored in a dictionary as key-value pairs.
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
