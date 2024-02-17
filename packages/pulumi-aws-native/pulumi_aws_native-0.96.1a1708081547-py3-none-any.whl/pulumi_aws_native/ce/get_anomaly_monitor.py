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
    'GetAnomalyMonitorResult',
    'AwaitableGetAnomalyMonitorResult',
    'get_anomaly_monitor',
    'get_anomaly_monitor_output',
]

@pulumi.output_type
class GetAnomalyMonitorResult:
    def __init__(__self__, creation_date=None, dimensional_value_count=None, last_evaluated_date=None, last_updated_date=None, monitor_arn=None, monitor_name=None):
        if creation_date and not isinstance(creation_date, str):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, "creation_date", creation_date)
        if dimensional_value_count and not isinstance(dimensional_value_count, int):
            raise TypeError("Expected argument 'dimensional_value_count' to be a int")
        pulumi.set(__self__, "dimensional_value_count", dimensional_value_count)
        if last_evaluated_date and not isinstance(last_evaluated_date, str):
            raise TypeError("Expected argument 'last_evaluated_date' to be a str")
        pulumi.set(__self__, "last_evaluated_date", last_evaluated_date)
        if last_updated_date and not isinstance(last_updated_date, str):
            raise TypeError("Expected argument 'last_updated_date' to be a str")
        pulumi.set(__self__, "last_updated_date", last_updated_date)
        if monitor_arn and not isinstance(monitor_arn, str):
            raise TypeError("Expected argument 'monitor_arn' to be a str")
        pulumi.set(__self__, "monitor_arn", monitor_arn)
        if monitor_name and not isinstance(monitor_name, str):
            raise TypeError("Expected argument 'monitor_name' to be a str")
        pulumi.set(__self__, "monitor_name", monitor_name)

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> Optional[str]:
        """
        The date when the monitor was created. 
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="dimensionalValueCount")
    def dimensional_value_count(self) -> Optional[int]:
        """
        The value for evaluated dimensions.
        """
        return pulumi.get(self, "dimensional_value_count")

    @property
    @pulumi.getter(name="lastEvaluatedDate")
    def last_evaluated_date(self) -> Optional[str]:
        """
        The date when the monitor last evaluated for anomalies.
        """
        return pulumi.get(self, "last_evaluated_date")

    @property
    @pulumi.getter(name="lastUpdatedDate")
    def last_updated_date(self) -> Optional[str]:
        """
        The date when the monitor was last updated.
        """
        return pulumi.get(self, "last_updated_date")

    @property
    @pulumi.getter(name="monitorArn")
    def monitor_arn(self) -> Optional[str]:
        return pulumi.get(self, "monitor_arn")

    @property
    @pulumi.getter(name="monitorName")
    def monitor_name(self) -> Optional[str]:
        """
        The name of the monitor.
        """
        return pulumi.get(self, "monitor_name")


class AwaitableGetAnomalyMonitorResult(GetAnomalyMonitorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAnomalyMonitorResult(
            creation_date=self.creation_date,
            dimensional_value_count=self.dimensional_value_count,
            last_evaluated_date=self.last_evaluated_date,
            last_updated_date=self.last_updated_date,
            monitor_arn=self.monitor_arn,
            monitor_name=self.monitor_name)


def get_anomaly_monitor(monitor_arn: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAnomalyMonitorResult:
    """
    AWS Cost Anomaly Detection leverages advanced Machine Learning technologies to identify anomalous spend and root causes, so you can quickly take action. You can use Cost Anomaly Detection by creating monitor.
    """
    __args__ = dict()
    __args__['monitorArn'] = monitor_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ce:getAnomalyMonitor', __args__, opts=opts, typ=GetAnomalyMonitorResult).value

    return AwaitableGetAnomalyMonitorResult(
        creation_date=pulumi.get(__ret__, 'creation_date'),
        dimensional_value_count=pulumi.get(__ret__, 'dimensional_value_count'),
        last_evaluated_date=pulumi.get(__ret__, 'last_evaluated_date'),
        last_updated_date=pulumi.get(__ret__, 'last_updated_date'),
        monitor_arn=pulumi.get(__ret__, 'monitor_arn'),
        monitor_name=pulumi.get(__ret__, 'monitor_name'))


@_utilities.lift_output_func(get_anomaly_monitor)
def get_anomaly_monitor_output(monitor_arn: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAnomalyMonitorResult]:
    """
    AWS Cost Anomaly Detection leverages advanced Machine Learning technologies to identify anomalous spend and root causes, so you can quickly take action. You can use Cost Anomaly Detection by creating monitor.
    """
    ...
