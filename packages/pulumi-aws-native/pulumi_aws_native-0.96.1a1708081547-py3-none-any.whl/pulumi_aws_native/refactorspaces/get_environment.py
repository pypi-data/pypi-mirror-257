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
    'GetEnvironmentResult',
    'AwaitableGetEnvironmentResult',
    'get_environment',
    'get_environment_output',
]

@pulumi.output_type
class GetEnvironmentResult:
    def __init__(__self__, arn=None, environment_identifier=None, tags=None, transit_gateway_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if environment_identifier and not isinstance(environment_identifier, str):
            raise TypeError("Expected argument 'environment_identifier' to be a str")
        pulumi.set(__self__, "environment_identifier", environment_identifier)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if transit_gateway_id and not isinstance(transit_gateway_id, str):
            raise TypeError("Expected argument 'transit_gateway_id' to be a str")
        pulumi.set(__self__, "transit_gateway_id", transit_gateway_id)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="environmentIdentifier")
    def environment_identifier(self) -> Optional[str]:
        return pulumi.get(self, "environment_identifier")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.EnvironmentTag']]:
        """
        Metadata that you can assign to help organize the frameworks that you create. Each tag is a key-value pair.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> Optional[str]:
        return pulumi.get(self, "transit_gateway_id")


class AwaitableGetEnvironmentResult(GetEnvironmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEnvironmentResult(
            arn=self.arn,
            environment_identifier=self.environment_identifier,
            tags=self.tags,
            transit_gateway_id=self.transit_gateway_id)


def get_environment(environment_identifier: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEnvironmentResult:
    """
    Definition of AWS::RefactorSpaces::Environment Resource Type
    """
    __args__ = dict()
    __args__['environmentIdentifier'] = environment_identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:refactorspaces:getEnvironment', __args__, opts=opts, typ=GetEnvironmentResult).value

    return AwaitableGetEnvironmentResult(
        arn=pulumi.get(__ret__, 'arn'),
        environment_identifier=pulumi.get(__ret__, 'environment_identifier'),
        tags=pulumi.get(__ret__, 'tags'),
        transit_gateway_id=pulumi.get(__ret__, 'transit_gateway_id'))


@_utilities.lift_output_func(get_environment)
def get_environment_output(environment_identifier: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEnvironmentResult]:
    """
    Definition of AWS::RefactorSpaces::Environment Resource Type
    """
    ...
