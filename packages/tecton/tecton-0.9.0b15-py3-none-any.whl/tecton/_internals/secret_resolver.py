from typing import Dict
from typing import List

from tecton._internals import metadata_service
from tecton_core.secrets import SecretCacheKey
from tecton_core.secrets import SecretContext
from tecton_core.secrets import SecretResolver
from tecton_proto.common.secret_pb2 import SecretReference
from tecton_proto.secrets.secrets_service_pb2 import GetSecretValueRequest


# Singleton local secret store for Notebook development
_local_secret_store: Dict[SecretCacheKey, str] = {}


def set_local_secret(scope: str, key: str, value: str) -> None:
    """Set the secret in Local Secret Store singleton instance."""
    _local_secret_store[SecretCacheKey(scope, key)] = value


class LocalDevSecretResolver(SecretResolver):
    """Secret Resolver for local development. Secrets are retrieved from Secret Service or locally specified values."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def resolve(self, secrets: List[SecretReference]) -> SecretContext:
        resolved_secrets_dict = {}
        for secret in secrets:
            context_key = SecretCacheKey(secret.scope, secret.key)
            if secret.is_local:
                resolved_secrets_dict[context_key] = self._fetch_local_secret(secret.scope, secret.key)
            else:
                resolved_secrets_dict[context_key] = self._fetch_mds_secret(secret.scope, secret.key)
        return SecretContext(resolved_secrets_dict)

    @staticmethod
    def _fetch_mds_secret(scope: str, key: str) -> str:
        request = GetSecretValueRequest(scope=scope, key=key)
        response = metadata_service.instance().GetSecretValue(request)
        return response.secret_value.value

    @staticmethod
    def _fetch_local_secret(scope: str, key: str) -> str:
        return _local_secret_store[SecretCacheKey(scope, key)]
