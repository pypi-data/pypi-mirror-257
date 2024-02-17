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
    'GetDeliveryResult',
    'AwaitableGetDeliveryResult',
    'get_delivery',
    'get_delivery_output',
]

@pulumi.output_type
class GetDeliveryResult:
    def __init__(__self__, arn=None, delivery_destination_type=None, delivery_id=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if delivery_destination_type and not isinstance(delivery_destination_type, str):
            raise TypeError("Expected argument 'delivery_destination_type' to be a str")
        pulumi.set(__self__, "delivery_destination_type", delivery_destination_type)
        if delivery_id and not isinstance(delivery_id, str):
            raise TypeError("Expected argument 'delivery_id' to be a str")
        pulumi.set(__self__, "delivery_id", delivery_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) that uniquely identifies this delivery.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="deliveryDestinationType")
    def delivery_destination_type(self) -> Optional[str]:
        """
        Displays whether the delivery destination associated with this delivery is CloudWatch Logs, Amazon S3, or Kinesis Data Firehose.
        """
        return pulumi.get(self, "delivery_destination_type")

    @property
    @pulumi.getter(name="deliveryId")
    def delivery_id(self) -> Optional[str]:
        """
        The unique ID that identifies this delivery in your account.
        """
        return pulumi.get(self, "delivery_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.DeliveryTag']]:
        """
        The tags that have been assigned to this delivery.
        """
        return pulumi.get(self, "tags")


class AwaitableGetDeliveryResult(GetDeliveryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDeliveryResult(
            arn=self.arn,
            delivery_destination_type=self.delivery_destination_type,
            delivery_id=self.delivery_id,
            tags=self.tags)


def get_delivery(delivery_id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDeliveryResult:
    """
    This structure contains information about one delivery in your account.

    A delivery is a connection between a logical delivery source and a logical delivery destination.

    For more information, see [CreateDelivery](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateDelivery.html).


    :param str delivery_id: The unique ID that identifies this delivery in your account.
    """
    __args__ = dict()
    __args__['deliveryId'] = delivery_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:logs:getDelivery', __args__, opts=opts, typ=GetDeliveryResult).value

    return AwaitableGetDeliveryResult(
        arn=pulumi.get(__ret__, 'arn'),
        delivery_destination_type=pulumi.get(__ret__, 'delivery_destination_type'),
        delivery_id=pulumi.get(__ret__, 'delivery_id'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_delivery)
def get_delivery_output(delivery_id: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDeliveryResult]:
    """
    This structure contains information about one delivery in your account.

    A delivery is a connection between a logical delivery source and a logical delivery destination.

    For more information, see [CreateDelivery](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateDelivery.html).


    :param str delivery_id: The unique ID that identifies this delivery in your account.
    """
    ...
