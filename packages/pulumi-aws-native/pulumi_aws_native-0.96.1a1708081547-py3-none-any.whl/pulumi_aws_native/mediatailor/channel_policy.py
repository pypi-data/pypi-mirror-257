# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ChannelPolicyArgs', 'ChannelPolicy']

@pulumi.input_type
class ChannelPolicyArgs:
    def __init__(__self__, *,
                 channel_name: pulumi.Input[str],
                 policy: Any):
        """
        The set of arguments for constructing a ChannelPolicy resource.
        :param Any policy: <p>The IAM policy for the channel. IAM policies are used to control access to your channel.</p>
        """
        pulumi.set(__self__, "channel_name", channel_name)
        pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter(name="channelName")
    def channel_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "channel_name")

    @channel_name.setter
    def channel_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "channel_name", value)

    @property
    @pulumi.getter
    def policy(self) -> Any:
        """
        <p>The IAM policy for the channel. IAM policies are used to control access to your channel.</p>
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Any):
        pulumi.set(self, "policy", value)


class ChannelPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 channel_name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[Any] = None,
                 __props__=None):
        """
        Definition of AWS::MediaTailor::ChannelPolicy Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param Any policy: <p>The IAM policy for the channel. IAM policies are used to control access to your channel.</p>
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ChannelPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::MediaTailor::ChannelPolicy Resource Type

        :param str resource_name: The name of the resource.
        :param ChannelPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ChannelPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 channel_name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[Any] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ChannelPolicyArgs.__new__(ChannelPolicyArgs)

            if channel_name is None and not opts.urn:
                raise TypeError("Missing required property 'channel_name'")
            __props__.__dict__["channel_name"] = channel_name
            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["channel_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ChannelPolicy, __self__).__init__(
            'aws-native:mediatailor:ChannelPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ChannelPolicy':
        """
        Get an existing ChannelPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ChannelPolicyArgs.__new__(ChannelPolicyArgs)

        __props__.__dict__["channel_name"] = None
        __props__.__dict__["policy"] = None
        return ChannelPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="channelName")
    def channel_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "channel_name")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[Any]:
        """
        <p>The IAM policy for the channel. IAM policies are used to control access to your channel.</p>
        """
        return pulumi.get(self, "policy")

