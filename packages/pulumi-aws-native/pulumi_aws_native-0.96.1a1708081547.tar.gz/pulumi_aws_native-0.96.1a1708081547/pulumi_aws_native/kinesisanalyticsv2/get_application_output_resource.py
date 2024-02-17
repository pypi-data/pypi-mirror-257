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
    'GetApplicationOutputResourceResult',
    'AwaitableGetApplicationOutputResourceResult',
    'get_application_output_resource',
    'get_application_output_resource_output',
]

@pulumi.output_type
class GetApplicationOutputResourceResult:
    def __init__(__self__, id=None, output=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if output and not isinstance(output, dict):
            raise TypeError("Expected argument 'output' to be a dict")
        pulumi.set(__self__, "output", output)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def output(self) -> Optional['outputs.ApplicationOutputResourceOutput']:
        return pulumi.get(self, "output")


class AwaitableGetApplicationOutputResourceResult(GetApplicationOutputResourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationOutputResourceResult(
            id=self.id,
            output=self.output)


def get_application_output_resource(id: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationOutputResourceResult:
    """
    Resource Type definition for AWS::KinesisAnalyticsV2::ApplicationOutput
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:kinesisanalyticsv2:getApplicationOutputResource', __args__, opts=opts, typ=GetApplicationOutputResourceResult).value

    return AwaitableGetApplicationOutputResourceResult(
        id=pulumi.get(__ret__, 'id'),
        output=pulumi.get(__ret__, 'output'))


@_utilities.lift_output_func(get_application_output_resource)
def get_application_output_resource_output(id: Optional[pulumi.Input[str]] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApplicationOutputResourceResult]:
    """
    Resource Type definition for AWS::KinesisAnalyticsV2::ApplicationOutput
    """
    ...
