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
    'GetSinkResult',
    'AwaitableGetSinkResult',
    'get_sink',
    'get_sink_output',
]

@pulumi.output_type
class GetSinkResult:
    def __init__(__self__, arn=None, policy=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if policy and not isinstance(policy, dict):
            raise TypeError("Expected argument 'policy' to be a dict")
        pulumi.set(__self__, "policy", policy)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon resource name (ARN) of the ObservabilityAccessManager Sink
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def policy(self) -> Optional[Any]:
        """
        The policy of this ObservabilityAccessManager Sink.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        """
        Tags to apply to the sink
        """
        return pulumi.get(self, "tags")


class AwaitableGetSinkResult(GetSinkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSinkResult(
            arn=self.arn,
            policy=self.policy,
            tags=self.tags)


def get_sink(arn: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSinkResult:
    """
    Resource Type definition for AWS::Oam::Sink


    :param str arn: The Amazon resource name (ARN) of the ObservabilityAccessManager Sink
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:oam:getSink', __args__, opts=opts, typ=GetSinkResult).value

    return AwaitableGetSinkResult(
        arn=pulumi.get(__ret__, 'arn'),
        policy=pulumi.get(__ret__, 'policy'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_sink)
def get_sink_output(arn: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSinkResult]:
    """
    Resource Type definition for AWS::Oam::Sink


    :param str arn: The Amazon resource name (ARN) of the ObservabilityAccessManager Sink
    """
    ...
