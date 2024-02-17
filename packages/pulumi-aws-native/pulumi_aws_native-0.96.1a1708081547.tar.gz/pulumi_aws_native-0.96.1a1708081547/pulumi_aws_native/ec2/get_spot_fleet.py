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
    'GetSpotFleetResult',
    'AwaitableGetSpotFleetResult',
    'get_spot_fleet',
    'get_spot_fleet_output',
]

@pulumi.output_type
class GetSpotFleetResult:
    def __init__(__self__, id=None, spot_fleet_request_config_data=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if spot_fleet_request_config_data and not isinstance(spot_fleet_request_config_data, dict):
            raise TypeError("Expected argument 'spot_fleet_request_config_data' to be a dict")
        pulumi.set(__self__, "spot_fleet_request_config_data", spot_fleet_request_config_data)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="spotFleetRequestConfigData")
    def spot_fleet_request_config_data(self) -> Optional['outputs.SpotFleetRequestConfigData']:
        return pulumi.get(self, "spot_fleet_request_config_data")


class AwaitableGetSpotFleetResult(GetSpotFleetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSpotFleetResult(
            id=self.id,
            spot_fleet_request_config_data=self.spot_fleet_request_config_data)


def get_spot_fleet(id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSpotFleetResult:
    """
    Resource Type definition for AWS::EC2::SpotFleet
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getSpotFleet', __args__, opts=opts, typ=GetSpotFleetResult).value

    return AwaitableGetSpotFleetResult(
        id=pulumi.get(__ret__, 'id'),
        spot_fleet_request_config_data=pulumi.get(__ret__, 'spot_fleet_request_config_data'))


@_utilities.lift_output_func(get_spot_fleet)
def get_spot_fleet_output(id: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSpotFleetResult]:
    """
    Resource Type definition for AWS::EC2::SpotFleet
    """
    ...
