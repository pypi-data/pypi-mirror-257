# Python Imports
import uuid

# Third-Party Imports

# Django Imports

# Project-Specific Imports

# Relative Import

class DynamicAttributes:
    """
    A class for creating dynamic objects with key-value pairs as attributes.

    Args:
        **kwargs: Key-value pairs to be assigned as object attributes.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class QueryParams:
    """A class for dynamically creating query parameters."""

    def __init__(self, **kwargs):
        """Initialize the QueryParams with the provided parameters."""
        self.params = kwargs

    def add_param(self, key, value):
        """Add a query parameter."""
        self.params[key] = value

    def remove_param(self, key):
        """Remove a query parameter."""
        if key in self.params:
            del self.params[key]

    def generate_query_string(self):
        """Generate the query string."""
        query_string = "&".join(
            [f"{key}={value}" for key, value in self.params.items()]
        )
        return f"{query_string}" if query_string else ""


class UUIDGenerator:
    """
    Utility class for generating UUIDs.
    """

    @classmethod
    def generate_uuid(cls):
        """
        Generates a UUID.
        """
        return str(uuid.uuid4())
