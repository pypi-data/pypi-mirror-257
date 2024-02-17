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

__all__ = ['QueueArgs', 'Queue']

@pulumi.input_type
class QueueArgs:
    def __init__(__self__, *,
                 hours_of_operation_arn: pulumi.Input[str],
                 instance_arn: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 max_contacts: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 outbound_caller_config: Optional[pulumi.Input['QueueOutboundCallerConfigArgs']] = None,
                 quick_connect_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input['QueueStatus']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['QueueTagArgs']]]] = None):
        """
        The set of arguments for constructing a Queue resource.
        :param pulumi.Input[str] hours_of_operation_arn: The identifier for the hours of operation.
        :param pulumi.Input[str] instance_arn: The identifier of the Amazon Connect instance.
        :param pulumi.Input[str] description: The description of the queue.
        :param pulumi.Input[int] max_contacts: The maximum number of contacts that can be in the queue before it is considered full.
        :param pulumi.Input[str] name: The name of the queue.
        :param pulumi.Input['QueueOutboundCallerConfigArgs'] outbound_caller_config: The outbound caller ID name, number, and outbound whisper flow.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] quick_connect_arns: The quick connects available to agents who are working the queue.
        :param pulumi.Input['QueueStatus'] status: The status of the queue.
        :param pulumi.Input[Sequence[pulumi.Input['QueueTagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        pulumi.set(__self__, "hours_of_operation_arn", hours_of_operation_arn)
        pulumi.set(__self__, "instance_arn", instance_arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if max_contacts is not None:
            pulumi.set(__self__, "max_contacts", max_contacts)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if outbound_caller_config is not None:
            pulumi.set(__self__, "outbound_caller_config", outbound_caller_config)
        if quick_connect_arns is not None:
            pulumi.set(__self__, "quick_connect_arns", quick_connect_arns)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="hoursOfOperationArn")
    def hours_of_operation_arn(self) -> pulumi.Input[str]:
        """
        The identifier for the hours of operation.
        """
        return pulumi.get(self, "hours_of_operation_arn")

    @hours_of_operation_arn.setter
    def hours_of_operation_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "hours_of_operation_arn", value)

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Input[str]:
        """
        The identifier of the Amazon Connect instance.
        """
        return pulumi.get(self, "instance_arn")

    @instance_arn.setter
    def instance_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the queue.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="maxContacts")
    def max_contacts(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of contacts that can be in the queue before it is considered full.
        """
        return pulumi.get(self, "max_contacts")

    @max_contacts.setter
    def max_contacts(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_contacts", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the queue.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="outboundCallerConfig")
    def outbound_caller_config(self) -> Optional[pulumi.Input['QueueOutboundCallerConfigArgs']]:
        """
        The outbound caller ID name, number, and outbound whisper flow.
        """
        return pulumi.get(self, "outbound_caller_config")

    @outbound_caller_config.setter
    def outbound_caller_config(self, value: Optional[pulumi.Input['QueueOutboundCallerConfigArgs']]):
        pulumi.set(self, "outbound_caller_config", value)

    @property
    @pulumi.getter(name="quickConnectArns")
    def quick_connect_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The quick connects available to agents who are working the queue.
        """
        return pulumi.get(self, "quick_connect_arns")

    @quick_connect_arns.setter
    def quick_connect_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "quick_connect_arns", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input['QueueStatus']]:
        """
        The status of the queue.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input['QueueStatus']]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['QueueTagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['QueueTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Queue(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 hours_of_operation_arn: Optional[pulumi.Input[str]] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 max_contacts: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 outbound_caller_config: Optional[pulumi.Input[pulumi.InputType['QueueOutboundCallerConfigArgs']]] = None,
                 quick_connect_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input['QueueStatus']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QueueTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Connect::Queue

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the queue.
        :param pulumi.Input[str] hours_of_operation_arn: The identifier for the hours of operation.
        :param pulumi.Input[str] instance_arn: The identifier of the Amazon Connect instance.
        :param pulumi.Input[int] max_contacts: The maximum number of contacts that can be in the queue before it is considered full.
        :param pulumi.Input[str] name: The name of the queue.
        :param pulumi.Input[pulumi.InputType['QueueOutboundCallerConfigArgs']] outbound_caller_config: The outbound caller ID name, number, and outbound whisper flow.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] quick_connect_arns: The quick connects available to agents who are working the queue.
        :param pulumi.Input['QueueStatus'] status: The status of the queue.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QueueTagArgs']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: QueueArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Connect::Queue

        :param str resource_name: The name of the resource.
        :param QueueArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(QueueArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 hours_of_operation_arn: Optional[pulumi.Input[str]] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 max_contacts: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 outbound_caller_config: Optional[pulumi.Input[pulumi.InputType['QueueOutboundCallerConfigArgs']]] = None,
                 quick_connect_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input['QueueStatus']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QueueTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = QueueArgs.__new__(QueueArgs)

            __props__.__dict__["description"] = description
            if hours_of_operation_arn is None and not opts.urn:
                raise TypeError("Missing required property 'hours_of_operation_arn'")
            __props__.__dict__["hours_of_operation_arn"] = hours_of_operation_arn
            if instance_arn is None and not opts.urn:
                raise TypeError("Missing required property 'instance_arn'")
            __props__.__dict__["instance_arn"] = instance_arn
            __props__.__dict__["max_contacts"] = max_contacts
            __props__.__dict__["name"] = name
            __props__.__dict__["outbound_caller_config"] = outbound_caller_config
            __props__.__dict__["quick_connect_arns"] = quick_connect_arns
            __props__.__dict__["status"] = status
            __props__.__dict__["tags"] = tags
            __props__.__dict__["queue_arn"] = None
            __props__.__dict__["type"] = None
        super(Queue, __self__).__init__(
            'aws-native:connect:Queue',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Queue':
        """
        Get an existing Queue resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = QueueArgs.__new__(QueueArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["hours_of_operation_arn"] = None
        __props__.__dict__["instance_arn"] = None
        __props__.__dict__["max_contacts"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["outbound_caller_config"] = None
        __props__.__dict__["queue_arn"] = None
        __props__.__dict__["quick_connect_arns"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return Queue(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the queue.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="hoursOfOperationArn")
    def hours_of_operation_arn(self) -> pulumi.Output[str]:
        """
        The identifier for the hours of operation.
        """
        return pulumi.get(self, "hours_of_operation_arn")

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Output[str]:
        """
        The identifier of the Amazon Connect instance.
        """
        return pulumi.get(self, "instance_arn")

    @property
    @pulumi.getter(name="maxContacts")
    def max_contacts(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum number of contacts that can be in the queue before it is considered full.
        """
        return pulumi.get(self, "max_contacts")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the queue.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outboundCallerConfig")
    def outbound_caller_config(self) -> pulumi.Output[Optional['outputs.QueueOutboundCallerConfig']]:
        """
        The outbound caller ID name, number, and outbound whisper flow.
        """
        return pulumi.get(self, "outbound_caller_config")

    @property
    @pulumi.getter(name="queueArn")
    def queue_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) for the queue.
        """
        return pulumi.get(self, "queue_arn")

    @property
    @pulumi.getter(name="quickConnectArns")
    def quick_connect_arns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The quick connects available to agents who are working the queue.
        """
        return pulumi.get(self, "quick_connect_arns")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional['QueueStatus']]:
        """
        The status of the queue.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.QueueTag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output['QueueType']:
        """
        The type of queue.
        """
        return pulumi.get(self, "type")

