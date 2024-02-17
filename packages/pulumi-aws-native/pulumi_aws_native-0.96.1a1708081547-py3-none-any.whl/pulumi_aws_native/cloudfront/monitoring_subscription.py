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
from ._inputs import *

__all__ = ['MonitoringSubscriptionInitArgs', 'MonitoringSubscription']

@pulumi.input_type
class MonitoringSubscriptionInitArgs:
    def __init__(__self__, *,
                 distribution_id: pulumi.Input[str],
                 monitoring_subscription: pulumi.Input['MonitoringSubscriptionArgs']):
        """
        The set of arguments for constructing a MonitoringSubscription resource.
        """
        pulumi.set(__self__, "distribution_id", distribution_id)
        pulumi.set(__self__, "monitoring_subscription", monitoring_subscription)

    @property
    @pulumi.getter(name="distributionId")
    def distribution_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "distribution_id")

    @distribution_id.setter
    def distribution_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "distribution_id", value)

    @property
    @pulumi.getter(name="monitoringSubscription")
    def monitoring_subscription(self) -> pulumi.Input['MonitoringSubscriptionArgs']:
        return pulumi.get(self, "monitoring_subscription")

    @monitoring_subscription.setter
    def monitoring_subscription(self, value: pulumi.Input['MonitoringSubscriptionArgs']):
        pulumi.set(self, "monitoring_subscription", value)


class MonitoringSubscription(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 distribution_id: Optional[pulumi.Input[str]] = None,
                 monitoring_subscription: Optional[pulumi.Input[pulumi.InputType['MonitoringSubscriptionArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::CloudFront::MonitoringSubscription

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MonitoringSubscriptionInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::CloudFront::MonitoringSubscription

        :param str resource_name: The name of the resource.
        :param MonitoringSubscriptionInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MonitoringSubscriptionInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 distribution_id: Optional[pulumi.Input[str]] = None,
                 monitoring_subscription: Optional[pulumi.Input[pulumi.InputType['MonitoringSubscriptionArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MonitoringSubscriptionInitArgs.__new__(MonitoringSubscriptionInitArgs)

            if distribution_id is None and not opts.urn:
                raise TypeError("Missing required property 'distribution_id'")
            __props__.__dict__["distribution_id"] = distribution_id
            if monitoring_subscription is None and not opts.urn:
                raise TypeError("Missing required property 'monitoring_subscription'")
            __props__.__dict__["monitoring_subscription"] = monitoring_subscription
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["distribution_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(MonitoringSubscription, __self__).__init__(
            'aws-native:cloudfront:MonitoringSubscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MonitoringSubscription':
        """
        Get an existing MonitoringSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MonitoringSubscriptionInitArgs.__new__(MonitoringSubscriptionInitArgs)

        __props__.__dict__["distribution_id"] = None
        __props__.__dict__["monitoring_subscription"] = None
        return MonitoringSubscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="distributionId")
    def distribution_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "distribution_id")

    @property
    @pulumi.getter(name="monitoringSubscription")
    def monitoring_subscription(self) -> pulumi.Output['outputs.MonitoringSubscription']:
        return pulumi.get(self, "monitoring_subscription")

