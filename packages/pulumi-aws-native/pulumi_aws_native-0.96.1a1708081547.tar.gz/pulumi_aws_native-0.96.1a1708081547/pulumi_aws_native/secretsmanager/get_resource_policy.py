# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetResourcePolicyResult',
    'AwaitableGetResourcePolicyResult',
    'get_resource_policy',
    'get_resource_policy_output',
]

@pulumi.output_type
class GetResourcePolicyResult:
    def __init__(__self__, block_public_policy=None, id=None, resource_policy=None):
        if block_public_policy and not isinstance(block_public_policy, bool):
            raise TypeError("Expected argument 'block_public_policy' to be a bool")
        pulumi.set(__self__, "block_public_policy", block_public_policy)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if resource_policy and not isinstance(resource_policy, dict):
            raise TypeError("Expected argument 'resource_policy' to be a dict")
        pulumi.set(__self__, "resource_policy", resource_policy)

    @property
    @pulumi.getter(name="blockPublicPolicy")
    def block_public_policy(self) -> Optional[bool]:
        return pulumi.get(self, "block_public_policy")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="resourcePolicy")
    def resource_policy(self) -> Optional[Any]:
        return pulumi.get(self, "resource_policy")


class AwaitableGetResourcePolicyResult(GetResourcePolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourcePolicyResult(
            block_public_policy=self.block_public_policy,
            id=self.id,
            resource_policy=self.resource_policy)


def get_resource_policy(id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourcePolicyResult:
    """
    Resource Type definition for AWS::SecretsManager::ResourcePolicy
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:secretsmanager:getResourcePolicy', __args__, opts=opts, typ=GetResourcePolicyResult).value

    return AwaitableGetResourcePolicyResult(
        block_public_policy=pulumi.get(__ret__, 'block_public_policy'),
        id=pulumi.get(__ret__, 'id'),
        resource_policy=pulumi.get(__ret__, 'resource_policy'))


@_utilities.lift_output_func(get_resource_policy)
def get_resource_policy_output(id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResourcePolicyResult]:
    """
    Resource Type definition for AWS::SecretsManager::ResourcePolicy
    """
    ...
