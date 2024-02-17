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
    'AssistantAssociationAssociationData',
    'AssistantAssociationTag',
    'AssistantServerSideEncryptionConfiguration',
    'AssistantTag',
    'KnowledgeBaseAppIntegrationsConfiguration',
    'KnowledgeBaseRenderingConfiguration',
    'KnowledgeBaseServerSideEncryptionConfiguration',
    'KnowledgeBaseSourceConfiguration',
    'KnowledgeBaseTag',
]

@pulumi.output_type
class AssistantAssociationAssociationData(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "knowledgeBaseId":
            suggest = "knowledge_base_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssistantAssociationAssociationData. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssistantAssociationAssociationData.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssistantAssociationAssociationData.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 knowledge_base_id: str):
        pulumi.set(__self__, "knowledge_base_id", knowledge_base_id)

    @property
    @pulumi.getter(name="knowledgeBaseId")
    def knowledge_base_id(self) -> str:
        return pulumi.get(self, "knowledge_base_id")


@pulumi.output_type
class AssistantAssociationTag(dict):
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
class AssistantServerSideEncryptionConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "kmsKeyId":
            suggest = "kms_key_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssistantServerSideEncryptionConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssistantServerSideEncryptionConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssistantServerSideEncryptionConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 kms_key_id: Optional[str] = None):
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[str]:
        return pulumi.get(self, "kms_key_id")


@pulumi.output_type
class AssistantTag(dict):
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
class KnowledgeBaseAppIntegrationsConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "appIntegrationArn":
            suggest = "app_integration_arn"
        elif key == "objectFields":
            suggest = "object_fields"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KnowledgeBaseAppIntegrationsConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KnowledgeBaseAppIntegrationsConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KnowledgeBaseAppIntegrationsConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 app_integration_arn: str,
                 object_fields: Optional[Sequence[str]] = None):
        pulumi.set(__self__, "app_integration_arn", app_integration_arn)
        if object_fields is not None:
            pulumi.set(__self__, "object_fields", object_fields)

    @property
    @pulumi.getter(name="appIntegrationArn")
    def app_integration_arn(self) -> str:
        return pulumi.get(self, "app_integration_arn")

    @property
    @pulumi.getter(name="objectFields")
    def object_fields(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "object_fields")


@pulumi.output_type
class KnowledgeBaseRenderingConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "templateUri":
            suggest = "template_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KnowledgeBaseRenderingConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KnowledgeBaseRenderingConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KnowledgeBaseRenderingConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 template_uri: Optional[str] = None):
        if template_uri is not None:
            pulumi.set(__self__, "template_uri", template_uri)

    @property
    @pulumi.getter(name="templateUri")
    def template_uri(self) -> Optional[str]:
        return pulumi.get(self, "template_uri")


@pulumi.output_type
class KnowledgeBaseServerSideEncryptionConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "kmsKeyId":
            suggest = "kms_key_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KnowledgeBaseServerSideEncryptionConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KnowledgeBaseServerSideEncryptionConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KnowledgeBaseServerSideEncryptionConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 kms_key_id: Optional[str] = None):
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[str]:
        return pulumi.get(self, "kms_key_id")


@pulumi.output_type
class KnowledgeBaseSourceConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "appIntegrations":
            suggest = "app_integrations"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KnowledgeBaseSourceConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KnowledgeBaseSourceConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KnowledgeBaseSourceConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 app_integrations: Optional['outputs.KnowledgeBaseAppIntegrationsConfiguration'] = None):
        if app_integrations is not None:
            pulumi.set(__self__, "app_integrations", app_integrations)

    @property
    @pulumi.getter(name="appIntegrations")
    def app_integrations(self) -> Optional['outputs.KnowledgeBaseAppIntegrationsConfiguration']:
        return pulumi.get(self, "app_integrations")


@pulumi.output_type
class KnowledgeBaseTag(dict):
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


