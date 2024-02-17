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
    'GetIdentityPoolPrincipalTagResult',
    'AwaitableGetIdentityPoolPrincipalTagResult',
    'get_identity_pool_principal_tag',
    'get_identity_pool_principal_tag_output',
]

@pulumi.output_type
class GetIdentityPoolPrincipalTagResult:
    def __init__(__self__, principal_tags=None, use_defaults=None):
        if principal_tags and not isinstance(principal_tags, dict):
            raise TypeError("Expected argument 'principal_tags' to be a dict")
        pulumi.set(__self__, "principal_tags", principal_tags)
        if use_defaults and not isinstance(use_defaults, bool):
            raise TypeError("Expected argument 'use_defaults' to be a bool")
        pulumi.set(__self__, "use_defaults", use_defaults)

    @property
    @pulumi.getter(name="principalTags")
    def principal_tags(self) -> Optional[Any]:
        return pulumi.get(self, "principal_tags")

    @property
    @pulumi.getter(name="useDefaults")
    def use_defaults(self) -> Optional[bool]:
        return pulumi.get(self, "use_defaults")


class AwaitableGetIdentityPoolPrincipalTagResult(GetIdentityPoolPrincipalTagResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIdentityPoolPrincipalTagResult(
            principal_tags=self.principal_tags,
            use_defaults=self.use_defaults)


def get_identity_pool_principal_tag(identity_pool_id: Optional[str] = None,
                                    identity_provider_name: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIdentityPoolPrincipalTagResult:
    """
    Resource Type definition for AWS::Cognito::IdentityPoolPrincipalTag
    """
    __args__ = dict()
    __args__['identityPoolId'] = identity_pool_id
    __args__['identityProviderName'] = identity_provider_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cognito:getIdentityPoolPrincipalTag', __args__, opts=opts, typ=GetIdentityPoolPrincipalTagResult).value

    return AwaitableGetIdentityPoolPrincipalTagResult(
        principal_tags=pulumi.get(__ret__, 'principal_tags'),
        use_defaults=pulumi.get(__ret__, 'use_defaults'))


@_utilities.lift_output_func(get_identity_pool_principal_tag)
def get_identity_pool_principal_tag_output(identity_pool_id: Optional[pulumi.Input[str]] = None,
                                           identity_provider_name: Optional[pulumi.Input[str]] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIdentityPoolPrincipalTagResult]:
    """
    Resource Type definition for AWS::Cognito::IdentityPoolPrincipalTag
    """
    ...
