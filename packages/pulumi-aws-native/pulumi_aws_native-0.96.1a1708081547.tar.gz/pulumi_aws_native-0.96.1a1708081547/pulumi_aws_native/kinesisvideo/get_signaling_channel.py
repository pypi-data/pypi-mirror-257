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
    'GetSignalingChannelResult',
    'AwaitableGetSignalingChannelResult',
    'get_signaling_channel',
    'get_signaling_channel_output',
]

@pulumi.output_type
class GetSignalingChannelResult:
    def __init__(__self__, arn=None, message_ttl_seconds=None, tags=None, type=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if message_ttl_seconds and not isinstance(message_ttl_seconds, int):
            raise TypeError("Expected argument 'message_ttl_seconds' to be a int")
        pulumi.set(__self__, "message_ttl_seconds", message_ttl_seconds)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the Kinesis Video Signaling Channel.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="messageTtlSeconds")
    def message_ttl_seconds(self) -> Optional[int]:
        """
        The period of time a signaling channel retains undelivered messages before they are discarded.
        """
        return pulumi.get(self, "message_ttl_seconds")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.SignalingChannelTag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional['SignalingChannelType']:
        """
        The type of the Kinesis Video Signaling Channel to create. Currently, SINGLE_MASTER is the only supported channel type.
        """
        return pulumi.get(self, "type")


class AwaitableGetSignalingChannelResult(GetSignalingChannelResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSignalingChannelResult(
            arn=self.arn,
            message_ttl_seconds=self.message_ttl_seconds,
            tags=self.tags,
            type=self.type)


def get_signaling_channel(name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSignalingChannelResult:
    """
    Resource Type Definition for AWS::KinesisVideo::SignalingChannel


    :param str name: The name of the Kinesis Video Signaling Channel.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:kinesisvideo:getSignalingChannel', __args__, opts=opts, typ=GetSignalingChannelResult).value

    return AwaitableGetSignalingChannelResult(
        arn=pulumi.get(__ret__, 'arn'),
        message_ttl_seconds=pulumi.get(__ret__, 'message_ttl_seconds'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'))


@_utilities.lift_output_func(get_signaling_channel)
def get_signaling_channel_output(name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSignalingChannelResult]:
    """
    Resource Type Definition for AWS::KinesisVideo::SignalingChannel


    :param str name: The name of the Kinesis Video Signaling Channel.
    """
    ...
