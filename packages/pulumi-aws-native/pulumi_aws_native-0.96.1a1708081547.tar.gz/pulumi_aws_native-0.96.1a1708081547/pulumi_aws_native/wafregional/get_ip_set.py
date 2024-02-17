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

__all__ = [
    'GetIpSetResult',
    'AwaitableGetIpSetResult',
    'get_ip_set',
    'get_ip_set_output',
]

@pulumi.output_type
class GetIpSetResult:
    def __init__(__self__, id=None, ip_set_descriptors=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_set_descriptors and not isinstance(ip_set_descriptors, list):
            raise TypeError("Expected argument 'ip_set_descriptors' to be a list")
        pulumi.set(__self__, "ip_set_descriptors", ip_set_descriptors)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipSetDescriptors")
    def ip_set_descriptors(self) -> Optional[Sequence['outputs.IpSetIpSetDescriptor']]:
        return pulumi.get(self, "ip_set_descriptors")


class AwaitableGetIpSetResult(GetIpSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIpSetResult(
            id=self.id,
            ip_set_descriptors=self.ip_set_descriptors)


def get_ip_set(id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIpSetResult:
    """
    Resource Type definition for AWS::WAFRegional::IPSet
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:wafregional:getIpSet', __args__, opts=opts, typ=GetIpSetResult).value

    return AwaitableGetIpSetResult(
        id=pulumi.get(__ret__, 'id'),
        ip_set_descriptors=pulumi.get(__ret__, 'ip_set_descriptors'))


@_utilities.lift_output_func(get_ip_set)
def get_ip_set_output(id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIpSetResult]:
    """
    Resource Type definition for AWS::WAFRegional::IPSet
    """
    ...
