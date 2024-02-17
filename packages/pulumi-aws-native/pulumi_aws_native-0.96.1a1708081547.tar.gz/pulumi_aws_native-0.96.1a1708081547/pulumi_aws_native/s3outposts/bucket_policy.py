# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BucketPolicyArgs', 'BucketPolicy']

@pulumi.input_type
class BucketPolicyArgs:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 policy_document: Any):
        """
        The set of arguments for constructing a BucketPolicy resource.
        :param pulumi.Input[str] bucket: The Amazon Resource Name (ARN) of the specified bucket.
        :param Any policy_document: A policy document containing permissions to add to the specified bucket.
        """
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "policy_document", policy_document)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the specified bucket.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Any:
        """
        A policy document containing permissions to add to the specified bucket.
        """
        return pulumi.get(self, "policy_document")

    @policy_document.setter
    def policy_document(self, value: Any):
        pulumi.set(self, "policy_document", value)


class BucketPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 policy_document: Optional[Any] = None,
                 __props__=None):
        """
        Resource Type Definition for AWS::S3Outposts::BucketPolicy

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The Amazon Resource Name (ARN) of the specified bucket.
        :param Any policy_document: A policy document containing permissions to add to the specified bucket.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type Definition for AWS::S3Outposts::BucketPolicy

        :param str resource_name: The name of the resource.
        :param BucketPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 policy_document: Optional[Any] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketPolicyArgs.__new__(BucketPolicyArgs)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            if policy_document is None and not opts.urn:
                raise TypeError("Missing required property 'policy_document'")
            __props__.__dict__["policy_document"] = policy_document
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["bucket"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(BucketPolicy, __self__).__init__(
            'aws-native:s3outposts:BucketPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BucketPolicy':
        """
        Get an existing BucketPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BucketPolicyArgs.__new__(BucketPolicyArgs)

        __props__.__dict__["bucket"] = None
        __props__.__dict__["policy_document"] = None
        return BucketPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the specified bucket.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> pulumi.Output[Any]:
        """
        A policy document containing permissions to add to the specified bucket.
        """
        return pulumi.get(self, "policy_document")

