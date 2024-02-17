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

__all__ = ['EventBusArgs', 'EventBus']

@pulumi.input_type
class EventBusArgs:
    def __init__(__self__, *,
                 event_source_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[Any] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['EventBusTagArgs']]]] = None):
        """
        The set of arguments for constructing a EventBus resource.
        :param pulumi.Input[str] event_source_name: If you are creating a partner event bus, this specifies the partner event source that the new event bus will be matched with.
        :param pulumi.Input[str] name: The name of the event bus.
        :param Any policy: A JSON string that describes the permission policy statement for the event bus.
        :param pulumi.Input[Sequence[pulumi.Input['EventBusTagArgs']]] tags: Any tags assigned to the event bus.
        """
        if event_source_name is not None:
            pulumi.set(__self__, "event_source_name", event_source_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="eventSourceName")
    def event_source_name(self) -> Optional[pulumi.Input[str]]:
        """
        If you are creating a partner event bus, this specifies the partner event source that the new event bus will be matched with.
        """
        return pulumi.get(self, "event_source_name")

    @event_source_name.setter
    def event_source_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_source_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the event bus.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[Any]:
        """
        A JSON string that describes the permission policy statement for the event bus.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[Any]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EventBusTagArgs']]]]:
        """
        Any tags assigned to the event bus.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EventBusTagArgs']]]]):
        pulumi.set(self, "tags", value)


class EventBus(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 event_source_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[Any] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EventBusTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource type definition for AWS::Events::EventBus

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] event_source_name: If you are creating a partner event bus, this specifies the partner event source that the new event bus will be matched with.
        :param pulumi.Input[str] name: The name of the event bus.
        :param Any policy: A JSON string that describes the permission policy statement for the event bus.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EventBusTagArgs']]]] tags: Any tags assigned to the event bus.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[EventBusArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource type definition for AWS::Events::EventBus

        :param str resource_name: The name of the resource.
        :param EventBusArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EventBusArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 event_source_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[Any] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EventBusTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EventBusArgs.__new__(EventBusArgs)

            __props__.__dict__["event_source_name"] = event_source_name
            __props__.__dict__["name"] = name
            __props__.__dict__["policy"] = policy
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(EventBus, __self__).__init__(
            'aws-native:events:EventBus',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'EventBus':
        """
        Get an existing EventBus resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EventBusArgs.__new__(EventBusArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["event_source_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["policy"] = None
        __props__.__dict__["tags"] = None
        return EventBus(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) for the event bus.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="eventSourceName")
    def event_source_name(self) -> pulumi.Output[Optional[str]]:
        """
        If you are creating a partner event bus, this specifies the partner event source that the new event bus will be matched with.
        """
        return pulumi.get(self, "event_source_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the event bus.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[Optional[Any]]:
        """
        A JSON string that describes the permission policy statement for the event bus.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.EventBusTag']]]:
        """
        Any tags assigned to the event bus.
        """
        return pulumi.get(self, "tags")

