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
    'GetProjectResult',
    'AwaitableGetProjectResult',
    'get_project',
    'get_project_output',
]

@pulumi.output_type
class GetProjectResult:
    def __init__(__self__, dataset_name=None, recipe_name=None, role_arn=None, sample=None):
        if dataset_name and not isinstance(dataset_name, str):
            raise TypeError("Expected argument 'dataset_name' to be a str")
        pulumi.set(__self__, "dataset_name", dataset_name)
        if recipe_name and not isinstance(recipe_name, str):
            raise TypeError("Expected argument 'recipe_name' to be a str")
        pulumi.set(__self__, "recipe_name", recipe_name)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if sample and not isinstance(sample, dict):
            raise TypeError("Expected argument 'sample' to be a dict")
        pulumi.set(__self__, "sample", sample)

    @property
    @pulumi.getter(name="datasetName")
    def dataset_name(self) -> Optional[str]:
        """
        Dataset name
        """
        return pulumi.get(self, "dataset_name")

    @property
    @pulumi.getter(name="recipeName")
    def recipe_name(self) -> Optional[str]:
        """
        Recipe name
        """
        return pulumi.get(self, "recipe_name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        Role arn
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def sample(self) -> Optional['outputs.ProjectSample']:
        """
        Sample
        """
        return pulumi.get(self, "sample")


class AwaitableGetProjectResult(GetProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectResult(
            dataset_name=self.dataset_name,
            recipe_name=self.recipe_name,
            role_arn=self.role_arn,
            sample=self.sample)


def get_project(name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectResult:
    """
    Resource schema for AWS::DataBrew::Project.


    :param str name: Project name
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:databrew:getProject', __args__, opts=opts, typ=GetProjectResult).value

    return AwaitableGetProjectResult(
        dataset_name=pulumi.get(__ret__, 'dataset_name'),
        recipe_name=pulumi.get(__ret__, 'recipe_name'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        sample=pulumi.get(__ret__, 'sample'))


@_utilities.lift_output_func(get_project)
def get_project_output(name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProjectResult]:
    """
    Resource schema for AWS::DataBrew::Project.


    :param str name: Project name
    """
    ...
