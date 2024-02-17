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
    'GetDirectoryBucketResult',
    'AwaitableGetDirectoryBucketResult',
    'get_directory_bucket',
    'get_directory_bucket_output',
]

@pulumi.output_type
class GetDirectoryBucketResult:
    def __init__(__self__, arn=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Returns the Amazon Resource Name (ARN) of the specified bucket.
        """
        return pulumi.get(self, "arn")


class AwaitableGetDirectoryBucketResult(GetDirectoryBucketResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDirectoryBucketResult(
            arn=self.arn)


def get_directory_bucket(bucket_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDirectoryBucketResult:
    """
    Resource Type definition for AWS::S3Express::DirectoryBucket.


    :param str bucket_name: Specifies a name for the bucket. The bucket name must contain only lowercase letters, numbers, and hyphens (-). A directory bucket name must be unique in the chosen Availability Zone. The bucket name must also follow the format 'bucket_base_name--az_id--x-s3' (for example, 'DOC-EXAMPLE-BUCKET--usw2-az1--x-s3'). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the bucket name.
    """
    __args__ = dict()
    __args__['bucketName'] = bucket_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:s3express:getDirectoryBucket', __args__, opts=opts, typ=GetDirectoryBucketResult).value

    return AwaitableGetDirectoryBucketResult(
        arn=pulumi.get(__ret__, 'arn'))


@_utilities.lift_output_func(get_directory_bucket)
def get_directory_bucket_output(bucket_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDirectoryBucketResult]:
    """
    Resource Type definition for AWS::S3Express::DirectoryBucket.


    :param str bucket_name: Specifies a name for the bucket. The bucket name must contain only lowercase letters, numbers, and hyphens (-). A directory bucket name must be unique in the chosen Availability Zone. The bucket name must also follow the format 'bucket_base_name--az_id--x-s3' (for example, 'DOC-EXAMPLE-BUCKET--usw2-az1--x-s3'). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the bucket name.
    """
    ...
