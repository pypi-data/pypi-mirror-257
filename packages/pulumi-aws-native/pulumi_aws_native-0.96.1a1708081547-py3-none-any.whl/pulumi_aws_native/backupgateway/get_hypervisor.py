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
    'GetHypervisorResult',
    'AwaitableGetHypervisorResult',
    'get_hypervisor',
    'get_hypervisor_output',
]

@pulumi.output_type
class GetHypervisorResult:
    def __init__(__self__, host=None, hypervisor_arn=None):
        if host and not isinstance(host, str):
            raise TypeError("Expected argument 'host' to be a str")
        pulumi.set(__self__, "host", host)
        if hypervisor_arn and not isinstance(hypervisor_arn, str):
            raise TypeError("Expected argument 'hypervisor_arn' to be a str")
        pulumi.set(__self__, "hypervisor_arn", hypervisor_arn)

    @property
    @pulumi.getter
    def host(self) -> Optional[str]:
        return pulumi.get(self, "host")

    @property
    @pulumi.getter(name="hypervisorArn")
    def hypervisor_arn(self) -> Optional[str]:
        return pulumi.get(self, "hypervisor_arn")


class AwaitableGetHypervisorResult(GetHypervisorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHypervisorResult(
            host=self.host,
            hypervisor_arn=self.hypervisor_arn)


def get_hypervisor(hypervisor_arn: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHypervisorResult:
    """
    Definition of AWS::BackupGateway::Hypervisor Resource Type
    """
    __args__ = dict()
    __args__['hypervisorArn'] = hypervisor_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:backupgateway:getHypervisor', __args__, opts=opts, typ=GetHypervisorResult).value

    return AwaitableGetHypervisorResult(
        host=pulumi.get(__ret__, 'host'),
        hypervisor_arn=pulumi.get(__ret__, 'hypervisor_arn'))


@_utilities.lift_output_func(get_hypervisor)
def get_hypervisor_output(hypervisor_arn: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHypervisorResult]:
    """
    Definition of AWS::BackupGateway::Hypervisor Resource Type
    """
    ...
