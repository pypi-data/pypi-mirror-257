import abc
import dataclasses


class ConnectorCredentials(abc.ABC):
    pass


@dataclasses.dataclass(frozen=True)
class S3ConnectorCredentials(ConnectorCredentials):
    access_key_id: str
    secret_access_key: str
    region: str


@dataclasses.dataclass(frozen=True)
class S3IAMRoleConnectorCredentials(ConnectorCredentials):
    role_arn: str
    external_id: str
    region: str


@dataclasses.dataclass(frozen=True)
class GCSConnectorCredentials(ConnectorCredentials):
    access_key_id: str
    secret_access_key: str
