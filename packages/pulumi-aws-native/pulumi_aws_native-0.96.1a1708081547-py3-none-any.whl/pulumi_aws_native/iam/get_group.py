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
    'GetGroupResult',
    'AwaitableGetGroupResult',
    'get_group',
    'get_group_output',
]

@pulumi.output_type
class GetGroupResult:
    def __init__(__self__, arn=None, managed_policy_arns=None, path=None, policies=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if managed_policy_arns and not isinstance(managed_policy_arns, list):
            raise TypeError("Expected argument 'managed_policy_arns' to be a list")
        pulumi.set(__self__, "managed_policy_arns", managed_policy_arns)
        if path and not isinstance(path, str):
            raise TypeError("Expected argument 'path' to be a str")
        pulumi.set(__self__, "path", path)
        if policies and not isinstance(policies, list):
            raise TypeError("Expected argument 'policies' to be a list")
        pulumi.set(__self__, "policies", policies)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Arn of the group to create
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="managedPolicyArns")
    def managed_policy_arns(self) -> Optional[Sequence[str]]:
        """
        A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role. 
        """
        return pulumi.get(self, "managed_policy_arns")

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        """
        The path to the group
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def policies(self) -> Optional[Sequence['outputs.GroupPolicy']]:
        """
        Adds or updates an inline policy document that is embedded in the specified IAM group
        """
        return pulumi.get(self, "policies")


class AwaitableGetGroupResult(GetGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGroupResult(
            arn=self.arn,
            managed_policy_arns=self.managed_policy_arns,
            path=self.path,
            policies=self.policies)


def get_group(group_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGroupResult:
    """
    Resource Type definition for AWS::IAM::Group


    :param str group_name: The name of the group to create
    """
    __args__ = dict()
    __args__['groupName'] = group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iam:getGroup', __args__, opts=opts, typ=GetGroupResult).value

    return AwaitableGetGroupResult(
        arn=pulumi.get(__ret__, 'arn'),
        managed_policy_arns=pulumi.get(__ret__, 'managed_policy_arns'),
        path=pulumi.get(__ret__, 'path'),
        policies=pulumi.get(__ret__, 'policies'))


@_utilities.lift_output_func(get_group)
def get_group_output(group_name: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGroupResult]:
    """
    Resource Type definition for AWS::IAM::Group


    :param str group_name: The name of the group to create
    """
    ...
