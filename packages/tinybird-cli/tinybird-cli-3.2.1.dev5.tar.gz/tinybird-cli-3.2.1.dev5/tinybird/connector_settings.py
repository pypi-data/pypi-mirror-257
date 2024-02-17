from __future__ import annotations

import logging
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel

from tinybird.data_connectors.credentials import (
    GCSConnectorCredentials,
    S3ConnectorCredentials,
    S3IAMRoleConnectorCredentials,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DataConnectorType(str, Enum):
    KAFKA = "kafka"
    GCLOUD_SCHEDULER = "gcscheduler"
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    GCLOUD_STORAGE = "gcs"
    GCLOUD_STORAGE_HMAC = "gcs_hmac"
    AMAZON_S3 = "s3"
    AMAZON_S3_IAMROLE = "s3_iamrole"

    def __str__(self) -> str:
        return self.value


DataConnectors = DataConnectorType  # this is just to make picking happy


class DataConnectorSetting(BaseModel):
    def get_region(self) -> str:
        return "unknown"

    def get_provider_name(self) -> str:
        return "unknown"


class KafkaConnectorSetting(DataConnectorSetting):
    kafka_bootstrap_servers: str
    kafka_sasl_plain_username: str
    kafka_sasl_plain_password: str
    cli_version: Optional[str] = None
    tb_endpoint: Optional[str] = None
    kafka_security_protocol: Optional[str] = None
    kafka_sasl_mechanism: Optional[str] = None
    kafka_schema_registry_url: Optional[str] = None


class S3ConnectorSetting(DataConnectorSetting):
    s3_access_key_id: str
    s3_secret_access_key: str
    s3_region: str
    endpoint_url: Optional[str] = None

    @property
    def credentials(self) -> S3ConnectorCredentials:
        return S3ConnectorCredentials(
            access_key_id=self.s3_access_key_id,
            secret_access_key=self.s3_secret_access_key,
            region=self.s3_region,
        )

    def get_provider_name(self) -> str:
        return DataConnectorType.AMAZON_S3

    def get_region(self) -> str:
        return self.s3_region


class S3IAMConnectorSetting(DataConnectorSetting):
    s3_iamrole_arn: str
    s3_iamrole_region: str
    s3_iamrole_external_id: str
    endpoint_url: Optional[str] = None

    @property
    def credentials(self) -> S3IAMRoleConnectorCredentials:
        return S3IAMRoleConnectorCredentials(
            role_arn=self.s3_iamrole_arn,
            external_id=self.s3_iamrole_external_id,
            region=self.s3_iamrole_region,
        )

    def get_provider_name(self) -> str:
        return DataConnectorType.AMAZON_S3

    def get_region(self) -> str:
        return self.s3_iamrole_region


class SnowflakeConnectorSetting(DataConnectorSetting):
    account: str
    username: str
    password: str
    role: str
    warehouse: str
    warehouse_size: Optional[str] = None
    stage: Optional[str] = None
    integration: Optional[str] = None


class GCSchedulerConnectorSetting(DataConnectorSetting):
    gcscheduler_region: Optional[str] = None


class BigQueryConnectorSetting(DataConnectorSetting):
    account: Optional[str] = None


class GCSHmacConnectorSetting(DataConnectorSetting):
    gcs_hmac_access_id: str
    gcs_hmac_secret: str
    endpoint_url: Optional[str] = None

    @property
    def credentials(self) -> GCSConnectorCredentials:
        return GCSConnectorCredentials(
            access_key_id=self.gcs_hmac_access_id,
            secret_access_key=self.gcs_hmac_secret,
        )

    def get_provider_name(self) -> str:
        return DataConnectorType.GCLOUD_STORAGE


class GCSConnectorSetting(DataConnectorSetting):
    gcs_private_key_id: str
    gcs_client_x509_cert_url: str
    gcs_project_id: str
    gcs_client_id: str
    gcs_client_email: str
    gcs_private_key: str


DATA_CONNECTOR_SETTINGS: dict[DataConnectors, type[DataConnectorSetting]] = {
    DataConnectors.KAFKA: KafkaConnectorSetting,
    DataConnectors.GCLOUD_SCHEDULER: GCSchedulerConnectorSetting,
    DataConnectors.SNOWFLAKE: SnowflakeConnectorSetting,
    DataConnectors.BIGQUERY: BigQueryConnectorSetting,
    DataConnectors.GCLOUD_STORAGE: GCSConnectorSetting,
    DataConnectors.GCLOUD_STORAGE_HMAC: GCSHmacConnectorSetting,
    DataConnectors.AMAZON_S3: S3ConnectorSetting,
    DataConnectors.AMAZON_S3_IAMROLE: S3IAMConnectorSetting,
}

SinkConnectorSettings = Union[S3ConnectorSetting, S3IAMConnectorSetting, GCSHmacConnectorSetting]


class DataLinkerSettings:
    kafka = [
        "tb_datasource",
        "tb_token",
        "kafka_topic",
        "kafka_group_id",
        "kafka_auto_offset_reset",
        "kafka_store_raw_value",
        "kafka_store_headers",
    ]


class DataSinkSettings:
    gcscheduler = [
        "cron",
        "timezone",
        "status",
        "gcscheduler_target_url",
        "gcscheduler_job_name",
        "gcscheduler_region",
    ]
    gcs_hmac = [
        "bucket_path",
        "file_template",
        "partition_node",
        "format",
        "compression",
    ]
    s3 = [
        "bucket_path",
        "file_template",
        "partition_node",
        "format",
        "compression",
    ]
    s3_iamrole = [
        "bucket_path",
        "file_template",
        "partition_node",
        "format",
        "compression",
    ]


class DataSensitiveSettings:
    kafka = ["kafka_sasl_plain_password"]
    gcscheduler = [
        "gcscheduler_target_url",
        "gcscheduler_job_name",
        "gcscheduler_region",
    ]
    bigquery: List[str] = []
    snowflake: List[str] = []
    gcs_hmac: List[str] = ["gcs_hmac_secret"]
    s3: List[str] = ["s3_secret_access_key"]
    s3_iamrole: List[str] = ["s3_iamrole_arn"]


CLI_EXCLUDED_SETTINGS = {
    "gcs_hmac": ["endpoint_url"],
    "s3": ["endpoint_url"],
    "s3_iamrole": ["endpoint_url"],
}
