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
from ._inputs import *

__all__ = ['EnvironmentArgs', 'Environment']

@pulumi.input_type
class EnvironmentArgs:
    def __init__(__self__, *,
                 application_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 monitors: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentMonitorArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentTagArgs']]]] = None):
        """
        The set of arguments for constructing a Environment resource.
        :param pulumi.Input[str] application_id: The application ID.
        :param pulumi.Input[str] description: A description of the environment.
        :param pulumi.Input[Sequence[pulumi.Input['EnvironmentMonitorArgs']]] monitors: Amazon CloudWatch alarms to monitor during the deployment process.
        :param pulumi.Input[str] name: A name for the environment.
        :param pulumi.Input[Sequence[pulumi.Input['EnvironmentTagArgs']]] tags: Metadata to assign to the environment. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.
        """
        pulumi.set(__self__, "application_id", application_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if monitors is not None:
            pulumi.set(__self__, "monitors", monitors)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Input[str]:
        """
        The application ID.
        """
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the environment.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def monitors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentMonitorArgs']]]]:
        """
        Amazon CloudWatch alarms to monitor during the deployment process.
        """
        return pulumi.get(self, "monitors")

    @monitors.setter
    def monitors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentMonitorArgs']]]]):
        pulumi.set(self, "monitors", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the environment.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentTagArgs']]]]:
        """
        Metadata to assign to the environment. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Environment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 monitors: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentMonitorArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::AppConfig::Environment

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_id: The application ID.
        :param pulumi.Input[str] description: A description of the environment.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentMonitorArgs']]]] monitors: Amazon CloudWatch alarms to monitor during the deployment process.
        :param pulumi.Input[str] name: A name for the environment.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentTagArgs']]]] tags: Metadata to assign to the environment. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnvironmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::AppConfig::Environment

        :param str resource_name: The name of the resource.
        :param EnvironmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnvironmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 monitors: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentMonitorArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EnvironmentArgs.__new__(EnvironmentArgs)

            if application_id is None and not opts.urn:
                raise TypeError("Missing required property 'application_id'")
            __props__.__dict__["application_id"] = application_id
            __props__.__dict__["description"] = description
            __props__.__dict__["monitors"] = monitors
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["environment_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["application_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Environment, __self__).__init__(
            'aws-native:appconfig:Environment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Environment':
        """
        Get an existing Environment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EnvironmentArgs.__new__(EnvironmentArgs)

        __props__.__dict__["application_id"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["environment_id"] = None
        __props__.__dict__["monitors"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["tags"] = None
        return Environment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Output[str]:
        """
        The application ID.
        """
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the environment.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> pulumi.Output[str]:
        """
        The environment ID.
        """
        return pulumi.get(self, "environment_id")

    @property
    @pulumi.getter
    def monitors(self) -> pulumi.Output[Optional[Sequence['outputs.EnvironmentMonitor']]]:
        """
        Amazon CloudWatch alarms to monitor during the deployment process.
        """
        return pulumi.get(self, "monitors")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A name for the environment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.EnvironmentTag']]]:
        """
        Metadata to assign to the environment. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.
        """
        return pulumi.get(self, "tags")

