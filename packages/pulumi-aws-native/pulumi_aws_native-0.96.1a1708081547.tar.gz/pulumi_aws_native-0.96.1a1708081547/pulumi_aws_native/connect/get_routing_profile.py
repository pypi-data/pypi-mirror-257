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
    'GetRoutingProfileResult',
    'AwaitableGetRoutingProfileResult',
    'get_routing_profile',
    'get_routing_profile_output',
]

@pulumi.output_type
class GetRoutingProfileResult:
    def __init__(__self__, agent_availability_timer=None, default_outbound_queue_arn=None, description=None, instance_arn=None, media_concurrencies=None, name=None, queue_configs=None, routing_profile_arn=None, tags=None):
        if agent_availability_timer and not isinstance(agent_availability_timer, str):
            raise TypeError("Expected argument 'agent_availability_timer' to be a str")
        pulumi.set(__self__, "agent_availability_timer", agent_availability_timer)
        if default_outbound_queue_arn and not isinstance(default_outbound_queue_arn, str):
            raise TypeError("Expected argument 'default_outbound_queue_arn' to be a str")
        pulumi.set(__self__, "default_outbound_queue_arn", default_outbound_queue_arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if instance_arn and not isinstance(instance_arn, str):
            raise TypeError("Expected argument 'instance_arn' to be a str")
        pulumi.set(__self__, "instance_arn", instance_arn)
        if media_concurrencies and not isinstance(media_concurrencies, list):
            raise TypeError("Expected argument 'media_concurrencies' to be a list")
        pulumi.set(__self__, "media_concurrencies", media_concurrencies)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if queue_configs and not isinstance(queue_configs, list):
            raise TypeError("Expected argument 'queue_configs' to be a list")
        pulumi.set(__self__, "queue_configs", queue_configs)
        if routing_profile_arn and not isinstance(routing_profile_arn, str):
            raise TypeError("Expected argument 'routing_profile_arn' to be a str")
        pulumi.set(__self__, "routing_profile_arn", routing_profile_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="agentAvailabilityTimer")
    def agent_availability_timer(self) -> Optional['RoutingProfileAgentAvailabilityTimer']:
        """
        Whether agents with this routing profile will have their routing order calculated based on longest idle time or time since their last inbound contact.
        """
        return pulumi.get(self, "agent_availability_timer")

    @property
    @pulumi.getter(name="defaultOutboundQueueArn")
    def default_outbound_queue_arn(self) -> Optional[str]:
        """
        The identifier of the default outbound queue for this routing profile.
        """
        return pulumi.get(self, "default_outbound_queue_arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the routing profile.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> Optional[str]:
        """
        The identifier of the Amazon Connect instance.
        """
        return pulumi.get(self, "instance_arn")

    @property
    @pulumi.getter(name="mediaConcurrencies")
    def media_concurrencies(self) -> Optional[Sequence['outputs.RoutingProfileMediaConcurrency']]:
        """
        The channels agents can handle in the Contact Control Panel (CCP) for this routing profile.
        """
        return pulumi.get(self, "media_concurrencies")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the routing profile.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="queueConfigs")
    def queue_configs(self) -> Optional[Sequence['outputs.RoutingProfileQueueConfig']]:
        """
        The queues to associate with this routing profile.
        """
        return pulumi.get(self, "queue_configs")

    @property
    @pulumi.getter(name="routingProfileArn")
    def routing_profile_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the routing profile.
        """
        return pulumi.get(self, "routing_profile_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.RoutingProfileTag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetRoutingProfileResult(GetRoutingProfileResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRoutingProfileResult(
            agent_availability_timer=self.agent_availability_timer,
            default_outbound_queue_arn=self.default_outbound_queue_arn,
            description=self.description,
            instance_arn=self.instance_arn,
            media_concurrencies=self.media_concurrencies,
            name=self.name,
            queue_configs=self.queue_configs,
            routing_profile_arn=self.routing_profile_arn,
            tags=self.tags)


def get_routing_profile(routing_profile_arn: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRoutingProfileResult:
    """
    Resource Type definition for AWS::Connect::RoutingProfile


    :param str routing_profile_arn: The Amazon Resource Name (ARN) of the routing profile.
    """
    __args__ = dict()
    __args__['routingProfileArn'] = routing_profile_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:connect:getRoutingProfile', __args__, opts=opts, typ=GetRoutingProfileResult).value

    return AwaitableGetRoutingProfileResult(
        agent_availability_timer=pulumi.get(__ret__, 'agent_availability_timer'),
        default_outbound_queue_arn=pulumi.get(__ret__, 'default_outbound_queue_arn'),
        description=pulumi.get(__ret__, 'description'),
        instance_arn=pulumi.get(__ret__, 'instance_arn'),
        media_concurrencies=pulumi.get(__ret__, 'media_concurrencies'),
        name=pulumi.get(__ret__, 'name'),
        queue_configs=pulumi.get(__ret__, 'queue_configs'),
        routing_profile_arn=pulumi.get(__ret__, 'routing_profile_arn'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_routing_profile)
def get_routing_profile_output(routing_profile_arn: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRoutingProfileResult]:
    """
    Resource Type definition for AWS::Connect::RoutingProfile


    :param str routing_profile_arn: The Amazon Resource Name (ARN) of the routing profile.
    """
    ...
