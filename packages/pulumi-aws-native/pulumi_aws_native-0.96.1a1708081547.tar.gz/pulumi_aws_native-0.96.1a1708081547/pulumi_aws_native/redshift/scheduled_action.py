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
from ._inputs import *

__all__ = ['ScheduledActionArgs', 'ScheduledAction']

@pulumi.input_type
class ScheduledActionArgs:
    def __init__(__self__, *,
                 enable: Optional[pulumi.Input[bool]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 iam_role: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 scheduled_action_description: Optional[pulumi.Input[str]] = None,
                 scheduled_action_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 target_action: Optional[pulumi.Input['ScheduledActionTypeArgs']] = None):
        """
        The set of arguments for constructing a ScheduledAction resource.
        :param pulumi.Input[bool] enable: If true, the schedule is enabled. If false, the scheduled action does not trigger.
        :param pulumi.Input[str] end_time: The end time in UTC of the scheduled action. After this time, the scheduled action does not trigger.
        :param pulumi.Input[str] iam_role: The IAM role to assume to run the target action.
        :param pulumi.Input[str] schedule: The schedule in `at( )` or `cron( )` format.
        :param pulumi.Input[str] scheduled_action_description: The description of the scheduled action.
        :param pulumi.Input[str] scheduled_action_name: The name of the scheduled action. The name must be unique within an account.
        :param pulumi.Input[str] start_time: The start time in UTC of the scheduled action. Before this time, the scheduled action does not trigger.
        :param pulumi.Input['ScheduledActionTypeArgs'] target_action: A JSON format string of the Amazon Redshift API operation with input parameters.
        """
        if enable is not None:
            pulumi.set(__self__, "enable", enable)
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if iam_role is not None:
            pulumi.set(__self__, "iam_role", iam_role)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)
        if scheduled_action_description is not None:
            pulumi.set(__self__, "scheduled_action_description", scheduled_action_description)
        if scheduled_action_name is not None:
            pulumi.set(__self__, "scheduled_action_name", scheduled_action_name)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)
        if target_action is not None:
            pulumi.set(__self__, "target_action", target_action)

    @property
    @pulumi.getter
    def enable(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, the schedule is enabled. If false, the scheduled action does not trigger.
        """
        return pulumi.get(self, "enable")

    @enable.setter
    def enable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable", value)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[pulumi.Input[str]]:
        """
        The end time in UTC of the scheduled action. After this time, the scheduled action does not trigger.
        """
        return pulumi.get(self, "end_time")

    @end_time.setter
    def end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_time", value)

    @property
    @pulumi.getter(name="iamRole")
    def iam_role(self) -> Optional[pulumi.Input[str]]:
        """
        The IAM role to assume to run the target action.
        """
        return pulumi.get(self, "iam_role")

    @iam_role.setter
    def iam_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "iam_role", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input[str]]:
        """
        The schedule in `at( )` or `cron( )` format.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter(name="scheduledActionDescription")
    def scheduled_action_description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the scheduled action.
        """
        return pulumi.get(self, "scheduled_action_description")

    @scheduled_action_description.setter
    def scheduled_action_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scheduled_action_description", value)

    @property
    @pulumi.getter(name="scheduledActionName")
    def scheduled_action_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the scheduled action. The name must be unique within an account.
        """
        return pulumi.get(self, "scheduled_action_name")

    @scheduled_action_name.setter
    def scheduled_action_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scheduled_action_name", value)

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[pulumi.Input[str]]:
        """
        The start time in UTC of the scheduled action. Before this time, the scheduled action does not trigger.
        """
        return pulumi.get(self, "start_time")

    @start_time.setter
    def start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_time", value)

    @property
    @pulumi.getter(name="targetAction")
    def target_action(self) -> Optional[pulumi.Input['ScheduledActionTypeArgs']]:
        """
        A JSON format string of the Amazon Redshift API operation with input parameters.
        """
        return pulumi.get(self, "target_action")

    @target_action.setter
    def target_action(self, value: Optional[pulumi.Input['ScheduledActionTypeArgs']]):
        pulumi.set(self, "target_action", value)


class ScheduledAction(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enable: Optional[pulumi.Input[bool]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 iam_role: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 scheduled_action_description: Optional[pulumi.Input[str]] = None,
                 scheduled_action_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 target_action: Optional[pulumi.Input[pulumi.InputType['ScheduledActionTypeArgs']]] = None,
                 __props__=None):
        """
        The `AWS::Redshift::ScheduledAction` resource creates an Amazon Redshift Scheduled Action.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enable: If true, the schedule is enabled. If false, the scheduled action does not trigger.
        :param pulumi.Input[str] end_time: The end time in UTC of the scheduled action. After this time, the scheduled action does not trigger.
        :param pulumi.Input[str] iam_role: The IAM role to assume to run the target action.
        :param pulumi.Input[str] schedule: The schedule in `at( )` or `cron( )` format.
        :param pulumi.Input[str] scheduled_action_description: The description of the scheduled action.
        :param pulumi.Input[str] scheduled_action_name: The name of the scheduled action. The name must be unique within an account.
        :param pulumi.Input[str] start_time: The start time in UTC of the scheduled action. Before this time, the scheduled action does not trigger.
        :param pulumi.Input[pulumi.InputType['ScheduledActionTypeArgs']] target_action: A JSON format string of the Amazon Redshift API operation with input parameters.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ScheduledActionArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The `AWS::Redshift::ScheduledAction` resource creates an Amazon Redshift Scheduled Action.

        :param str resource_name: The name of the resource.
        :param ScheduledActionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ScheduledActionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enable: Optional[pulumi.Input[bool]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 iam_role: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 scheduled_action_description: Optional[pulumi.Input[str]] = None,
                 scheduled_action_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 target_action: Optional[pulumi.Input[pulumi.InputType['ScheduledActionTypeArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ScheduledActionArgs.__new__(ScheduledActionArgs)

            __props__.__dict__["enable"] = enable
            __props__.__dict__["end_time"] = end_time
            __props__.__dict__["iam_role"] = iam_role
            __props__.__dict__["schedule"] = schedule
            __props__.__dict__["scheduled_action_description"] = scheduled_action_description
            __props__.__dict__["scheduled_action_name"] = scheduled_action_name
            __props__.__dict__["start_time"] = start_time
            __props__.__dict__["target_action"] = target_action
            __props__.__dict__["next_invocations"] = None
            __props__.__dict__["state"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["scheduled_action_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ScheduledAction, __self__).__init__(
            'aws-native:redshift:ScheduledAction',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ScheduledAction':
        """
        Get an existing ScheduledAction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ScheduledActionArgs.__new__(ScheduledActionArgs)

        __props__.__dict__["enable"] = None
        __props__.__dict__["end_time"] = None
        __props__.__dict__["iam_role"] = None
        __props__.__dict__["next_invocations"] = None
        __props__.__dict__["schedule"] = None
        __props__.__dict__["scheduled_action_description"] = None
        __props__.__dict__["scheduled_action_name"] = None
        __props__.__dict__["start_time"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["target_action"] = None
        return ScheduledAction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def enable(self) -> pulumi.Output[Optional[bool]]:
        """
        If true, the schedule is enabled. If false, the scheduled action does not trigger.
        """
        return pulumi.get(self, "enable")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[Optional[str]]:
        """
        The end time in UTC of the scheduled action. After this time, the scheduled action does not trigger.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="iamRole")
    def iam_role(self) -> pulumi.Output[Optional[str]]:
        """
        The IAM role to assume to run the target action.
        """
        return pulumi.get(self, "iam_role")

    @property
    @pulumi.getter(name="nextInvocations")
    def next_invocations(self) -> pulumi.Output[Sequence[str]]:
        """
        List of times when the scheduled action will run.
        """
        return pulumi.get(self, "next_invocations")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output[Optional[str]]:
        """
        The schedule in `at( )` or `cron( )` format.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter(name="scheduledActionDescription")
    def scheduled_action_description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the scheduled action.
        """
        return pulumi.get(self, "scheduled_action_description")

    @property
    @pulumi.getter(name="scheduledActionName")
    def scheduled_action_name(self) -> pulumi.Output[str]:
        """
        The name of the scheduled action. The name must be unique within an account.
        """
        return pulumi.get(self, "scheduled_action_name")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[Optional[str]]:
        """
        The start time in UTC of the scheduled action. Before this time, the scheduled action does not trigger.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output['ScheduledActionState']:
        """
        The state of the scheduled action.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="targetAction")
    def target_action(self) -> pulumi.Output[Optional['outputs.ScheduledActionType']]:
        """
        A JSON format string of the Amazon Redshift API operation with input parameters.
        """
        return pulumi.get(self, "target_action")

