# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'PipelineBufferOptions',
    'PipelineEncryptionAtRestOptions',
    'PipelineLogPublishingOptions',
    'PipelineLogPublishingOptionsCloudWatchLogDestinationProperties',
    'PipelineTag',
    'PipelineVpcEndpoint',
    'PipelineVpcOptions',
]

@pulumi.output_type
class PipelineBufferOptions(dict):
    """
    Key-value pairs to configure buffering.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "persistentBufferEnabled":
            suggest = "persistent_buffer_enabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineBufferOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineBufferOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineBufferOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 persistent_buffer_enabled: bool):
        """
        Key-value pairs to configure buffering.
        :param bool persistent_buffer_enabled: Whether persistent buffering should be enabled.
        """
        pulumi.set(__self__, "persistent_buffer_enabled", persistent_buffer_enabled)

    @property
    @pulumi.getter(name="persistentBufferEnabled")
    def persistent_buffer_enabled(self) -> bool:
        """
        Whether persistent buffering should be enabled.
        """
        return pulumi.get(self, "persistent_buffer_enabled")


@pulumi.output_type
class PipelineEncryptionAtRestOptions(dict):
    """
    Key-value pairs to configure encryption at rest.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "kmsKeyArn":
            suggest = "kms_key_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineEncryptionAtRestOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineEncryptionAtRestOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineEncryptionAtRestOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 kms_key_arn: str):
        """
        Key-value pairs to configure encryption at rest.
        :param str kms_key_arn: The KMS key to use for encrypting data. By default an AWS owned key is used
        """
        pulumi.set(__self__, "kms_key_arn", kms_key_arn)

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> str:
        """
        The KMS key to use for encrypting data. By default an AWS owned key is used
        """
        return pulumi.get(self, "kms_key_arn")


@pulumi.output_type
class PipelineLogPublishingOptions(dict):
    """
    Key-value pairs to configure log publishing.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cloudWatchLogDestination":
            suggest = "cloud_watch_log_destination"
        elif key == "isLoggingEnabled":
            suggest = "is_logging_enabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineLogPublishingOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineLogPublishingOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineLogPublishingOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cloud_watch_log_destination: Optional['outputs.PipelineLogPublishingOptionsCloudWatchLogDestinationProperties'] = None,
                 is_logging_enabled: Optional[bool] = None):
        """
        Key-value pairs to configure log publishing.
        :param 'PipelineLogPublishingOptionsCloudWatchLogDestinationProperties' cloud_watch_log_destination: The destination for OpenSearch Ingestion Service logs sent to Amazon CloudWatch.
        :param bool is_logging_enabled: Whether logs should be published.
        """
        if cloud_watch_log_destination is not None:
            pulumi.set(__self__, "cloud_watch_log_destination", cloud_watch_log_destination)
        if is_logging_enabled is not None:
            pulumi.set(__self__, "is_logging_enabled", is_logging_enabled)

    @property
    @pulumi.getter(name="cloudWatchLogDestination")
    def cloud_watch_log_destination(self) -> Optional['outputs.PipelineLogPublishingOptionsCloudWatchLogDestinationProperties']:
        """
        The destination for OpenSearch Ingestion Service logs sent to Amazon CloudWatch.
        """
        return pulumi.get(self, "cloud_watch_log_destination")

    @property
    @pulumi.getter(name="isLoggingEnabled")
    def is_logging_enabled(self) -> Optional[bool]:
        """
        Whether logs should be published.
        """
        return pulumi.get(self, "is_logging_enabled")


@pulumi.output_type
class PipelineLogPublishingOptionsCloudWatchLogDestinationProperties(dict):
    """
    The destination for OpenSearch Ingestion Service logs sent to Amazon CloudWatch.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroup":
            suggest = "log_group"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineLogPublishingOptionsCloudWatchLogDestinationProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineLogPublishingOptionsCloudWatchLogDestinationProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineLogPublishingOptionsCloudWatchLogDestinationProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_group: str):
        """
        The destination for OpenSearch Ingestion Service logs sent to Amazon CloudWatch.
        """
        pulumi.set(__self__, "log_group", log_group)

    @property
    @pulumi.getter(name="logGroup")
    def log_group(self) -> str:
        return pulumi.get(self, "log_group")


@pulumi.output_type
class PipelineTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param str value: The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class PipelineVpcEndpoint(dict):
    """
    An OpenSearch Ingestion Service-managed VPC endpoint that will access one or more pipelines.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "vpcEndpointId":
            suggest = "vpc_endpoint_id"
        elif key == "vpcId":
            suggest = "vpc_id"
        elif key == "vpcOptions":
            suggest = "vpc_options"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineVpcEndpoint. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineVpcEndpoint.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineVpcEndpoint.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 vpc_endpoint_id: Optional[str] = None,
                 vpc_id: Optional[str] = None,
                 vpc_options: Optional['outputs.PipelineVpcOptions'] = None):
        """
        An OpenSearch Ingestion Service-managed VPC endpoint that will access one or more pipelines.
        :param str vpc_endpoint_id: The unique identifier of the endpoint.
        :param str vpc_id: The ID for your VPC. AWS Privatelink generates this value when you create a VPC.
        """
        if vpc_endpoint_id is not None:
            pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)
        if vpc_options is not None:
            pulumi.set(__self__, "vpc_options", vpc_options)

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> Optional[str]:
        """
        The unique identifier of the endpoint.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        The ID for your VPC. AWS Privatelink generates this value when you create a VPC.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vpcOptions")
    def vpc_options(self) -> Optional['outputs.PipelineVpcOptions']:
        return pulumi.get(self, "vpc_options")


@pulumi.output_type
class PipelineVpcOptions(dict):
    """
    Container for the values required to configure VPC access for the pipeline. If you don't specify these values, OpenSearch Ingestion Service creates the pipeline with a public endpoint.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "subnetIds":
            suggest = "subnet_ids"
        elif key == "securityGroupIds":
            suggest = "security_group_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineVpcOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineVpcOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineVpcOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 subnet_ids: Sequence[str],
                 security_group_ids: Optional[Sequence[str]] = None):
        """
        Container for the values required to configure VPC access for the pipeline. If you don't specify these values, OpenSearch Ingestion Service creates the pipeline with a public endpoint.
        :param Sequence[str] subnet_ids: A list of subnet IDs associated with the VPC endpoint.
        :param Sequence[str] security_group_ids: A list of security groups associated with the VPC endpoint.
        """
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        """
        A list of subnet IDs associated with the VPC endpoint.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[str]]:
        """
        A list of security groups associated with the VPC endpoint.
        """
        return pulumi.get(self, "security_group_ids")


