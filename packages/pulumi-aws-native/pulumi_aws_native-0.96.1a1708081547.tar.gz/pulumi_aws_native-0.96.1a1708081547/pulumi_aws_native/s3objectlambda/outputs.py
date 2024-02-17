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
    'AccessPointAlias',
    'AccessPointAwsLambda',
    'AccessPointObjectLambdaConfiguration',
    'AccessPointPolicyStatus',
    'AccessPointPublicAccessBlockConfiguration',
    'AccessPointTransformationConfiguration',
    'AccessPointTransformationConfigurationContentTransformationProperties',
]

@pulumi.output_type
class AccessPointAlias(dict):
    def __init__(__self__, *,
                 value: str,
                 status: Optional[str] = None):
        """
        :param str value: The value of the Object Lambda alias.
        :param str status: The status of the Object Lambda alias.
        """
        pulumi.set(__self__, "value", value)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the Object Lambda alias.
        """
        return pulumi.get(self, "value")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the Object Lambda alias.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class AccessPointAwsLambda(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "functionArn":
            suggest = "function_arn"
        elif key == "functionPayload":
            suggest = "function_payload"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessPointAwsLambda. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessPointAwsLambda.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessPointAwsLambda.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 function_arn: str,
                 function_payload: Optional[str] = None):
        pulumi.set(__self__, "function_arn", function_arn)
        if function_payload is not None:
            pulumi.set(__self__, "function_payload", function_payload)

    @property
    @pulumi.getter(name="functionArn")
    def function_arn(self) -> str:
        return pulumi.get(self, "function_arn")

    @property
    @pulumi.getter(name="functionPayload")
    def function_payload(self) -> Optional[str]:
        return pulumi.get(self, "function_payload")


@pulumi.output_type
class AccessPointObjectLambdaConfiguration(dict):
    """
    Configuration to be applied to this Object lambda Access Point. It specifies Supporting Access Point, Transformation Configurations. Customers can also set if they like to enable Cloudwatch metrics for accesses to this Object lambda Access Point. Default setting for Cloudwatch metrics is disable.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "supportingAccessPoint":
            suggest = "supporting_access_point"
        elif key == "transformationConfigurations":
            suggest = "transformation_configurations"
        elif key == "allowedFeatures":
            suggest = "allowed_features"
        elif key == "cloudWatchMetricsEnabled":
            suggest = "cloud_watch_metrics_enabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessPointObjectLambdaConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessPointObjectLambdaConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessPointObjectLambdaConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 supporting_access_point: str,
                 transformation_configurations: Sequence['outputs.AccessPointTransformationConfiguration'],
                 allowed_features: Optional[Sequence[str]] = None,
                 cloud_watch_metrics_enabled: Optional[bool] = None):
        """
        Configuration to be applied to this Object lambda Access Point. It specifies Supporting Access Point, Transformation Configurations. Customers can also set if they like to enable Cloudwatch metrics for accesses to this Object lambda Access Point. Default setting for Cloudwatch metrics is disable.
        """
        pulumi.set(__self__, "supporting_access_point", supporting_access_point)
        pulumi.set(__self__, "transformation_configurations", transformation_configurations)
        if allowed_features is not None:
            pulumi.set(__self__, "allowed_features", allowed_features)
        if cloud_watch_metrics_enabled is not None:
            pulumi.set(__self__, "cloud_watch_metrics_enabled", cloud_watch_metrics_enabled)

    @property
    @pulumi.getter(name="supportingAccessPoint")
    def supporting_access_point(self) -> str:
        return pulumi.get(self, "supporting_access_point")

    @property
    @pulumi.getter(name="transformationConfigurations")
    def transformation_configurations(self) -> Sequence['outputs.AccessPointTransformationConfiguration']:
        return pulumi.get(self, "transformation_configurations")

    @property
    @pulumi.getter(name="allowedFeatures")
    def allowed_features(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "allowed_features")

    @property
    @pulumi.getter(name="cloudWatchMetricsEnabled")
    def cloud_watch_metrics_enabled(self) -> Optional[bool]:
        return pulumi.get(self, "cloud_watch_metrics_enabled")


@pulumi.output_type
class AccessPointPolicyStatus(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "isPublic":
            suggest = "is_public"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessPointPolicyStatus. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessPointPolicyStatus.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessPointPolicyStatus.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 is_public: Optional[bool] = None):
        """
        :param bool is_public: Specifies whether the Object lambda Access Point Policy is Public or not. Object lambda Access Points are private by default.
        """
        if is_public is not None:
            pulumi.set(__self__, "is_public", is_public)

    @property
    @pulumi.getter(name="isPublic")
    def is_public(self) -> Optional[bool]:
        """
        Specifies whether the Object lambda Access Point Policy is Public or not. Object lambda Access Points are private by default.
        """
        return pulumi.get(self, "is_public")


