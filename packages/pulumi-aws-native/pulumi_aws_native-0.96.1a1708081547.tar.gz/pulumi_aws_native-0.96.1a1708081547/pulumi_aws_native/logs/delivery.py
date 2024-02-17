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
from ._inputs import *

__all__ = ['DeliveryArgs', 'Delivery']

@pulumi.input_type
class DeliveryArgs:
    def __init__(__self__, *,
                 delivery_destination_arn: pulumi.Input[str],
                 delivery_source_name: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['DeliveryTagArgs']]]] = None):
        """
        The set of arguments for constructing a Delivery resource.
        :param pulumi.Input[str] delivery_destination_arn: The ARN of the delivery destination that is associated with this delivery.
        :param pulumi.Input[str] delivery_source_name: The name of the delivery source that is associated with this delivery.
        :param pulumi.Input[Sequence[pulumi.Input['DeliveryTagArgs']]] tags: The tags that have been assigned to this delivery.
        """
        pulumi.set(__self__, "delivery_destination_arn", delivery_destination_arn)
        pulumi.set(__self__, "delivery_source_name", delivery_source_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="deliveryDestinationArn")
    def delivery_destination_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the delivery destination that is associated with this delivery.
        """
        return pulumi.get(self, "delivery_destination_arn")

    @delivery_destination_arn.setter
    def delivery_destination_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "delivery_destination_arn", value)

    @property
    @pulumi.getter(name="deliverySourceName")
    def delivery_source_name(self) -> pulumi.Input[str]:
        """
        The name of the delivery source that is associated with this delivery.
        """
        return pulumi.get(self, "delivery_source_name")

    @delivery_source_name.setter
    def delivery_source_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "delivery_source_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DeliveryTagArgs']]]]:
        """
        The tags that have been assigned to this delivery.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DeliveryTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Delivery(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delivery_destination_arn: Optional[pulumi.Input[str]] = None,
                 delivery_source_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeliveryTagArgs']]]]] = None,
                 __props__=None):
        """
        This structure contains information about one delivery in your account.

        A delivery is a connection between a logical delivery source and a logical delivery destination.

        For more information, see [CreateDelivery](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateDelivery.html).

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] delivery_destination_arn: The ARN of the delivery destination that is associated with this delivery.
        :param pulumi.Input[str] delivery_source_name: The name of the delivery source that is associated with this delivery.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeliveryTagArgs']]]] tags: The tags that have been assigned to this delivery.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DeliveryArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This structure contains information about one delivery in your account.

        A delivery is a connection between a logical delivery source and a logical delivery destination.

        For more information, see [CreateDelivery](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateDelivery.html).

        :param str resource_name: The name of the resource.
        :param DeliveryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeliveryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delivery_destination_arn: Optional[pulumi.Input[str]] = None,
                 delivery_source_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeliveryTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DeliveryArgs.__new__(DeliveryArgs)

            if delivery_destination_arn is None and not opts.urn:
                raise TypeError("Missing required property 'delivery_destination_arn'")
            __props__.__dict__["delivery_destination_arn"] = delivery_destination_arn
            if delivery_source_name is None and not opts.urn:
                raise TypeError("Missing required property 'delivery_source_name'")
            __props__.__dict__["delivery_source_name"] = delivery_source_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["delivery_destination_type"] = None
            __props__.__dict__["delivery_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["delivery_destination_arn", "delivery_source_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Delivery, __self__).__init__(
            'aws-native:logs:Delivery',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Delivery':
        """
        Get an existing Delivery resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DeliveryArgs.__new__(DeliveryArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["delivery_destination_arn"] = None
        __props__.__dict__["delivery_destination_type"] = None
        __props__.__dict__["delivery_id"] = None
        __props__.__dict__["delivery_source_name"] = None
        __props__.__dict__["tags"] = None
        return Delivery(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) that uniquely identifies this delivery.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="deliveryDestinationArn")
    def delivery_destination_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the delivery destination that is associated with this delivery.
        """
        return pulumi.get(self, "delivery_destination_arn")

    @property
    @pulumi.getter(name="deliveryDestinationType")
    def delivery_destination_type(self) -> pulumi.Output[str]:
        """
        Displays whether the delivery destination associated with this delivery is CloudWatch Logs, Amazon S3, or Kinesis Data Firehose.
        """
        return pulumi.get(self, "delivery_destination_type")

    @property
    @pulumi.getter(name="deliveryId")
    def delivery_id(self) -> pulumi.Output[str]:
        """
        The unique ID that identifies this delivery in your account.
        """
        return pulumi.get(self, "delivery_id")

    @property
    @pulumi.getter(name="deliverySourceName")
    def delivery_source_name(self) -> pulumi.Output[str]:
        """
        The name of the delivery source that is associated with this delivery.
        """
        return pulumi.get(self, "delivery_source_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.DeliveryTag']]]:
        """
        The tags that have been assigned to this delivery.
        """
        return pulumi.get(self, "tags")

