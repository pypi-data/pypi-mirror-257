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
    'GetApiGatewayManagedOverridesResult',
    'AwaitableGetApiGatewayManagedOverridesResult',
    'get_api_gateway_managed_overrides',
    'get_api_gateway_managed_overrides_output',
]

@pulumi.output_type
class GetApiGatewayManagedOverridesResult:
    def __init__(__self__, id=None, integration=None, route=None, stage=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if integration and not isinstance(integration, dict):
            raise TypeError("Expected argument 'integration' to be a dict")
        pulumi.set(__self__, "integration", integration)
        if route and not isinstance(route, dict):
            raise TypeError("Expected argument 'route' to be a dict")
        pulumi.set(__self__, "route", route)
        if stage and not isinstance(stage, dict):
            raise TypeError("Expected argument 'stage' to be a dict")
        pulumi.set(__self__, "stage", stage)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def integration(self) -> Optional['outputs.ApiGatewayManagedOverridesIntegrationOverrides']:
        return pulumi.get(self, "integration")

    @property
    @pulumi.getter
    def route(self) -> Optional['outputs.ApiGatewayManagedOverridesRouteOverrides']:
        return pulumi.get(self, "route")

    @property
    @pulumi.getter
    def stage(self) -> Optional['outputs.ApiGatewayManagedOverridesStageOverrides']:
        return pulumi.get(self, "stage")


class AwaitableGetApiGatewayManagedOverridesResult(GetApiGatewayManagedOverridesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApiGatewayManagedOverridesResult(
            id=self.id,
            integration=self.integration,
            route=self.route,
            stage=self.stage)


def get_api_gateway_managed_overrides(id: Optional[str] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApiGatewayManagedOverridesResult:
    """
    Resource Type definition for AWS::ApiGatewayV2::ApiGatewayManagedOverrides
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:apigatewayv2:getApiGatewayManagedOverrides', __args__, opts=opts, typ=GetApiGatewayManagedOverridesResult).value

    return AwaitableGetApiGatewayManagedOverridesResult(
        id=pulumi.get(__ret__, 'id'),
        integration=pulumi.get(__ret__, 'integration'),
        route=pulumi.get(__ret__, 'route'),
        stage=pulumi.get(__ret__, 'stage'))


@_utilities.lift_output_func(get_api_gateway_managed_overrides)
def get_api_gateway_managed_overrides_output(id: Optional[pulumi.Input[str]] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApiGatewayManagedOverridesResult]:
    """
    Resource Type definition for AWS::ApiGatewayV2::ApiGatewayManagedOverrides
    """
    ...
