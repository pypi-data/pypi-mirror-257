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

__all__ = [
    'GetLinkResult',
    'AwaitableGetLinkResult',
    'get_link',
    'get_link_output',
]

@pulumi.output_type
class GetLinkResult:
    def __init__(__self__, arn=None, label=None, resource_types=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if label and not isinstance(label, str):
            raise TypeError("Expected argument 'label' to be a str")
        pulumi.set(__self__, "label", label)
        if resource_types and not isinstance(resource_types, list):
            raise TypeError("Expected argument 'resource_types' to be a list")
        pulumi.set(__self__, "resource_types", resource_types)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def label(self) -> Optional[str]:
        return pulumi.get(self, "label")

    @property
    @pulumi.getter(name="resourceTypes")
    def resource_types(self) -> Optional[Sequence['LinkResourceType']]:
        return pulumi.get(self, "resource_types")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        """
        Tags to apply to the link
        """
        return pulumi.get(self, "tags")


class AwaitableGetLinkResult(GetLinkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLinkResult(
            arn=self.arn,
            label=self.label,
            resource_types=self.resource_types,
            tags=self.tags)


def get_link(arn: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLinkResult:
    """
    Definition of AWS::Oam::Link Resource Type
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:oam:getLink', __args__, opts=opts, typ=GetLinkResult).value

    return AwaitableGetLinkResult(
        arn=pulumi.get(__ret__, 'arn'),
        label=pulumi.get(__ret__, 'label'),
        resource_types=pulumi.get(__ret__, 'resource_types'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_link)
def get_link_output(arn: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLinkResult]:
    """
    Definition of AWS::Oam::Link Resource Type
    """
    ...
