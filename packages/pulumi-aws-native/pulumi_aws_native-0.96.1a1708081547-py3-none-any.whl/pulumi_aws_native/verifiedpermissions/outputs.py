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
    'IdentitySourceCognitoUserPoolConfiguration',
    'IdentitySourceConfiguration',
    'IdentitySourceDetails',
    'PolicyDefinition0Properties',
    'PolicyDefinition1Properties',
    'PolicyEntityIdentifier',
    'PolicyStaticPolicyDefinition',
    'PolicyStoreSchemaDefinition',
    'PolicyStoreValidationSettings',
    'PolicyTemplateLinkedPolicyDefinition',
]

@pulumi.output_type
class IdentitySourceCognitoUserPoolConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "userPoolArn":
            suggest = "user_pool_arn"
        elif key == "clientIds":
            suggest = "client_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentitySourceCognitoUserPoolConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentitySourceCognitoUserPoolConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentitySourceCognitoUserPoolConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 user_pool_arn: str,
                 client_ids: Optional[Sequence[str]] = None):
        pulumi.set(__self__, "user_pool_arn", user_pool_arn)
        if client_ids is not None:
            pulumi.set(__self__, "client_ids", client_ids)

    @property
    @pulumi.getter(name="userPoolArn")
    def user_pool_arn(self) -> str:
        return pulumi.get(self, "user_pool_arn")

    @property
    @pulumi.getter(name="clientIds")
    def client_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "client_ids")


@pulumi.output_type
class IdentitySourceConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cognitoUserPoolConfiguration":
            suggest = "cognito_user_pool_configuration"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentitySourceConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentitySourceConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentitySourceConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cognito_user_pool_configuration: 'outputs.IdentitySourceCognitoUserPoolConfiguration'):
        pulumi.set(__self__, "cognito_user_pool_configuration", cognito_user_pool_configuration)

    @property
    @pulumi.getter(name="cognitoUserPoolConfiguration")
    def cognito_user_pool_configuration(self) -> 'outputs.IdentitySourceCognitoUserPoolConfiguration':
        return pulumi.get(self, "cognito_user_pool_configuration")


@pulumi.output_type
class IdentitySourceDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientIds":
            suggest = "client_ids"
        elif key == "discoveryUrl":
            suggest = "discovery_url"
        elif key == "openIdIssuer":
            suggest = "open_id_issuer"
        elif key == "userPoolArn":
            suggest = "user_pool_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentitySourceDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentitySourceDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentitySourceDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_ids: Optional[Sequence[str]] = None,
                 discovery_url: Optional[str] = None,
                 open_id_issuer: Optional['IdentitySourceOpenIdIssuer'] = None,
                 user_pool_arn: Optional[str] = None):
        if client_ids is not None:
            pulumi.set(__self__, "client_ids", client_ids)
        if discovery_url is not None:
            pulumi.set(__self__, "discovery_url", discovery_url)
        if open_id_issuer is not None:
            pulumi.set(__self__, "open_id_issuer", open_id_issuer)
        if user_pool_arn is not None:
            pulumi.set(__self__, "user_pool_arn", user_pool_arn)

    @property
    @pulumi.getter(name="clientIds")
    def client_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "client_ids")

    @property
    @pulumi.getter(name="discoveryUrl")
    def discovery_url(self) -> Optional[str]:
        return pulumi.get(self, "discovery_url")

    @property
    @pulumi.getter(name="openIdIssuer")
    def open_id_issuer(self) -> Optional['IdentitySourceOpenIdIssuer']:
        return pulumi.get(self, "open_id_issuer")

    @property
    @pulumi.getter(name="userPoolArn")
    def user_pool_arn(self) -> Optional[str]:
        return pulumi.get(self, "user_pool_arn")


@pulumi.output_type
class PolicyDefinition0Properties(dict):
    def __init__(__self__, *,
                 static: 'outputs.PolicyStaticPolicyDefinition'):
        pulumi.set(__self__, "static", static)

    @property
    @pulumi.getter
    def static(self) -> 'outputs.PolicyStaticPolicyDefinition':
        return pulumi.get(self, "static")


@pulumi.output_type
class PolicyDefinition1Properties(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "templateLinked":
            suggest = "template_linked"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyDefinition1Properties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyDefinition1Properties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyDefinition1Properties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 template_linked: 'outputs.PolicyTemplateLinkedPolicyDefinition'):
        pulumi.set(__self__, "template_linked", template_linked)

    @property
    @pulumi.getter(name="templateLinked")
    def template_linked(self) -> 'outputs.PolicyTemplateLinkedPolicyDefinition':
        return pulumi.get(self, "template_linked")


@pulumi.output_type
class PolicyEntityIdentifier(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "entityId":
            suggest = "entity_id"
        elif key == "entityType":
            suggest = "entity_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyEntityIdentifier. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyEntityIdentifier.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyEntityIdentifier.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 entity_id: str,
                 entity_type: str):
        pulumi.set(__self__, "entity_id", entity_id)
        pulumi.set(__self__, "entity_type", entity_type)

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> str:
        return pulumi.get(self, "entity_id")

    @property
    @pulumi.getter(name="entityType")
    def entity_type(self) -> str:
        return pulumi.get(self, "entity_type")


@pulumi.output_type
class PolicyStaticPolicyDefinition(dict):
    def __init__(__self__, *,
                 statement: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "statement", statement)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def statement(self) -> str:
        return pulumi.get(self, "statement")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class PolicyStoreSchemaDefinition(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cedarJson":
            suggest = "cedar_json"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyStoreSchemaDefinition. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyStoreSchemaDefinition.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyStoreSchemaDefinition.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cedar_json: Optional[str] = None):
        if cedar_json is not None:
            pulumi.set(__self__, "cedar_json", cedar_json)

    @property
    @pulumi.getter(name="cedarJson")
    def cedar_json(self) -> Optional[str]:
        return pulumi.get(self, "cedar_json")


@pulumi.output_type
class PolicyStoreValidationSettings(dict):
    def __init__(__self__, *,
                 mode: 'PolicyStoreValidationMode'):
        pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter
    def mode(self) -> 'PolicyStoreValidationMode':
        return pulumi.get(self, "mode")


@pulumi.output_type
class PolicyTemplateLinkedPolicyDefinition(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "policyTemplateId":
            suggest = "policy_template_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyTemplateLinkedPolicyDefinition. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyTemplateLinkedPolicyDefinition.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyTemplateLinkedPolicyDefinition.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 policy_template_id: str,
                 principal: Optional['outputs.PolicyEntityIdentifier'] = None,
                 resource: Optional['outputs.PolicyEntityIdentifier'] = None):
        pulumi.set(__self__, "policy_template_id", policy_template_id)
        if principal is not None:
            pulumi.set(__self__, "principal", principal)
        if resource is not None:
            pulumi.set(__self__, "resource", resource)

    @property
    @pulumi.getter(name="policyTemplateId")
    def policy_template_id(self) -> str:
        return pulumi.get(self, "policy_template_id")

    @property
    @pulumi.getter
    def principal(self) -> Optional['outputs.PolicyEntityIdentifier']:
        return pulumi.get(self, "principal")

    @property
    @pulumi.getter
    def resource(self) -> Optional['outputs.PolicyEntityIdentifier']:
        return pulumi.get(self, "resource")


