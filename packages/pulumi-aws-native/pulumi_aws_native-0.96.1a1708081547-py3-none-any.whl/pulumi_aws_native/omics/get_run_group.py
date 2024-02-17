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
    'GetRunGroupResult',
    'AwaitableGetRunGroupResult',
    'get_run_group',
    'get_run_group_output',
]

@pulumi.output_type
class GetRunGroupResult:
    def __init__(__self__, arn=None, creation_time=None, id=None, max_cpus=None, max_duration=None, max_gpus=None, max_runs=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if max_cpus and not isinstance(max_cpus, float):
            raise TypeError("Expected argument 'max_cpus' to be a float")
        pulumi.set(__self__, "max_cpus", max_cpus)
        if max_duration and not isinstance(max_duration, float):
            raise TypeError("Expected argument 'max_duration' to be a float")
        pulumi.set(__self__, "max_duration", max_duration)
        if max_gpus and not isinstance(max_gpus, float):
            raise TypeError("Expected argument 'max_gpus' to be a float")
        pulumi.set(__self__, "max_gpus", max_gpus)
        if max_runs and not isinstance(max_runs, float):
            raise TypeError("Expected argument 'max_runs' to be a float")
        pulumi.set(__self__, "max_runs", max_runs)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="maxCpus")
    def max_cpus(self) -> Optional[float]:
        return pulumi.get(self, "max_cpus")

    @property
    @pulumi.getter(name="maxDuration")
    def max_duration(self) -> Optional[float]:
        return pulumi.get(self, "max_duration")

    @property
    @pulumi.getter(name="maxGpus")
    def max_gpus(self) -> Optional[float]:
        return pulumi.get(self, "max_gpus")

    @property
    @pulumi.getter(name="maxRuns")
    def max_runs(self) -> Optional[float]:
        return pulumi.get(self, "max_runs")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional['outputs.RunGroupTagMap']:
        return pulumi.get(self, "tags")


class AwaitableGetRunGroupResult(GetRunGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRunGroupResult(
            arn=self.arn,
            creation_time=self.creation_time,
            id=self.id,
            max_cpus=self.max_cpus,
            max_duration=self.max_duration,
            max_gpus=self.max_gpus,
            max_runs=self.max_runs,
            name=self.name,
            tags=self.tags)


def get_run_group(id: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRunGroupResult:
    """
    Definition of AWS::Omics::RunGroup Resource Type
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:omics:getRunGroup', __args__, opts=opts, typ=GetRunGroupResult).value

    return AwaitableGetRunGroupResult(
        arn=pulumi.get(__ret__, 'arn'),
        creation_time=pulumi.get(__ret__, 'creation_time'),
        id=pulumi.get(__ret__, 'id'),
        max_cpus=pulumi.get(__ret__, 'max_cpus'),
        max_duration=pulumi.get(__ret__, 'max_duration'),
        max_gpus=pulumi.get(__ret__, 'max_gpus'),
        max_runs=pulumi.get(__ret__, 'max_runs'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_run_group)
def get_run_group_output(id: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRunGroupResult]:
    """
    Definition of AWS::Omics::RunGroup Resource Type
    """
    ...
