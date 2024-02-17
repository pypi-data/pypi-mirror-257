# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'DeliveryStreamAmazonOpenSearchServerlessDestinationConfigurationS3BackupMode',
    'DeliveryStreamAmazonopensearchserviceDestinationConfigurationIndexRotationPeriod',
    'DeliveryStreamAmazonopensearchserviceDestinationConfigurationS3BackupMode',
    'DeliveryStreamAuthenticationConfigurationConnectivity',
    'DeliveryStreamDocumentIdOptionsDefaultDocumentIdFormat',
    'DeliveryStreamElasticsearchDestinationConfigurationIndexRotationPeriod',
    'DeliveryStreamElasticsearchDestinationConfigurationS3BackupMode',
    'DeliveryStreamEncryptionConfigurationInputKeyType',
    'DeliveryStreamEncryptionConfigurationNoEncryptionConfig',
    'DeliveryStreamExtendedS3DestinationConfigurationCompressionFormat',
    'DeliveryStreamExtendedS3DestinationConfigurationS3BackupMode',
    'DeliveryStreamHttpEndpointRequestConfigurationContentEncoding',
    'DeliveryStreamProcessorType',
    'DeliveryStreamRedshiftDestinationConfigurationS3BackupMode',
    'DeliveryStreamS3DestinationConfigurationCompressionFormat',
    'DeliveryStreamSnowflakeDestinationConfigurationDataLoadingOption',
    'DeliveryStreamSnowflakeDestinationConfigurationS3BackupMode',
    'DeliveryStreamSplunkDestinationConfigurationHecEndpointType',
    'DeliveryStreamType',
]


class DeliveryStreamAmazonOpenSearchServerlessDestinationConfigurationS3BackupMode(str, Enum):
    FAILED_DOCUMENTS_ONLY = "FailedDocumentsOnly"
    ALL_DOCUMENTS = "AllDocuments"


class DeliveryStreamAmazonopensearchserviceDestinationConfigurationIndexRotationPeriod(str, Enum):
    NO_ROTATION = "NoRotation"
    ONE_HOUR = "OneHour"
    ONE_DAY = "OneDay"
    ONE_WEEK = "OneWeek"
    ONE_MONTH = "OneMonth"


class DeliveryStreamAmazonopensearchserviceDestinationConfigurationS3BackupMode(str, Enum):
    FAILED_DOCUMENTS_ONLY = "FailedDocumentsOnly"
    ALL_DOCUMENTS = "AllDocuments"


class DeliveryStreamAuthenticationConfigurationConnectivity(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class DeliveryStreamDocumentIdOptionsDefaultDocumentIdFormat(str, Enum):
    FIREHOSE_DEFAULT = "FIREHOSE_DEFAULT"
    NO_DOCUMENT_ID = "NO_DOCUMENT_ID"


class DeliveryStreamElasticsearchDestinationConfigurationIndexRotationPeriod(str, Enum):
    NO_ROTATION = "NoRotation"
    ONE_HOUR = "OneHour"
    ONE_DAY = "OneDay"
    ONE_WEEK = "OneWeek"
    ONE_MONTH = "OneMonth"


class DeliveryStreamElasticsearchDestinationConfigurationS3BackupMode(str, Enum):
    FAILED_DOCUMENTS_ONLY = "FailedDocumentsOnly"
    ALL_DOCUMENTS = "AllDocuments"


class DeliveryStreamEncryptionConfigurationInputKeyType(str, Enum):
    AWS_OWNED_CMK = "AWS_OWNED_CMK"
    CUSTOMER_MANAGED_CMK = "CUSTOMER_MANAGED_CMK"


class DeliveryStreamEncryptionConfigurationNoEncryptionConfig(str, Enum):
    NO_ENCRYPTION = "NoEncryption"


class DeliveryStreamExtendedS3DestinationConfigurationCompressionFormat(str, Enum):
    UNCOMPRESSED = "UNCOMPRESSED"
    GZIP = "GZIP"
    ZIP = "ZIP"
    SNAPPY = "Snappy"
    HADOOP_SNAPPY = "HADOOP_SNAPPY"


class DeliveryStreamExtendedS3DestinationConfigurationS3BackupMode(str, Enum):
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class DeliveryStreamHttpEndpointRequestConfigurationContentEncoding(str, Enum):
    NONE = "NONE"
    GZIP = "GZIP"


class DeliveryStreamProcessorType(str, Enum):
    RECORD_DE_AGGREGATION = "RecordDeAggregation"
    DECOMPRESSION = "Decompression"
    LAMBDA_ = "Lambda"
    METADATA_EXTRACTION = "MetadataExtraction"
    APPEND_DELIMITER_TO_RECORD = "AppendDelimiterToRecord"


class DeliveryStreamRedshiftDestinationConfigurationS3BackupMode(str, Enum):
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class DeliveryStreamS3DestinationConfigurationCompressionFormat(str, Enum):
    UNCOMPRESSED = "UNCOMPRESSED"
    GZIP = "GZIP"
    ZIP = "ZIP"
    SNAPPY = "Snappy"
    HADOOP_SNAPPY = "HADOOP_SNAPPY"


class DeliveryStreamSnowflakeDestinationConfigurationDataLoadingOption(str, Enum):
    JSON_MAPPING = "JSON_MAPPING"
    VARIANT_CONTENT_MAPPING = "VARIANT_CONTENT_MAPPING"
    VARIANT_CONTENT_AND_METADATA_MAPPING = "VARIANT_CONTENT_AND_METADATA_MAPPING"


class DeliveryStreamSnowflakeDestinationConfigurationS3BackupMode(str, Enum):
    FAILED_DATA_ONLY = "FailedDataOnly"
    ALL_DATA = "AllData"


class DeliveryStreamSplunkDestinationConfigurationHecEndpointType(str, Enum):
    RAW = "Raw"
    EVENT = "Event"


class DeliveryStreamType(str, Enum):
    DIRECT_PUT = "DirectPut"
    KINESIS_STREAM_AS_SOURCE = "KinesisStreamAsSource"
    MSKAS_SOURCE = "MSKAsSource"
