# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'IdentitySourceCognitoUserPoolConfigurationArgs',
    'IdentitySourceConfigurationArgs',
    'PolicyDefinition0PropertiesArgs',
    'PolicyDefinition1PropertiesArgs',
    'PolicyEntityIdentifierArgs',
    'PolicyStaticPolicyDefinitionArgs',
    'PolicyStoreSchemaDefinitionArgs',
    'PolicyStoreValidationSettingsArgs',
    'PolicyTemplateLinkedPolicyDefinitionArgs',
]

@pulumi.input_type
class IdentitySourceCognitoUserPoolConfigurationArgs:
    def __init__(__self__, *,
                 user_pool_arn: pulumi.Input[str],
                 client_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        pulumi.set(__self__, "user_pool_arn", user_pool_arn)
        if client_ids is not None:
            pulumi.set(__self__, "client_ids", client_ids)

    @property
    @pulumi.getter(name="userPoolArn")
    def user_pool_arn(self) -> pulumi.Input[str]:
        return pulumi.get(self, "user_pool_arn")

    @user_pool_arn.setter
    def user_pool_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_pool_arn", value)

    @property
    @pulumi.getter(name="clientIds")
    def client_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "client_ids")

    @client_ids.setter
    def client_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "client_ids", value)


@pulumi.input_type
class IdentitySourceConfigurationArgs:
    def __init__(__self__, *,
                 cognito_user_pool_configuration: pulumi.Input['IdentitySourceCognitoUserPoolConfigurationArgs']):
        pulumi.set(__self__, "cognito_user_pool_configuration", cognito_user_pool_configuration)

    @property
    @pulumi.getter(name="cognitoUserPoolConfiguration")
    def cognito_user_pool_configuration(self) -> pulumi.Input['IdentitySourceCognitoUserPoolConfigurationArgs']:
        return pulumi.get(self, "cognito_user_pool_configuration")

    @cognito_user_pool_configuration.setter
    def cognito_user_pool_configuration(self, value: pulumi.Input['IdentitySourceCognitoUserPoolConfigurationArgs']):
        pulumi.set(self, "cognito_user_pool_configuration", value)


@pulumi.input_type
class PolicyDefinition0PropertiesArgs:
    def __init__(__self__, *,
                 static: pulumi.Input['PolicyStaticPolicyDefinitionArgs']):
        pulumi.set(__self__, "static", static)

    @property
    @pulumi.getter
    def static(self) -> pulumi.Input['PolicyStaticPolicyDefinitionArgs']:
        return pulumi.get(self, "static")

    @static.setter
    def static(self, value: pulumi.Input['PolicyStaticPolicyDefinitionArgs']):
        pulumi.set(self, "static", value)


@pulumi.input_type
class PolicyDefinition1PropertiesArgs:
    def __init__(__self__, *,
                 template_linked: pulumi.Input['PolicyTemplateLinkedPolicyDefinitionArgs']):
        pulumi.set(__self__, "template_linked", template_linked)

    @property
    @pulumi.getter(name="templateLinked")
    def template_linked(self) -> pulumi.Input['PolicyTemplateLinkedPolicyDefinitionArgs']:
        return pulumi.get(self, "template_linked")

    @template_linked.setter
    def template_linked(self, value: pulumi.Input['PolicyTemplateLinkedPolicyDefinitionArgs']):
        pulumi.set(self, "template_linked", value)


@pulumi.input_type
class PolicyEntityIdentifierArgs:
    def __init__(__self__, *,
                 entity_id: pulumi.Input[str],
                 entity_type: pulumi.Input[str]):
        pulumi.set(__self__, "entity_id", entity_id)
        pulumi.set(__self__, "entity_type", entity_type)

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "entity_id")

    @entity_id.setter
    def entity_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "entity_id", value)

    @property
    @pulumi.getter(name="entityType")
    def entity_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "entity_type")

    @entity_type.setter
    def entity_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "entity_type", value)


@pulumi.input_type
class PolicyStaticPolicyDefinitionArgs:
    def __init__(__self__, *,
                 statement: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "statement", statement)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def statement(self) -> pulumi.Input[str]:
        return pulumi.get(self, "statement")

    @statement.setter
    def statement(self, value: pulumi.Input[str]):
        pulumi.set(self, "statement", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class PolicyStoreSchemaDefinitionArgs:
    def __init__(__self__, *,
                 cedar_json: Optional[pulumi.Input[str]] = None):
        if cedar_json is not None:
            pulumi.set(__self__, "cedar_json", cedar_json)

    @property
    @pulumi.getter(name="cedarJson")
    def cedar_json(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cedar_json")

    @cedar_json.setter
    def cedar_json(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cedar_json", value)


@pulumi.input_type
class PolicyStoreValidationSettingsArgs:
    def __init__(__self__, *,
                 mode: pulumi.Input['PolicyStoreValidationMode']):
        pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter
    def mode(self) -> pulumi.Input['PolicyStoreValidationMode']:
        return pulumi.get(self, "mode")

    @mode.setter
    def mode(self, value: pulumi.Input['PolicyStoreValidationMode']):
        pulumi.set(self, "mode", value)


@pulumi.input_type
class PolicyTemplateLinkedPolicyDefinitionArgs:
    def __init__(__self__, *,
                 policy_template_id: pulumi.Input[str],
                 principal: Optional[pulumi.Input['PolicyEntityIdentifierArgs']] = None,
                 resource: Optional[pulumi.Input['PolicyEntityIdentifierArgs']] = None):
        pulumi.set(__self__, "policy_template_id", policy_template_id)
        if principal is not None:
            pulumi.set(__self__, "principal", principal)
        if resource is not None:
            pulumi.set(__self__, "resource", resource)

    @property
    @pulumi.getter(name="policyTemplateId")
    def policy_template_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "policy_template_id")

    @policy_template_id.setter
    def policy_template_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_template_id", value)

    @property
    @pulumi.getter
    def principal(self) -> Optional[pulumi.Input['PolicyEntityIdentifierArgs']]:
        return pulumi.get(self, "principal")

    @principal.setter
    def principal(self, value: Optional[pulumi.Input['PolicyEntityIdentifierArgs']]):
        pulumi.set(self, "principal", value)

    @property
    @pulumi.getter
    def resource(self) -> Optional[pulumi.Input['PolicyEntityIdentifierArgs']]:
        return pulumi.get(self, "resource")

    @resource.setter
    def resource(self, value: Optional[pulumi.Input['PolicyEntityIdentifierArgs']]):
        pulumi.set(self, "resource", value)


