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
    'GetLiveSourceResult',
    'AwaitableGetLiveSourceResult',
    'get_live_source',
    'get_live_source_output',
]

@pulumi.output_type
class GetLiveSourceResult:
    def __init__(__self__, arn=None, http_package_configurations=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if http_package_configurations and not isinstance(http_package_configurations, list):
            raise TypeError("Expected argument 'http_package_configurations' to be a list")
        pulumi.set(__self__, "http_package_configurations", http_package_configurations)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        <p>The ARN of the live source.</p>
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="httpPackageConfigurations")
    def http_package_configurations(self) -> Optional[Sequence['outputs.LiveSourceHttpPackageConfiguration']]:
        """
        <p>A list of HTTP package configuration parameters for this live source.</p>
        """
        return pulumi.get(self, "http_package_configurations")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.LiveSourceTag']]:
        """
        The tags to assign to the live source.
        """
        return pulumi.get(self, "tags")


class AwaitableGetLiveSourceResult(GetLiveSourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLiveSourceResult(
            arn=self.arn,
            http_package_configurations=self.http_package_configurations,
            tags=self.tags)


def get_live_source(live_source_name: Optional[str] = None,
                    source_location_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLiveSourceResult:
    """
    Definition of AWS::MediaTailor::LiveSource Resource Type
    """
    __args__ = dict()
    __args__['liveSourceName'] = live_source_name
    __args__['sourceLocationName'] = source_location_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:mediatailor:getLiveSource', __args__, opts=opts, typ=GetLiveSourceResult).value

    return AwaitableGetLiveSourceResult(
        arn=pulumi.get(__ret__, 'arn'),
        http_package_configurations=pulumi.get(__ret__, 'http_package_configurations'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_live_source)
def get_live_source_output(live_source_name: Optional[pulumi.Input[str]] = None,
                           source_location_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLiveSourceResult]:
    """
    Definition of AWS::MediaTailor::LiveSource Resource Type
    """
    ...
