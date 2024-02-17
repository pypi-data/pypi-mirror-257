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
from ._enums import *

__all__ = [
    'CapabilityConfigurationProperties',
    'CapabilityEdiConfiguration',
    'CapabilityEdiTypeProperties',
    'CapabilityS3Location',
    'CapabilityTag',
    'CapabilityX12Details',
    'PartnershipTag',
    'ProfileTag',
    'TransformerEdiTypeProperties',
    'TransformerTag',
    'TransformerX12Details',
]

@pulumi.output_type
class CapabilityConfigurationProperties(dict):
    def __init__(__self__, *,
                 edi: 'outputs.CapabilityEdiConfiguration'):
        pulumi.set(__self__, "edi", edi)

    @property
    @pulumi.getter
    def edi(self) -> 'outputs.CapabilityEdiConfiguration':
        return pulumi.get(self, "edi")


@pulumi.output_type
class CapabilityEdiConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "inputLocation":
            suggest = "input_location"
        elif key == "outputLocation":
            suggest = "output_location"
        elif key == "transformerId":
            suggest = "transformer_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CapabilityEdiConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CapabilityEdiConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CapabilityEdiConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 input_location: 'outputs.CapabilityS3Location',
                 output_location: 'outputs.CapabilityS3Location',
                 transformer_id: str,
                 type: 'outputs.CapabilityEdiTypeProperties'):
        pulumi.set(__self__, "input_location", input_location)
        pulumi.set(__self__, "output_location", output_location)
        pulumi.set(__self__, "transformer_id", transformer_id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="inputLocation")
    def input_location(self) -> 'outputs.CapabilityS3Location':
        return pulumi.get(self, "input_location")

    @property
    @pulumi.getter(name="outputLocation")
    def output_location(self) -> 'outputs.CapabilityS3Location':
        return pulumi.get(self, "output_location")

    @property
    @pulumi.getter(name="transformerId")
    def transformer_id(self) -> str:
        return pulumi.get(self, "transformer_id")

    @property
    @pulumi.getter
    def type(self) -> 'outputs.CapabilityEdiTypeProperties':
        return pulumi.get(self, "type")


@pulumi.output_type
class CapabilityEdiTypeProperties(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "x12Details":
            suggest = "x12_details"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CapabilityEdiTypeProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CapabilityEdiTypeProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CapabilityEdiTypeProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 x12_details: 'outputs.CapabilityX12Details'):
        pulumi.set(__self__, "x12_details", x12_details)

    @property
    @pulumi.getter(name="x12Details")
    def x12_details(self) -> 'outputs.CapabilityX12Details':
        return pulumi.get(self, "x12_details")


@pulumi.output_type
class CapabilityS3Location(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CapabilityS3Location. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CapabilityS3Location.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CapabilityS3Location.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_name: Optional[str] = None,
                 key: Optional[str] = None):
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if key is not None:
            pulumi.set(__self__, "key", key)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[str]:
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        return pulumi.get(self, "key")


@pulumi.output_type
class CapabilityTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class CapabilityX12Details(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "transactionSet":
            suggest = "transaction_set"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CapabilityX12Details. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CapabilityX12Details.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CapabilityX12Details.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 transaction_set: Optional['CapabilityX12TransactionSet'] = None,
                 version: Optional['CapabilityX12Version'] = None):
        if transaction_set is not None:
            pulumi.set(__self__, "transaction_set", transaction_set)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="transactionSet")
    def transaction_set(self) -> Optional['CapabilityX12TransactionSet']:
        return pulumi.get(self, "transaction_set")

    @property
    @pulumi.getter
    def version(self) -> Optional['CapabilityX12Version']:
        return pulumi.get(self, "version")


@pulumi.output_type
class PartnershipTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class ProfileTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class TransformerEdiTypeProperties(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "x12Details":
            suggest = "x12_details"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TransformerEdiTypeProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TransformerEdiTypeProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TransformerEdiTypeProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 x12_details: 'outputs.TransformerX12Details'):
        pulumi.set(__self__, "x12_details", x12_details)

    @property
    @pulumi.getter(name="x12Details")
    def x12_details(self) -> 'outputs.TransformerX12Details':
        return pulumi.get(self, "x12_details")


@pulumi.output_type
class TransformerTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class TransformerX12Details(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "transactionSet":
            suggest = "transaction_set"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TransformerX12Details. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TransformerX12Details.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TransformerX12Details.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 transaction_set: Optional['TransformerX12TransactionSet'] = None,
                 version: Optional['TransformerX12Version'] = None):
        if transaction_set is not None:
            pulumi.set(__self__, "transaction_set", transaction_set)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="transactionSet")
    def transaction_set(self) -> Optional['TransformerX12TransactionSet']:
        return pulumi.get(self, "transaction_set")

    @property
    @pulumi.getter
    def version(self) -> Optional['TransformerX12Version']:
        return pulumi.get(self, "version")


