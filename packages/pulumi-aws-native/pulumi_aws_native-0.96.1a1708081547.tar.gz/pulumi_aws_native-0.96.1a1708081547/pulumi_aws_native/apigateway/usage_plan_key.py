# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = ['UsagePlanKeyArgs', 'UsagePlanKey']

@pulumi.input_type
class UsagePlanKeyArgs:
    def __init__(__self__, *,
                 key_id: pulumi.Input[str],
                 key_type: pulumi.Input['UsagePlanKeyKeyType'],
                 usage_plan_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a UsagePlanKey resource.
        :param pulumi.Input[str] key_id: The Id of the UsagePlanKey resource.
        :param pulumi.Input['UsagePlanKeyKeyType'] key_type: The type of a UsagePlanKey resource for a plan customer.
        :param pulumi.Input[str] usage_plan_id: The Id of the UsagePlan resource representing the usage plan containing the UsagePlanKey resource representing a plan customer.
        """
        pulumi.set(__self__, "key_id", key_id)
        pulumi.set(__self__, "key_type", key_type)
        pulumi.set(__self__, "usage_plan_id", usage_plan_id)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> pulumi.Input[str]:
        """
        The Id of the UsagePlanKey resource.
        """
        return pulumi.get(self, "key_id")

    @key_id.setter
    def key_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_id", value)

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> pulumi.Input['UsagePlanKeyKeyType']:
        """
        The type of a UsagePlanKey resource for a plan customer.
        """
        return pulumi.get(self, "key_type")

    @key_type.setter
    def key_type(self, value: pulumi.Input['UsagePlanKeyKeyType']):
        pulumi.set(self, "key_type", value)

    @property
    @pulumi.getter(name="usagePlanId")
    def usage_plan_id(self) -> pulumi.Input[str]:
        """
        The Id of the UsagePlan resource representing the usage plan containing the UsagePlanKey resource representing a plan customer.
        """
        return pulumi.get(self, "usage_plan_id")

    @usage_plan_id.setter
    def usage_plan_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "usage_plan_id", value)


class UsagePlanKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_id: Optional[pulumi.Input[str]] = None,
                 key_type: Optional[pulumi.Input['UsagePlanKeyKeyType']] = None,
                 usage_plan_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The ``AWS::ApiGateway::UsagePlanKey`` resource associates an API key with a usage plan. This association determines which users the usage plan is applied to.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_id: The Id of the UsagePlanKey resource.
        :param pulumi.Input['UsagePlanKeyKeyType'] key_type: The type of a UsagePlanKey resource for a plan customer.
        :param pulumi.Input[str] usage_plan_id: The Id of the UsagePlan resource representing the usage plan containing the UsagePlanKey resource representing a plan customer.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UsagePlanKeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ``AWS::ApiGateway::UsagePlanKey`` resource associates an API key with a usage plan. This association determines which users the usage plan is applied to.

        :param str resource_name: The name of the resource.
        :param UsagePlanKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UsagePlanKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_id: Optional[pulumi.Input[str]] = None,
                 key_type: Optional[pulumi.Input['UsagePlanKeyKeyType']] = None,
                 usage_plan_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UsagePlanKeyArgs.__new__(UsagePlanKeyArgs)

            if key_id is None and not opts.urn:
                raise TypeError("Missing required property 'key_id'")
            __props__.__dict__["key_id"] = key_id
            if key_type is None and not opts.urn:
                raise TypeError("Missing required property 'key_type'")
            __props__.__dict__["key_type"] = key_type
            if usage_plan_id is None and not opts.urn:
                raise TypeError("Missing required property 'usage_plan_id'")
            __props__.__dict__["usage_plan_id"] = usage_plan_id
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["key_id", "key_type", "usage_plan_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(UsagePlanKey, __self__).__init__(
            'aws-native:apigateway:UsagePlanKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'UsagePlanKey':
        """
        Get an existing UsagePlanKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = UsagePlanKeyArgs.__new__(UsagePlanKeyArgs)

        __props__.__dict__["key_id"] = None
        __props__.__dict__["key_type"] = None
        __props__.__dict__["usage_plan_id"] = None
        return UsagePlanKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> pulumi.Output[str]:
        """
        The Id of the UsagePlanKey resource.
        """
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> pulumi.Output['UsagePlanKeyKeyType']:
        """
        The type of a UsagePlanKey resource for a plan customer.
        """
        return pulumi.get(self, "key_type")

    @property
    @pulumi.getter(name="usagePlanId")
    def usage_plan_id(self) -> pulumi.Output[str]:
        """
        The Id of the UsagePlan resource representing the usage plan containing the UsagePlanKey resource representing a plan customer.
        """
        return pulumi.get(self, "usage_plan_id")

