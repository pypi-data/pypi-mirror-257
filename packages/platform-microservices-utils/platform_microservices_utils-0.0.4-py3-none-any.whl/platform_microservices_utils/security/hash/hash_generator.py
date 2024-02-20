# Python Imports

# Django Imports

# Project-Specific Imports

# Third-Party Imports


# Relative Import
from .base import KeyDerivationBase, KeyGenerationUtility


class KeyDerivation(KeyDerivationBase, KeyGenerationUtility):
    """
    Utility class for key derivation using PBKDF2.
    """

    @classmethod
    def generate_key(cls, request_id):
        """
        Derive a key using PBKDF2.
        """
        return cls.derive_key(secret_key=cls.get_secret_key(), request_id=request_id)
