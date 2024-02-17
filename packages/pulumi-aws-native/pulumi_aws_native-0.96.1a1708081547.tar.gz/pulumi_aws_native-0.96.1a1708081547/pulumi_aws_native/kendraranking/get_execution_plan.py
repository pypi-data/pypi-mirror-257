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
    'GetExecutionPlanResult',
    'AwaitableGetExecutionPlanResult',
    'get_execution_plan',
    'get_execution_plan_output',
]

@pulumi.output_type
class GetExecutionPlanResult:
    def __init__(__self__, arn=None, capacity_units=None, description=None, id=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if capacity_units and not isinstance(capacity_units, dict):
            raise TypeError("Expected argument 'capacity_units' to be a dict")
        pulumi.set(__self__, "capacity_units", capacity_units)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="capacityUnits")
    def capacity_units(self) -> Optional['outputs.ExecutionPlanCapacityUnitsConfiguration']:
        """
        Capacity units
        """
        return pulumi.get(self, "capacity_units")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description for the execution plan
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.ExecutionPlanTag']]:
        """
        Tags for labeling the execution plan
        """
        return pulumi.get(self, "tags")


class AwaitableGetExecutionPlanResult(GetExecutionPlanResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetExecutionPlanResult(
            arn=self.arn,
            capacity_units=self.capacity_units,
            description=self.description,
            id=self.id,
            name=self.name,
            tags=self.tags)


def get_execution_plan(id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetExecutionPlanResult:
    """
    A KendraRanking Rescore execution plan
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:kendraranking:getExecutionPlan', __args__, opts=opts, typ=GetExecutionPlanResult).value

    return AwaitableGetExecutionPlanResult(
        arn=pulumi.get(__ret__, 'arn'),
        capacity_units=pulumi.get(__ret__, 'capacity_units'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_execution_plan)
def get_execution_plan_output(id: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetExecutionPlanResult]:
    """
    A KendraRanking Rescore execution plan
    """
    ...