@pulumi.output_type
class AccessPointPublicAccessBlockConfiguration(dict):
    """
    The Public Access Block Configuration is used to block policies that would allow public access to this Object lambda Access Point. All public access to Object lambda Access Points are blocked by default, and any policy that would give public access to them will be also blocked. This behavior cannot be changed for Object lambda Access Points.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "blockPublicAcls":
            suggest = "block_public_acls"
        elif key == "blockPublicPolicy":
            suggest = "block_public_policy"
        elif key == "ignorePublicAcls":
            suggest = "ignore_public_acls"
        elif key == "restrictPublicBuckets":
            suggest = "restrict_public_buckets"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessPointPublicAccessBlockConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessPointPublicAccessBlockConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessPointPublicAccessBlockConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 block_public_acls: Optional[bool] = None,
                 block_public_policy: Optional[bool] = None,
                 ignore_public_acls: Optional[bool] = None,
                 restrict_public_buckets: Optional[bool] = None):
        """
        The Public Access Block Configuration is used to block policies that would allow public access to this Object lambda Access Point. All public access to Object lambda Access Points are blocked by default, and any policy that would give public access to them will be also blocked. This behavior cannot be changed for Object lambda Access Points.
        :param bool block_public_acls: Specifies whether Amazon S3 should block public access control lists (ACLs) to this object lambda access point. Setting this element to TRUE causes the following behavior:
               - PUT Bucket acl and PUT Object acl calls fail if the specified ACL is public.
                - PUT Object calls fail if the request includes a public ACL.
               . - PUT Bucket calls fail if the request includes a public ACL.
               Enabling this setting doesn't affect existing policies or ACLs.
        :param bool block_public_policy: Specifies whether Amazon S3 should block public bucket policies for buckets in this account. Setting this element to TRUE causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access. Enabling this setting doesn't affect existing bucket policies.
        :param bool ignore_public_acls: Specifies whether Amazon S3 should ignore public ACLs for buckets in this account. Setting this element to TRUE causes Amazon S3 to ignore all public ACLs on buckets in this account and any objects that they contain. Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.
        :param bool restrict_public_buckets: Specifies whether Amazon S3 should restrict public bucket policies for this bucket. Setting this element to TRUE restricts access to this bucket to only AWS services and authorized users within this account if the bucket has a public policy.
               Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.
        """
        if block_public_acls is not None:
            pulumi.set(__self__, "block_public_acls", block_public_acls)
        if block_public_policy is not None:
            pulumi.set(__self__, "block_public_policy", block_public_policy)
        if ignore_public_acls is not None:
            pulumi.set(__self__, "ignore_public_acls", ignore_public_acls)
        if restrict_public_buckets is not None:
            pulumi.set(__self__, "restrict_public_buckets", restrict_public_buckets)

    @property
    @pulumi.getter(name="blockPublicAcls")
    def block_public_acls(self) -> Optional[bool]:
        """
        Specifies whether Amazon S3 should block public access control lists (ACLs) to this object lambda access point. Setting this element to TRUE causes the following behavior:
        - PUT Bucket acl and PUT Object acl calls fail if the specified ACL is public.
         - PUT Object calls fail if the request includes a public ACL.
        . - PUT Bucket calls fail if the request includes a public ACL.
        Enabling this setting doesn't affect existing policies or ACLs.
        """
        return pulumi.get(self, "block_public_acls")

    @property
    @pulumi.getter(name="blockPublicPolicy")
    def block_public_policy(self) -> Optional[bool]:
        """
        Specifies whether Amazon S3 should block public bucket policies for buckets in this account. Setting this element to TRUE causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access. Enabling this setting doesn't affect existing bucket policies.
        """
        return pulumi.get(self, "block_public_policy")

    @property
    @pulumi.getter(name="ignorePublicAcls")
    def ignore_public_acls(self) -> Optional[bool]:
        """
        Specifies whether Amazon S3 should ignore public ACLs for buckets in this account. Setting this element to TRUE causes Amazon S3 to ignore all public ACLs on buckets in this account and any objects that they contain. Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.
        """
        return pulumi.get(self, "ignore_public_acls")

    @property
    @pulumi.getter(name="restrictPublicBuckets")
    def restrict_public_buckets(self) -> Optional[bool]:
        """
        Specifies whether Amazon S3 should restrict public bucket policies for this bucket. Setting this element to TRUE restricts access to this bucket to only AWS services and authorized users within this account if the bucket has a public policy.
        Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.
        """
        return pulumi.get(self, "restrict_public_buckets")


@pulumi.output_type
class AccessPointTransformationConfiguration(dict):
    """
    Configuration to define what content transformation will be applied on which S3 Action.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "contentTransformation":
            suggest = "content_transformation"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessPointTransformationConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessPointTransformationConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessPointTransformationConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 actions: Sequence[str],
                 content_transformation: 'outputs.AccessPointTransformationConfigurationContentTransformationProperties'):
        """
        Configuration to define what content transformation will be applied on which S3 Action.
        """
        pulumi.set(__self__, "actions", actions)
        pulumi.set(__self__, "content_transformation", content_transformation)

    @property
    @pulumi.getter
    def actions(self) -> Sequence[str]:
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter(name="contentTransformation")
    def content_transformation(self) -> 'outputs.AccessPointTransformationConfigurationContentTransformationProperties':
        return pulumi.get(self, "content_transformation")


@pulumi.output_type
class AccessPointTransformationConfigurationContentTransformationProperties(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "awsLambda":
            suggest = "aws_lambda"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessPointTransformationConfigurationContentTransformationProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessPointTransformationConfigurationContentTransformationProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessPointTransformationConfigurationContentTransformationProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 aws_lambda: 'outputs.AccessPointAwsLambda'):
        pulumi.set(__self__, "aws_lambda", aws_lambda)

    @property
    @pulumi.getter(name="awsLambda")
    def aws_lambda(self) -> 'outputs.AccessPointAwsLambda':
        return pulumi.get(self, "aws_lambda")


