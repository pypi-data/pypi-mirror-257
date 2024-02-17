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
    'GetVpcEndpointConnectionNotificationResult',
    'AwaitableGetVpcEndpointConnectionNotificationResult',
    'get_vpc_endpoint_connection_notification',
    'get_vpc_endpoint_connection_notification_output',
]

@pulumi.output_type
class GetVpcEndpointConnectionNotificationResult:
    def __init__(__self__, connection_events=None, connection_notification_arn=None, vpc_endpoint_connection_notification_id=None):
        if connection_events and not isinstance(connection_events, list):
            raise TypeError("Expected argument 'connection_events' to be a list")
        pulumi.set(__self__, "connection_events", connection_events)
        if connection_notification_arn and not isinstance(connection_notification_arn, str):
            raise TypeError("Expected argument 'connection_notification_arn' to be a str")
        pulumi.set(__self__, "connection_notification_arn", connection_notification_arn)
        if vpc_endpoint_connection_notification_id and not isinstance(vpc_endpoint_connection_notification_id, str):
            raise TypeError("Expected argument 'vpc_endpoint_connection_notification_id' to be a str")
        pulumi.set(__self__, "vpc_endpoint_connection_notification_id", vpc_endpoint_connection_notification_id)

    @property
    @pulumi.getter(name="connectionEvents")
    def connection_events(self) -> Optional[Sequence[str]]:
        """
        The endpoint events for which to receive notifications.
        """
        return pulumi.get(self, "connection_events")

    @property
    @pulumi.getter(name="connectionNotificationArn")
    def connection_notification_arn(self) -> Optional[str]:
        """
        The ARN of the SNS topic for the notifications.
        """
        return pulumi.get(self, "connection_notification_arn")

    @property
    @pulumi.getter(name="vpcEndpointConnectionNotificationId")
    def vpc_endpoint_connection_notification_id(self) -> Optional[str]:
        """
        VPC Endpoint Connection ID generated by service
        """
        return pulumi.get(self, "vpc_endpoint_connection_notification_id")


class AwaitableGetVpcEndpointConnectionNotificationResult(GetVpcEndpointConnectionNotificationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcEndpointConnectionNotificationResult(
            connection_events=self.connection_events,
            connection_notification_arn=self.connection_notification_arn,
            vpc_endpoint_connection_notification_id=self.vpc_endpoint_connection_notification_id)


def get_vpc_endpoint_connection_notification(vpc_endpoint_connection_notification_id: Optional[str] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcEndpointConnectionNotificationResult:
    """
    Resource Type definition for AWS::EC2::VPCEndpointConnectionNotification


    :param str vpc_endpoint_connection_notification_id: VPC Endpoint Connection ID generated by service
    """
    __args__ = dict()
    __args__['vpcEndpointConnectionNotificationId'] = vpc_endpoint_connection_notification_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getVpcEndpointConnectionNotification', __args__, opts=opts, typ=GetVpcEndpointConnectionNotificationResult).value

    return AwaitableGetVpcEndpointConnectionNotificationResult(
        connection_events=pulumi.get(__ret__, 'connection_events'),
        connection_notification_arn=pulumi.get(__ret__, 'connection_notification_arn'),
        vpc_endpoint_connection_notification_id=pulumi.get(__ret__, 'vpc_endpoint_connection_notification_id'))


@_utilities.lift_output_func(get_vpc_endpoint_connection_notification)
def get_vpc_endpoint_connection_notification_output(vpc_endpoint_connection_notification_id: Optional[pulumi.Input[str]] = None,
                                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVpcEndpointConnectionNotificationResult]:
    """
    Resource Type definition for AWS::EC2::VPCEndpointConnectionNotification


    :param str vpc_endpoint_connection_notification_id: VPC Endpoint Connection ID generated by service
    """
    ...
