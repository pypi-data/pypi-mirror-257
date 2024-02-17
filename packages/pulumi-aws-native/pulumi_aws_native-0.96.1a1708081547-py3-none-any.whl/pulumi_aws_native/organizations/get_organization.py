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
    'GetOrganizationResult',
    'AwaitableGetOrganizationResult',
    'get_organization',
    'get_organization_output',
]

@pulumi.output_type
class GetOrganizationResult:
    def __init__(__self__, arn=None, feature_set=None, id=None, management_account_arn=None, management_account_email=None, management_account_id=None, root_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if feature_set and not isinstance(feature_set, str):
            raise TypeError("Expected argument 'feature_set' to be a str")
        pulumi.set(__self__, "feature_set", feature_set)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if management_account_arn and not isinstance(management_account_arn, str):
            raise TypeError("Expected argument 'management_account_arn' to be a str")
        pulumi.set(__self__, "management_account_arn", management_account_arn)
        if management_account_email and not isinstance(management_account_email, str):
            raise TypeError("Expected argument 'management_account_email' to be a str")
        pulumi.set(__self__, "management_account_email", management_account_email)
        if management_account_id and not isinstance(management_account_id, str):
            raise TypeError("Expected argument 'management_account_id' to be a str")
        pulumi.set(__self__, "management_account_id", management_account_id)
        if root_id and not isinstance(root_id, str):
            raise TypeError("Expected argument 'root_id' to be a str")
        pulumi.set(__self__, "root_id", root_id)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of an organization.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="featureSet")
    def feature_set(self) -> Optional['OrganizationFeatureSet']:
        """
        Specifies the feature set supported by the new organization. Each feature set supports different levels of functionality.
        """
        return pulumi.get(self, "feature_set")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The unique identifier (ID) of an organization.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="managementAccountArn")
    def management_account_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the account that is designated as the management account for the organization.
        """
        return pulumi.get(self, "management_account_arn")

    @property
    @pulumi.getter(name="managementAccountEmail")
    def management_account_email(self) -> Optional[str]:
        """
        The email address that is associated with the AWS account that is designated as the management account for the organization.
        """
        return pulumi.get(self, "management_account_email")

    @property
    @pulumi.getter(name="managementAccountId")
    def management_account_id(self) -> Optional[str]:
        """
        The unique identifier (ID) of the management account of an organization.
        """
        return pulumi.get(self, "management_account_id")

    @property
    @pulumi.getter(name="rootId")
    def root_id(self) -> Optional[str]:
        """
        The unique identifier (ID) for the root.
        """
        return pulumi.get(self, "root_id")


class AwaitableGetOrganizationResult(GetOrganizationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrganizationResult(
            arn=self.arn,
            feature_set=self.feature_set,
            id=self.id,
            management_account_arn=self.management_account_arn,
            management_account_email=self.management_account_email,
            management_account_id=self.management_account_id,
            root_id=self.root_id)


def get_organization(id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrganizationResult:
    """
    Resource schema for AWS::Organizations::Organization


    :param str id: The unique identifier (ID) of an organization.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:organizations:getOrganization', __args__, opts=opts, typ=GetOrganizationResult).value

    return AwaitableGetOrganizationResult(
        arn=pulumi.get(__ret__, 'arn'),
        feature_set=pulumi.get(__ret__, 'feature_set'),
        id=pulumi.get(__ret__, 'id'),
        management_account_arn=pulumi.get(__ret__, 'management_account_arn'),
        management_account_email=pulumi.get(__ret__, 'management_account_email'),
        management_account_id=pulumi.get(__ret__, 'management_account_id'),
        root_id=pulumi.get(__ret__, 'root_id'))


@_utilities.lift_output_func(get_organization)
def get_organization_output(id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOrganizationResult]:
    """
    Resource schema for AWS::Organizations::Organization


    :param str id: The unique identifier (ID) of an organization.
    """
    ...
