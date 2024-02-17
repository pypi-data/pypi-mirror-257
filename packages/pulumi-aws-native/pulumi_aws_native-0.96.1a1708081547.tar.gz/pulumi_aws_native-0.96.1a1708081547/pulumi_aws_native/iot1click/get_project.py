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
    'GetProjectResult',
    'AwaitableGetProjectResult',
    'get_project',
    'get_project_output',
]

@pulumi.output_type
class GetProjectResult:
    def __init__(__self__, arn=None, description=None, id=None, placement_template=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if placement_template and not isinstance(placement_template, dict):
            raise TypeError("Expected argument 'placement_template' to be a dict")
        pulumi.set(__self__, "placement_template", placement_template)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="placementTemplate")
    def placement_template(self) -> Optional['outputs.ProjectPlacementTemplate']:
        return pulumi.get(self, "placement_template")


class AwaitableGetProjectResult(GetProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectResult(
            arn=self.arn,
            description=self.description,
            id=self.id,
            placement_template=self.placement_template)


def get_project(id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectResult:
    """
    Resource Type definition for AWS::IoT1Click::Project
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iot1click:getProject', __args__, opts=opts, typ=GetProjectResult).value

    return AwaitableGetProjectResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        placement_template=pulumi.get(__ret__, 'placement_template'))


@_utilities.lift_output_func(get_project)
def get_project_output(id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProjectResult]:
    """
    Resource Type definition for AWS::IoT1Click::Project
    """
    ...
