from enum import Enum


class DefaultHeadersMapping(Enum):
    """Enumeration of default headers mapping."""

    TENANT_IDENTIFIER = "Tenant-Identifier"
    AUTHORIZATION = "Authorization"
    MICROSERVICE_TOKEN = "X-Microservice-Token"
    MICROSERVICE_REQUEST_KEY = "X-Microservice-Request-Key"
    MICROSERVICE_REQUEST_ID = "X-Microservice-Request-Id"
