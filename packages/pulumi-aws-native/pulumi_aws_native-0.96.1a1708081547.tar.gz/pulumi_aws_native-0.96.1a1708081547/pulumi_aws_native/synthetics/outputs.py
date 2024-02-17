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
    'CanaryArtifactConfig',
    'CanaryBaseScreenshot',
    'CanaryCode',
    'CanaryRunConfig',
    'CanaryS3Encryption',
    'CanarySchedule',
    'CanaryTag',
    'CanaryVisualReference',
    'CanaryVpcConfig',
    'GroupTag',
]

@pulumi.output_type
class CanaryArtifactConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "s3Encryption":
            suggest = "s3_encryption"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CanaryArtifactConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CanaryArtifactConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CanaryArtifactConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 s3_encryption: Optional['outputs.CanaryS3Encryption'] = None):
        """
        :param 'CanaryS3Encryption' s3_encryption: Encryption configuration for uploading artifacts to S3
        """
        if s3_encryption is not None:
            pulumi.set(__self__, "s3_encryption", s3_encryption)

    @property
    @pulumi.getter(name="s3Encryption")
    def s3_encryption(self) -> Optional['outputs.CanaryS3Encryption']:
        """
        Encryption configuration for uploading artifacts to S3
        """
        return pulumi.get(self, "s3_encryption")


@pulumi.output_type
class CanaryBaseScreenshot(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "screenshotName":
            suggest = "screenshot_name"
        elif key == "ignoreCoordinates":
            suggest = "ignore_coordinates"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CanaryBaseScreenshot. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CanaryBaseScreenshot.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CanaryBaseScreenshot.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 screenshot_name: str,
                 ignore_coordinates: Optional[Sequence[str]] = None):
        """
        :param str screenshot_name: Name of the screenshot to be used as base reference for visual testing
        :param Sequence[str] ignore_coordinates: List of coordinates of rectangles to be ignored during visual testing
        """
        pulumi.set(__self__, "screenshot_name", screenshot_name)
        if ignore_coordinates is not None:
            pulumi.set(__self__, "ignore_coordinates", ignore_coordinates)

    @property
    @pulumi.getter(name="screenshotName")
    def screenshot_name(self) -> str:
        """
        Name of the screenshot to be used as base reference for visual testing
        """
        return pulumi.get(self, "screenshot_name")

    @property
    @pulumi.getter(name="ignoreCoordinates")
    def ignore_coordinates(self) -> Optional[Sequence[str]]:
        """
        List of coordinates of rectangles to be ignored during visual testing
        """
        return pulumi.get(self, "ignore_coordinates")


@pulumi.output_type
class CanaryCode(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "s3Bucket":
            suggest = "s3_bucket"
        elif key == "s3Key":
            suggest = "s3_key"
        elif key == "s3ObjectVersion":
            suggest = "s3_object_version"
        elif key == "sourceLocationArn":
            suggest = "source_location_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CanaryCode. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CanaryCode.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CanaryCode.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 handler: str,
                 s3_bucket: Optional[str] = None,
                 s3_key: Optional[str] = None,
                 s3_object_version: Optional[str] = None,
                 script: Optional[str] = None,
                 source_location_arn: Optional[str] = None):
        pulumi.set(__self__, "handler", handler)
        if s3_bucket is not None:
            pulumi.set(__self__, "s3_bucket", s3_bucket)
        if s3_key is not None:
            pulumi.set(__self__, "s3_key", s3_key)
        if s3_object_version is not None:
            pulumi.set(__self__, "s3_object_version", s3_object_version)
        if script is not None:
            pulumi.set(__self__, "script", script)
        if source_location_arn is not None:
            pulumi.set(__self__, "source_location_arn", source_location_arn)

    @property
    @pulumi.getter
    def handler(self) -> str:
        return pulumi.get(self, "handler")

    @property
    @pulumi.getter(name="s3Bucket")
    def s3_bucket(self) -> Optional[str]:
        return pulumi.get(self, "s3_bucket")

    @property
    @pulumi.getter(name="s3Key")
    def s3_key(self) -> Optional[str]:
        return pulumi.get(self, "s3_key")

    @property
    @pulumi.getter(name="s3ObjectVersion")
    def s3_object_version(self) -> Optional[str]:
        return pulumi.get(self, "s3_object_version")

    @property
    @pulumi.getter
    def script(self) -> Optional[str]:
        return pulumi.get(self, "script")

    @property
    @pulumi.getter(name="sourceLocationArn")
    def source_location_arn(self) -> Optional[str]:
        return pulumi.get(self, "source_location_arn")


