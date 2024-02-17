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
    'GetProfileResult',
    'AwaitableGetProfileResult',
    'get_profile',
    'get_profile_output',
]

@pulumi.output_type
class GetProfileResult:
    def __init__(__self__, duration_seconds=None, enabled=None, managed_policy_arns=None, name=None, profile_arn=None, profile_id=None, require_instance_properties=None, role_arns=None, session_policy=None, tags=None):
        if duration_seconds and not isinstance(duration_seconds, float):
            raise TypeError("Expected argument 'duration_seconds' to be a float")
        pulumi.set(__self__, "duration_seconds", duration_seconds)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if managed_policy_arns and not isinstance(managed_policy_arns, list):
            raise TypeError("Expected argument 'managed_policy_arns' to be a list")
        pulumi.set(__self__, "managed_policy_arns", managed_policy_arns)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if profile_arn and not isinstance(profile_arn, str):
            raise TypeError("Expected argument 'profile_arn' to be a str")
        pulumi.set(__self__, "profile_arn", profile_arn)
        if profile_id and not isinstance(profile_id, str):
            raise TypeError("Expected argument 'profile_id' to be a str")
        pulumi.set(__self__, "profile_id", profile_id)
        if require_instance_properties and not isinstance(require_instance_properties, bool):
            raise TypeError("Expected argument 'require_instance_properties' to be a bool")
        pulumi.set(__self__, "require_instance_properties", require_instance_properties)
        if role_arns and not isinstance(role_arns, list):
            raise TypeError("Expected argument 'role_arns' to be a list")
        pulumi.set(__self__, "role_arns", role_arns)
        if session_policy and not isinstance(session_policy, str):
            raise TypeError("Expected argument 'session_policy' to be a str")
        pulumi.set(__self__, "session_policy", session_policy)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="durationSeconds")
    def duration_seconds(self) -> Optional[float]:
        return pulumi.get(self, "duration_seconds")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="managedPolicyArns")
    def managed_policy_arns(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "managed_policy_arns")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="profileArn")
    def profile_arn(self) -> Optional[str]:
        return pulumi.get(self, "profile_arn")

    @property
    @pulumi.getter(name="profileId")
    def profile_id(self) -> Optional[str]:
        return pulumi.get(self, "profile_id")

    @property
    @pulumi.getter(name="requireInstanceProperties")
    def require_instance_properties(self) -> Optional[bool]:
        return pulumi.get(self, "require_instance_properties")

    @property
    @pulumi.getter(name="roleArns")
    def role_arns(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "role_arns")

    @property
    @pulumi.getter(name="sessionPolicy")
    def session_policy(self) -> Optional[str]:
        return pulumi.get(self, "session_policy")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.ProfileTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetProfileResult(GetProfileResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProfileResult(
            duration_seconds=self.duration_seconds,
            enabled=self.enabled,
            managed_policy_arns=self.managed_policy_arns,
            name=self.name,
            profile_arn=self.profile_arn,
            profile_id=self.profile_id,
            require_instance_properties=self.require_instance_properties,
            role_arns=self.role_arns,
            session_policy=self.session_policy,
            tags=self.tags)


def get_profile(profile_id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProfileResult:
    """
    Definition of AWS::RolesAnywhere::Profile Resource Type
    """
    __args__ = dict()
    __args__['profileId'] = profile_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:rolesanywhere:getProfile', __args__, opts=opts, typ=GetProfileResult).value

    return AwaitableGetProfileResult(
        duration_seconds=pulumi.get(__ret__, 'duration_seconds'),
        enabled=pulumi.get(__ret__, 'enabled'),
        managed_policy_arns=pulumi.get(__ret__, 'managed_policy_arns'),
        name=pulumi.get(__ret__, 'name'),
        profile_arn=pulumi.get(__ret__, 'profile_arn'),
        profile_id=pulumi.get(__ret__, 'profile_id'),
        require_instance_properties=pulumi.get(__ret__, 'require_instance_properties'),
        role_arns=pulumi.get(__ret__, 'role_arns'),
        session_policy=pulumi.get(__ret__, 'session_policy'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_profile)
def get_profile_output(profile_id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProfileResult]:
    """
    Definition of AWS::RolesAnywhere::Profile Resource Type
    """
    ...
