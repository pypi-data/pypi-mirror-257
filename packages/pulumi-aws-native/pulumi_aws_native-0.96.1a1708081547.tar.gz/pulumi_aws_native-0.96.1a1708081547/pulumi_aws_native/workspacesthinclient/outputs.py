# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'EnvironmentMaintenanceWindow',
    'EnvironmentTag',
]

@pulumi.output_type
class EnvironmentMaintenanceWindow(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "applyTimeOf":
            suggest = "apply_time_of"
        elif key == "daysOfTheWeek":
            suggest = "days_of_the_week"
        elif key == "endTimeHour":
            suggest = "end_time_hour"
        elif key == "endTimeMinute":
            suggest = "end_time_minute"
        elif key == "startTimeHour":
            suggest = "start_time_hour"
        elif key == "startTimeMinute":
            suggest = "start_time_minute"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EnvironmentMaintenanceWindow. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EnvironmentMaintenanceWindow.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EnvironmentMaintenanceWindow.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: 'EnvironmentMaintenanceWindowType',
                 apply_time_of: Optional['EnvironmentMaintenanceWindowApplyTimeOf'] = None,
                 days_of_the_week: Optional[Sequence['EnvironmentDayOfWeek']] = None,
                 end_time_hour: Optional[int] = None,
                 end_time_minute: Optional[int] = None,
                 start_time_hour: Optional[int] = None,
                 start_time_minute: Optional[int] = None):
        """
        :param 'EnvironmentMaintenanceWindowType' type: The type of maintenance window.
        :param 'EnvironmentMaintenanceWindowApplyTimeOf' apply_time_of: The desired time zone maintenance window.
        :param Sequence['EnvironmentDayOfWeek'] days_of_the_week: The date of maintenance window.
        :param int end_time_hour: The hour end time of maintenance window.
        :param int end_time_minute: The minute end time of maintenance window.
        :param int start_time_hour: The hour start time of maintenance window.
        :param int start_time_minute: The minute start time of maintenance window.
        """
        pulumi.set(__self__, "type", type)
        if apply_time_of is not None:
            pulumi.set(__self__, "apply_time_of", apply_time_of)
        if days_of_the_week is not None:
            pulumi.set(__self__, "days_of_the_week", days_of_the_week)
        if end_time_hour is not None:
            pulumi.set(__self__, "end_time_hour", end_time_hour)
        if end_time_minute is not None:
            pulumi.set(__self__, "end_time_minute", end_time_minute)
        if start_time_hour is not None:
            pulumi.set(__self__, "start_time_hour", start_time_hour)
        if start_time_minute is not None:
            pulumi.set(__self__, "start_time_minute", start_time_minute)

    @property
    @pulumi.getter
    def type(self) -> 'EnvironmentMaintenanceWindowType':
        """
        The type of maintenance window.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="applyTimeOf")
    def apply_time_of(self) -> Optional['EnvironmentMaintenanceWindowApplyTimeOf']:
        """
        The desired time zone maintenance window.
        """
        return pulumi.get(self, "apply_time_of")

    @property
    @pulumi.getter(name="daysOfTheWeek")
    def days_of_the_week(self) -> Optional[Sequence['EnvironmentDayOfWeek']]:
        """
        The date of maintenance window.
        """
        return pulumi.get(self, "days_of_the_week")

    @property
    @pulumi.getter(name="endTimeHour")
    def end_time_hour(self) -> Optional[int]:
        """
        The hour end time of maintenance window.
        """
        return pulumi.get(self, "end_time_hour")

    @property
    @pulumi.getter(name="endTimeMinute")
    def end_time_minute(self) -> Optional[int]:
        """
        The minute end time of maintenance window.
        """
        return pulumi.get(self, "end_time_minute")

    @property
    @pulumi.getter(name="startTimeHour")
    def start_time_hour(self) -> Optional[int]:
        """
        The hour start time of maintenance window.
        """
        return pulumi.get(self, "start_time_hour")

    @property
    @pulumi.getter(name="startTimeMinute")
    def start_time_minute(self) -> Optional[int]:
        """
        The minute start time of maintenance window.
        """
        return pulumi.get(self, "start_time_minute")


@pulumi.output_type
class EnvironmentTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param str value: The value for the tag. You can specify a value that is 1 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 1 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")