@pulumi.output_type
class CanaryRunConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "activeTracing":
            suggest = "active_tracing"
        elif key == "environmentVariables":
            suggest = "environment_variables"
        elif key == "memoryInMb":
            suggest = "memory_in_mb"
        elif key == "timeoutInSeconds":
            suggest = "timeout_in_seconds"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CanaryRunConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CanaryRunConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CanaryRunConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 active_tracing: Optional[bool] = None,
                 environment_variables: Optional[Mapping[str, str]] = None,
                 memory_in_mb: Optional[int] = None,
                 timeout_in_seconds: Optional[int] = None):
        """
        :param bool active_tracing: Enable active tracing if set to true
        :param Mapping[str, str] environment_variables: Environment variable key-value pairs.
        :param int memory_in_mb: Provide maximum memory available for canary in MB
        :param int timeout_in_seconds: Provide maximum canary timeout per run in seconds
        """
        if active_tracing is not None:
            pulumi.set(__self__, "active_tracing", active_tracing)
        if environment_variables is not None:
            pulumi.set(__self__, "environment_variables", environment_variables)
        if memory_in_mb is not None:
            pulumi.set(__self__, "memory_in_mb", memory_in_mb)
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)

    @property
    @pulumi.getter(name="activeTracing")
    def active_tracing(self) -> Optional[bool]:
        """
        Enable active tracing if set to true
        """
        return pulumi.get(self, "active_tracing")

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[Mapping[str, str]]:
        """
        Environment variable key-value pairs.
        """
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter(name="memoryInMb")
    def memory_in_mb(self) -> Optional[int]:
        """
        Provide maximum memory available for canary in MB
        """
        return pulumi.get(self, "memory_in_mb")

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[int]:
        """
        Provide maximum canary timeout per run in seconds
        """
        return pulumi.get(self, "timeout_in_seconds")


@pulumi.output_type
class CanaryS3Encryption(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "encryptionMode":
            suggest = "encryption_mode"
        elif key == "kmsKeyArn":
            suggest = "kms_key_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CanaryS3Encryption. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CanaryS3Encryption.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CanaryS3Encryption.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 encryption_mode: Optional[str] = None,
                 kms_key_arn: Optional[str] = None):
        """
        :param str encryption_mode: Encryption mode for encrypting artifacts when uploading to S3. Valid values: SSE_S3 and SSE_KMS.
        :param str kms_key_arn: KMS key Arn for encrypting artifacts when uploading to S3. You must specify KMS key Arn for SSE_KMS encryption mode only.
        """
        if encryption_mode is not None:
            pulumi.set(__self__, "encryption_mode", encryption_mode)
        if kms_key_arn is not None:
            pulumi.set(__self__, "kms_key_arn", kms_key_arn)

    @property
    @pulumi.getter(name="encryptionMode")
    def encryption_mode(self) -> Optional[str]:
        """
        Encryption mode for encrypting artifacts when uploading to S3. Valid values: SSE_S3 and SSE_KMS.
        """
        return pulumi.get(self, "encryption_mode")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[str]:
        """
        KMS key Arn for encrypting artifacts when uploading to S3. You must specify KMS key Arn for SSE_KMS encryption mode only.
        """
        return pulumi.get(self, "kms_key_arn")


@pulumi.output_type
class CanarySchedule(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "durationInSeconds":
            suggest = "duration_in_seconds"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CanarySchedule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CanarySchedule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CanarySchedule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 expression: str,
                 duration_in_seconds: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        if duration_in_seconds is not None:
            pulumi.set(__self__, "duration_in_seconds", duration_in_seconds)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter(name="durationInSeconds")
    def duration_in_seconds(self) -> Optional[str]:
        return pulumi.get(self, "duration_in_seconds")


@pulumi.output_type
class CanaryTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        :param str value: The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class CanaryVisualReference(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "baseCanaryRunId":
            suggest = "base_canary_run_id"
        elif key == "baseScreenshots":
            suggest = "base_screenshots"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CanaryVisualReference. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CanaryVisualReference.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CanaryVisualReference.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 base_canary_run_id: str,
                 base_screenshots: Optional[Sequence['outputs.CanaryBaseScreenshot']] = None):
        """
        :param str base_canary_run_id: Canary run id to be used as base reference for visual testing
        :param Sequence['CanaryBaseScreenshot'] base_screenshots: List of screenshots used as base reference for visual testing
        """
        pulumi.set(__self__, "base_canary_run_id", base_canary_run_id)
        if base_screenshots is not None:
            pulumi.set(__self__, "base_screenshots", base_screenshots)

    @property
    @pulumi.getter(name="baseCanaryRunId")
    def base_canary_run_id(self) -> str:
        """
        Canary run id to be used as base reference for visual testing
        """
        return pulumi.get(self, "base_canary_run_id")

    @property
    @pulumi.getter(name="baseScreenshots")
    def base_screenshots(self) -> Optional[Sequence['outputs.CanaryBaseScreenshot']]:
        """
        List of screenshots used as base reference for visual testing
        """
        return pulumi.get(self, "base_screenshots")


@pulumi.output_type
class CanaryVpcConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "securityGroupIds":
            suggest = "security_group_ids"
        elif key == "subnetIds":
            suggest = "subnet_ids"
        elif key == "vpcId":
            suggest = "vpc_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CanaryVpcConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CanaryVpcConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CanaryVpcConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 security_group_ids: Sequence[str],
                 subnet_ids: Sequence[str],
                 vpc_id: Optional[str] = None):
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        return pulumi.get(self, "vpc_id")


@pulumi.output_type
class GroupTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        :param str value: The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        """
        return pulumi.get(self, "value")


