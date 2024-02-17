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
    'GetConfigurationProfileResult',
    'AwaitableGetConfigurationProfileResult',
    'get_configuration_profile',
    'get_configuration_profile_output',
]

@pulumi.output_type
class GetConfigurationProfileResult:
    def __init__(__self__, configuration_profile_id=None, description=None, kms_key_arn=None, kms_key_identifier=None, name=None, retrieval_role_arn=None, tags=None, validators=None):
        if configuration_profile_id and not isinstance(configuration_profile_id, str):
            raise TypeError("Expected argument 'configuration_profile_id' to be a str")
        pulumi.set(__self__, "configuration_profile_id", configuration_profile_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if kms_key_arn and not isinstance(kms_key_arn, str):
            raise TypeError("Expected argument 'kms_key_arn' to be a str")
        pulumi.set(__self__, "kms_key_arn", kms_key_arn)
        if kms_key_identifier and not isinstance(kms_key_identifier, str):
            raise TypeError("Expected argument 'kms_key_identifier' to be a str")
        pulumi.set(__self__, "kms_key_identifier", kms_key_identifier)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if retrieval_role_arn and not isinstance(retrieval_role_arn, str):
            raise TypeError("Expected argument 'retrieval_role_arn' to be a str")
        pulumi.set(__self__, "retrieval_role_arn", retrieval_role_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if validators and not isinstance(validators, list):
            raise TypeError("Expected argument 'validators' to be a list")
        pulumi.set(__self__, "validators", validators)

    @property
    @pulumi.getter(name="configurationProfileId")
    def configuration_profile_id(self) -> Optional[str]:
        """
        The configuration profile ID
        """
        return pulumi.get(self, "configuration_profile_id")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of the configuration profile.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name of the AWS Key Management Service key to encrypt new configuration data versions in the AWS AppConfig hosted configuration store. This attribute is only used for hosted configuration types. To encrypt data managed in other configuration stores, see the documentation for how to specify an AWS KMS key for that particular service.
        """
        return pulumi.get(self, "kms_key_arn")

    @property
    @pulumi.getter(name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> Optional[str]:
        """
        The AWS Key Management Service key identifier (key ID, key alias, or key ARN) provided when the resource was created or updated.
        """
        return pulumi.get(self, "kms_key_identifier")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A name for the configuration profile.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="retrievalRoleArn")
    def retrieval_role_arn(self) -> Optional[str]:
        """
        The ARN of an IAM role with permission to access the configuration at the specified LocationUri.
        """
        return pulumi.get(self, "retrieval_role_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.ConfigurationProfileTags']]:
        """
        Metadata to assign to the configuration profile. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def validators(self) -> Optional[Sequence['outputs.ConfigurationProfileValidators']]:
        """
        A list of methods for validating the configuration.
        """
        return pulumi.get(self, "validators")


class AwaitableGetConfigurationProfileResult(GetConfigurationProfileResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConfigurationProfileResult(
            configuration_profile_id=self.configuration_profile_id,
            description=self.description,
            kms_key_arn=self.kms_key_arn,
            kms_key_identifier=self.kms_key_identifier,
            name=self.name,
            retrieval_role_arn=self.retrieval_role_arn,
            tags=self.tags,
            validators=self.validators)


def get_configuration_profile(application_id: Optional[str] = None,
                              configuration_profile_id: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConfigurationProfileResult:
    """
    An example resource schema demonstrating some basic constructs and validation rules.


    :param str application_id: The application ID.
    :param str configuration_profile_id: The configuration profile ID
    """
    __args__ = dict()
    __args__['applicationId'] = application_id
    __args__['configurationProfileId'] = configuration_profile_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:appconfig:getConfigurationProfile', __args__, opts=opts, typ=GetConfigurationProfileResult).value

    return AwaitableGetConfigurationProfileResult(
        configuration_profile_id=pulumi.get(__ret__, 'configuration_profile_id'),
        description=pulumi.get(__ret__, 'description'),
        kms_key_arn=pulumi.get(__ret__, 'kms_key_arn'),
        kms_key_identifier=pulumi.get(__ret__, 'kms_key_identifier'),
        name=pulumi.get(__ret__, 'name'),
        retrieval_role_arn=pulumi.get(__ret__, 'retrieval_role_arn'),
        tags=pulumi.get(__ret__, 'tags'),
        validators=pulumi.get(__ret__, 'validators'))


@_utilities.lift_output_func(get_configuration_profile)
def get_configuration_profile_output(application_id: Optional[pulumi.Input[str]] = None,
                                     configuration_profile_id: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConfigurationProfileResult]:
    """
    An example resource schema demonstrating some basic constructs and validation rules.


    :param str application_id: The application ID.
    :param str configuration_profile_id: The configuration profile ID
    """
    ...
