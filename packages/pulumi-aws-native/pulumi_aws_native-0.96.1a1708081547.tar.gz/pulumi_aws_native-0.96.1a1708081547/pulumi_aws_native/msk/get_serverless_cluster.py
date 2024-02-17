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
    'GetServerlessClusterResult',
    'AwaitableGetServerlessClusterResult',
    'get_serverless_cluster',
    'get_serverless_cluster_output',
]

@pulumi.output_type
class GetServerlessClusterResult:
    def __init__(__self__, arn=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")


class AwaitableGetServerlessClusterResult(GetServerlessClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServerlessClusterResult(
            arn=self.arn)


def get_serverless_cluster(arn: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServerlessClusterResult:
    """
    Resource Type definition for AWS::MSK::ServerlessCluster
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:msk:getServerlessCluster', __args__, opts=opts, typ=GetServerlessClusterResult).value

    return AwaitableGetServerlessClusterResult(
        arn=pulumi.get(__ret__, 'arn'))


@_utilities.lift_output_func(get_serverless_cluster)
def get_serverless_cluster_output(arn: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServerlessClusterResult]:
    """
    Resource Type definition for AWS::MSK::ServerlessCluster
    """
    ...
