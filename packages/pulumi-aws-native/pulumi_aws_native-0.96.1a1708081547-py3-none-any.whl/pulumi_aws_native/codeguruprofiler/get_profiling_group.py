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
    'GetProfilingGroupResult',
    'AwaitableGetProfilingGroupResult',
    'get_profiling_group',
    'get_profiling_group_output',
]

@pulumi.output_type
class GetProfilingGroupResult:
    def __init__(__self__, agent_permissions=None, anomaly_detection_notification_configuration=None, arn=None, tags=None):
        if agent_permissions and not isinstance(agent_permissions, dict):
            raise TypeError("Expected argument 'agent_permissions' to be a dict")
        pulumi.set(__self__, "agent_permissions", agent_permissions)
        if anomaly_detection_notification_configuration and not isinstance(anomaly_detection_notification_configuration, list):
            raise TypeError("Expected argument 'anomaly_detection_notification_configuration' to be a list")
        pulumi.set(__self__, "anomaly_detection_notification_configuration", anomaly_detection_notification_configuration)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="agentPermissions")
    def agent_permissions(self) -> Optional['outputs.AgentPermissionsProperties']:
        """
        The agent permissions attached to this profiling group.
        """
        return pulumi.get(self, "agent_permissions")

    @property
    @pulumi.getter(name="anomalyDetectionNotificationConfiguration")
    def anomaly_detection_notification_configuration(self) -> Optional[Sequence['outputs.ProfilingGroupChannel']]:
        """
        Configuration for Notification Channels for Anomaly Detection feature in CodeGuru Profiler which enables customers to detect anomalies in the application profile for those methods that represent the highest proportion of CPU time or latency
        """
        return pulumi.get(self, "anomaly_detection_notification_configuration")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the specified profiling group.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.ProfilingGroupTag']]:
        """
        The tags associated with a profiling group.
        """
        return pulumi.get(self, "tags")


class AwaitableGetProfilingGroupResult(GetProfilingGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProfilingGroupResult(
            agent_permissions=self.agent_permissions,
            anomaly_detection_notification_configuration=self.anomaly_detection_notification_configuration,
            arn=self.arn,
            tags=self.tags)


def get_profiling_group(profiling_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProfilingGroupResult:
    """
    This resource schema represents the Profiling Group resource in the Amazon CodeGuru Profiler service.


    :param str profiling_group_name: The name of the profiling group.
    """
    __args__ = dict()
    __args__['profilingGroupName'] = profiling_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:codeguruprofiler:getProfilingGroup', __args__, opts=opts, typ=GetProfilingGroupResult).value

    return AwaitableGetProfilingGroupResult(
        agent_permissions=pulumi.get(__ret__, 'agent_permissions'),
        anomaly_detection_notification_configuration=pulumi.get(__ret__, 'anomaly_detection_notification_configuration'),
        arn=pulumi.get(__ret__, 'arn'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_profiling_group)
def get_profiling_group_output(profiling_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProfilingGroupResult]:
    """
    This resource schema represents the Profiling Group resource in the Amazon CodeGuru Profiler service.


    :param str profiling_group_name: The name of the profiling group.
    """
    ...
