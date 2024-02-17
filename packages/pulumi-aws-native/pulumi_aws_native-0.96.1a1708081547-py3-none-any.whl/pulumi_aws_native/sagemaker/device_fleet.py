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

__all__ = ['DeviceFleetArgs', 'DeviceFleet']

@pulumi.input_type
class DeviceFleetArgs:
    def __init__(__self__, *,
                 output_config: pulumi.Input['DeviceFleetEdgeOutputConfigArgs'],
                 role_arn: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 device_fleet_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['DeviceFleetTagArgs']]]] = None):
        """
        The set of arguments for constructing a DeviceFleet resource.
        :param pulumi.Input['DeviceFleetEdgeOutputConfigArgs'] output_config: S3 bucket and an ecryption key id (if available) to store outputs for the fleet
        :param pulumi.Input[str] role_arn: Role associated with the device fleet
        :param pulumi.Input[str] description: Description for the edge device fleet
        :param pulumi.Input[str] device_fleet_name: The name of the edge device fleet
        :param pulumi.Input[Sequence[pulumi.Input['DeviceFleetTagArgs']]] tags: Associate tags with the resource
        """
        pulumi.set(__self__, "output_config", output_config)
        pulumi.set(__self__, "role_arn", role_arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if device_fleet_name is not None:
            pulumi.set(__self__, "device_fleet_name", device_fleet_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="outputConfig")
    def output_config(self) -> pulumi.Input['DeviceFleetEdgeOutputConfigArgs']:
        """
        S3 bucket and an ecryption key id (if available) to store outputs for the fleet
        """
        return pulumi.get(self, "output_config")

    @output_config.setter
    def output_config(self, value: pulumi.Input['DeviceFleetEdgeOutputConfigArgs']):
        pulumi.set(self, "output_config", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        Role associated with the device fleet
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description for the edge device fleet
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="deviceFleetName")
    def device_fleet_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the edge device fleet
        """
        return pulumi.get(self, "device_fleet_name")

    @device_fleet_name.setter
    def device_fleet_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "device_fleet_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DeviceFleetTagArgs']]]]:
        """
        Associate tags with the resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DeviceFleetTagArgs']]]]):
        pulumi.set(self, "tags", value)


class DeviceFleet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 device_fleet_name: Optional[pulumi.Input[str]] = None,
                 output_config: Optional[pulumi.Input[pulumi.InputType['DeviceFleetEdgeOutputConfigArgs']]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeviceFleetTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource schema for AWS::SageMaker::DeviceFleet

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description for the edge device fleet
        :param pulumi.Input[str] device_fleet_name: The name of the edge device fleet
        :param pulumi.Input[pulumi.InputType['DeviceFleetEdgeOutputConfigArgs']] output_config: S3 bucket and an ecryption key id (if available) to store outputs for the fleet
        :param pulumi.Input[str] role_arn: Role associated with the device fleet
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeviceFleetTagArgs']]]] tags: Associate tags with the resource
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DeviceFleetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::SageMaker::DeviceFleet

        :param str resource_name: The name of the resource.
        :param DeviceFleetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeviceFleetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 device_fleet_name: Optional[pulumi.Input[str]] = None,
                 output_config: Optional[pulumi.Input[pulumi.InputType['DeviceFleetEdgeOutputConfigArgs']]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeviceFleetTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DeviceFleetArgs.__new__(DeviceFleetArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["device_fleet_name"] = device_fleet_name
            if output_config is None and not opts.urn:
                raise TypeError("Missing required property 'output_config'")
            __props__.__dict__["output_config"] = output_config
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["tags"] = tags
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["device_fleet_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(DeviceFleet, __self__).__init__(
            'aws-native:sagemaker:DeviceFleet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DeviceFleet':
        """
        Get an existing DeviceFleet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DeviceFleetArgs.__new__(DeviceFleetArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["device_fleet_name"] = None
        __props__.__dict__["output_config"] = None
        __props__.__dict__["role_arn"] = None
        __props__.__dict__["tags"] = None
        return DeviceFleet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description for the edge device fleet
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="deviceFleetName")
    def device_fleet_name(self) -> pulumi.Output[str]:
        """
        The name of the edge device fleet
        """
        return pulumi.get(self, "device_fleet_name")

    @property
    @pulumi.getter(name="outputConfig")
    def output_config(self) -> pulumi.Output['outputs.DeviceFleetEdgeOutputConfig']:
        """
        S3 bucket and an ecryption key id (if available) to store outputs for the fleet
        """
        return pulumi.get(self, "output_config")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        Role associated with the device fleet
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.DeviceFleetTag']]]:
        """
        Associate tags with the resource
        """
        return pulumi.get(self, "tags")

