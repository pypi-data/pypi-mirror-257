# Python Imports
import base64
import hashlib
import logging

# Project-Specific Imports
from platform_microservices_utils.config.env import SecretKeyProvider

# Third-Party Imports

# Django Imports

# Relative Import


class KeyDerivationBase:
    """
    Base class for key derivation using PBKDF2.
    """

    @classmethod
    def derive_key(cls, secret_key=None, request_id=None, iterations=100000):
        """
        Derive a key using PBKDF2.
        """
        logger = logging.getLogger(__name__)
        logger.info("Deriving key...")

        combined_key = cls._combine_keys(request_id, secret_key)

        # Use PBKDF2 to derive a key
        derived_key = hashlib.pbkdf2_hmac(
            "sha256", combined_key.encode(), b"", iterations=iterations
        )
        encoded_key = base64.b64encode(derived_key).decode("utf-8")
        logger.info("Key derived successfully.")

        # Log the derived key
        logger.info("Derived key: %s", encoded_key)

        return encoded_key

    @classmethod
    def _combine_keys(cls, request_id, secret_key):
        """
        Combine the secret key and request ID with a specific format.
        """
        return f"{secret_key}###{request_id}"


class KeyGenerationUtility:
    """Utility class for key generation."""

    @classmethod
    def get_secret_key(cls):
        """Get the secret key."""
        return SecretKeyProvider.get_secret_key()
