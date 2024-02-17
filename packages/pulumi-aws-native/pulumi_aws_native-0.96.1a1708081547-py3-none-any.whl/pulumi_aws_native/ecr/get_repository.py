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
    'GetRepositoryResult',
    'AwaitableGetRepositoryResult',
    'get_repository',
    'get_repository_output',
]

@pulumi.output_type
class GetRepositoryResult:
    def __init__(__self__, arn=None, image_scanning_configuration=None, image_tag_mutability=None, lifecycle_policy=None, repository_policy_text=None, repository_uri=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if image_scanning_configuration and not isinstance(image_scanning_configuration, dict):
            raise TypeError("Expected argument 'image_scanning_configuration' to be a dict")
        pulumi.set(__self__, "image_scanning_configuration", image_scanning_configuration)
        if image_tag_mutability and not isinstance(image_tag_mutability, str):
            raise TypeError("Expected argument 'image_tag_mutability' to be a str")
        pulumi.set(__self__, "image_tag_mutability", image_tag_mutability)
        if lifecycle_policy and not isinstance(lifecycle_policy, dict):
            raise TypeError("Expected argument 'lifecycle_policy' to be a dict")
        pulumi.set(__self__, "lifecycle_policy", lifecycle_policy)
        if repository_policy_text and not isinstance(repository_policy_text, dict):
            raise TypeError("Expected argument 'repository_policy_text' to be a dict")
        pulumi.set(__self__, "repository_policy_text", repository_policy_text)
        if repository_uri and not isinstance(repository_uri, str):
            raise TypeError("Expected argument 'repository_uri' to be a str")
        pulumi.set(__self__, "repository_uri", repository_uri)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="imageScanningConfiguration")
    def image_scanning_configuration(self) -> Optional['outputs.RepositoryImageScanningConfiguration']:
        return pulumi.get(self, "image_scanning_configuration")

    @property
    @pulumi.getter(name="imageTagMutability")
    def image_tag_mutability(self) -> Optional['RepositoryImageTagMutability']:
        """
        The image tag mutability setting for the repository.
        """
        return pulumi.get(self, "image_tag_mutability")

    @property
    @pulumi.getter(name="lifecyclePolicy")
    def lifecycle_policy(self) -> Optional['outputs.RepositoryLifecyclePolicy']:
        return pulumi.get(self, "lifecycle_policy")

    @property
    @pulumi.getter(name="repositoryPolicyText")
    def repository_policy_text(self) -> Optional[Any]:
        """
        The JSON repository policy text to apply to the repository. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/RepositoryPolicyExamples.html in the Amazon Elastic Container Registry User Guide. 
        """
        return pulumi.get(self, "repository_policy_text")

    @property
    @pulumi.getter(name="repositoryUri")
    def repository_uri(self) -> Optional[str]:
        return pulumi.get(self, "repository_uri")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.RepositoryTag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetRepositoryResult(GetRepositoryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRepositoryResult(
            arn=self.arn,
            image_scanning_configuration=self.image_scanning_configuration,
            image_tag_mutability=self.image_tag_mutability,
            lifecycle_policy=self.lifecycle_policy,
            repository_policy_text=self.repository_policy_text,
            repository_uri=self.repository_uri,
            tags=self.tags)


def get_repository(repository_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRepositoryResult:
    """
    The AWS::ECR::Repository resource specifies an Amazon Elastic Container Registry (Amazon ECR) repository, where users can push and pull Docker images. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html


    :param str repository_name: The name to use for the repository. The repository name may be specified on its own (such as nginx-web-app) or it can be prepended with a namespace to group the repository into a category (such as project-a/nginx-web-app). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the repository name. For more information, see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html.
    """
    __args__ = dict()
    __args__['repositoryName'] = repository_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ecr:getRepository', __args__, opts=opts, typ=GetRepositoryResult).value

    return AwaitableGetRepositoryResult(
        arn=pulumi.get(__ret__, 'arn'),
        image_scanning_configuration=pulumi.get(__ret__, 'image_scanning_configuration'),
        image_tag_mutability=pulumi.get(__ret__, 'image_tag_mutability'),
        lifecycle_policy=pulumi.get(__ret__, 'lifecycle_policy'),
        repository_policy_text=pulumi.get(__ret__, 'repository_policy_text'),
        repository_uri=pulumi.get(__ret__, 'repository_uri'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_repository)
def get_repository_output(repository_name: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRepositoryResult]:
    """
    The AWS::ECR::Repository resource specifies an Amazon Elastic Container Registry (Amazon ECR) repository, where users can push and pull Docker images. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html


    :param str repository_name: The name to use for the repository. The repository name may be specified on its own (such as nginx-web-app) or it can be prepended with a namespace to group the repository into a category (such as project-a/nginx-web-app). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the repository name. For more information, see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html.
    """
    ...
