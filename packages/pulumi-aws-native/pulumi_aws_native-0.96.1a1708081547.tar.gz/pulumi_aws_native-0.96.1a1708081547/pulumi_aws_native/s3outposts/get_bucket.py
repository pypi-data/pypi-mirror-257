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
    'GetBucketResult',
    'AwaitableGetBucketResult',
    'get_bucket',
    'get_bucket_output',
]

@pulumi.output_type
class GetBucketResult:
    def __init__(__self__, arn=None, lifecycle_configuration=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if lifecycle_configuration and not isinstance(lifecycle_configuration, dict):
            raise TypeError("Expected argument 'lifecycle_configuration' to be a dict")
        pulumi.set(__self__, "lifecycle_configuration", lifecycle_configuration)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the specified bucket.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="lifecycleConfiguration")
    def lifecycle_configuration(self) -> Optional['outputs.BucketLifecycleConfiguration']:
        """
        Rules that define how Amazon S3Outposts manages objects during their lifetime.
        """
        return pulumi.get(self, "lifecycle_configuration")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.BucketTag']]:
        """
        An arbitrary set of tags (key-value pairs) for this S3Outposts bucket.
        """
        return pulumi.get(self, "tags")


class AwaitableGetBucketResult(GetBucketResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBucketResult(
            arn=self.arn,
            lifecycle_configuration=self.lifecycle_configuration,
            tags=self.tags)


def get_bucket(arn: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBucketResult:
    """
    Resource Type Definition for AWS::S3Outposts::Bucket


    :param str arn: The Amazon Resource Name (ARN) of the specified bucket.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:s3outposts:getBucket', __args__, opts=opts, typ=GetBucketResult).value

    return AwaitableGetBucketResult(
        arn=pulumi.get(__ret__, 'arn'),
        lifecycle_configuration=pulumi.get(__ret__, 'lifecycle_configuration'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_bucket)
def get_bucket_output(arn: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBucketResult]:
    """
    Resource Type Definition for AWS::S3Outposts::Bucket


    :param str arn: The Amazon Resource Name (ARN) of the specified bucket.
    """
    ...
