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
    'GetTransitGatewayRouteTableResult',
    'AwaitableGetTransitGatewayRouteTableResult',
    'get_transit_gateway_route_table',
    'get_transit_gateway_route_table_output',
]

@pulumi.output_type
class GetTransitGatewayRouteTableResult:
    def __init__(__self__, transit_gateway_route_table_id=None):
        if transit_gateway_route_table_id and not isinstance(transit_gateway_route_table_id, str):
            raise TypeError("Expected argument 'transit_gateway_route_table_id' to be a str")
        pulumi.set(__self__, "transit_gateway_route_table_id", transit_gateway_route_table_id)

    @property
    @pulumi.getter(name="transitGatewayRouteTableId")
    def transit_gateway_route_table_id(self) -> Optional[str]:
        """
        Transit Gateway Route Table primary identifier
        """
        return pulumi.get(self, "transit_gateway_route_table_id")


class AwaitableGetTransitGatewayRouteTableResult(GetTransitGatewayRouteTableResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTransitGatewayRouteTableResult(
            transit_gateway_route_table_id=self.transit_gateway_route_table_id)


def get_transit_gateway_route_table(transit_gateway_route_table_id: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTransitGatewayRouteTableResult:
    """
    Resource Type definition for AWS::EC2::TransitGatewayRouteTable


    :param str transit_gateway_route_table_id: Transit Gateway Route Table primary identifier
    """
    __args__ = dict()
    __args__['transitGatewayRouteTableId'] = transit_gateway_route_table_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getTransitGatewayRouteTable', __args__, opts=opts, typ=GetTransitGatewayRouteTableResult).value

    return AwaitableGetTransitGatewayRouteTableResult(
        transit_gateway_route_table_id=pulumi.get(__ret__, 'transit_gateway_route_table_id'))


@_utilities.lift_output_func(get_transit_gateway_route_table)
def get_transit_gateway_route_table_output(transit_gateway_route_table_id: Optional[pulumi.Input[str]] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTransitGatewayRouteTableResult]:
    """
    Resource Type definition for AWS::EC2::TransitGatewayRouteTable


    :param str transit_gateway_route_table_id: Transit Gateway Route Table primary identifier
    """
    ...
