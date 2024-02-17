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
    'GetTaskDefinitionResult',
    'AwaitableGetTaskDefinitionResult',
    'get_task_definition',
    'get_task_definition_output',
]

@pulumi.output_type
class GetTaskDefinitionResult:
    def __init__(__self__, tags=None, task_definition_arn=None):
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if task_definition_arn and not isinstance(task_definition_arn, str):
            raise TypeError("Expected argument 'task_definition_arn' to be a str")
        pulumi.set(__self__, "task_definition_arn", task_definition_arn)

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.TaskDefinitionTag']]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="taskDefinitionArn")
    def task_definition_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the Amazon ECS task definition
        """
        return pulumi.get(self, "task_definition_arn")


class AwaitableGetTaskDefinitionResult(GetTaskDefinitionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTaskDefinitionResult(
            tags=self.tags,
            task_definition_arn=self.task_definition_arn)


def get_task_definition(task_definition_arn: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTaskDefinitionResult:
    """
    Resource Schema describing various properties for ECS TaskDefinition


    :param str task_definition_arn: The Amazon Resource Name (ARN) of the Amazon ECS task definition
    """
    __args__ = dict()
    __args__['taskDefinitionArn'] = task_definition_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ecs:getTaskDefinition', __args__, opts=opts, typ=GetTaskDefinitionResult).value

    return AwaitableGetTaskDefinitionResult(
        tags=pulumi.get(__ret__, 'tags'),
        task_definition_arn=pulumi.get(__ret__, 'task_definition_arn'))


@_utilities.lift_output_func(get_task_definition)
def get_task_definition_output(task_definition_arn: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTaskDefinitionResult]:
    """
    Resource Schema describing various properties for ECS TaskDefinition


    :param str task_definition_arn: The Amazon Resource Name (ARN) of the Amazon ECS task definition
    """
    ...
