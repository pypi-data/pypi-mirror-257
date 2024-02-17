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

__all__ = ['ComputeEnvironmentArgs', 'ComputeEnvironment']

@pulumi.input_type
class ComputeEnvironmentArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 compute_environment_name: Optional[pulumi.Input[str]] = None,
                 compute_resources: Optional[pulumi.Input['ComputeEnvironmentComputeResourcesArgs']] = None,
                 eks_configuration: Optional[pulumi.Input['ComputeEnvironmentEksConfigurationArgs']] = None,
                 replace_compute_environment: Optional[pulumi.Input[bool]] = None,
                 service_role: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 unmanagedv_cpus: Optional[pulumi.Input[int]] = None,
                 update_policy: Optional[pulumi.Input['ComputeEnvironmentUpdatePolicyArgs']] = None):
        """
        The set of arguments for constructing a ComputeEnvironment resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A key-value pair to associate with a resource.
        """
        pulumi.set(__self__, "type", type)
        if compute_environment_name is not None:
            pulumi.set(__self__, "compute_environment_name", compute_environment_name)
        if compute_resources is not None:
            pulumi.set(__self__, "compute_resources", compute_resources)
        if eks_configuration is not None:
            pulumi.set(__self__, "eks_configuration", eks_configuration)
        if replace_compute_environment is not None:
            pulumi.set(__self__, "replace_compute_environment", replace_compute_environment)
        if service_role is not None:
            pulumi.set(__self__, "service_role", service_role)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if unmanagedv_cpus is not None:
            pulumi.set(__self__, "unmanagedv_cpus", unmanagedv_cpus)
        if update_policy is not None:
            pulumi.set(__self__, "update_policy", update_policy)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="computeEnvironmentName")
    def compute_environment_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "compute_environment_name")

    @compute_environment_name.setter
    def compute_environment_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compute_environment_name", value)

    @property
    @pulumi.getter(name="computeResources")
    def compute_resources(self) -> Optional[pulumi.Input['ComputeEnvironmentComputeResourcesArgs']]:
        return pulumi.get(self, "compute_resources")

    @compute_resources.setter
    def compute_resources(self, value: Optional[pulumi.Input['ComputeEnvironmentComputeResourcesArgs']]):
        pulumi.set(self, "compute_resources", value)

    @property
    @pulumi.getter(name="eksConfiguration")
    def eks_configuration(self) -> Optional[pulumi.Input['ComputeEnvironmentEksConfigurationArgs']]:
        return pulumi.get(self, "eks_configuration")

    @eks_configuration.setter
    def eks_configuration(self, value: Optional[pulumi.Input['ComputeEnvironmentEksConfigurationArgs']]):
        pulumi.set(self, "eks_configuration", value)

    @property
    @pulumi.getter(name="replaceComputeEnvironment")
    def replace_compute_environment(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "replace_compute_environment")

    @replace_compute_environment.setter
    def replace_compute_environment(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "replace_compute_environment", value)

    @property
    @pulumi.getter(name="serviceRole")
    def service_role(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "service_role")

    @service_role.setter
    def service_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_role", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A key-value pair to associate with a resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="unmanagedvCpus")
    def unmanagedv_cpus(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "unmanagedv_cpus")

    @unmanagedv_cpus.setter
    def unmanagedv_cpus(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "unmanagedv_cpus", value)

    @property
    @pulumi.getter(name="updatePolicy")
    def update_policy(self) -> Optional[pulumi.Input['ComputeEnvironmentUpdatePolicyArgs']]:
        return pulumi.get(self, "update_policy")

    @update_policy.setter
    def update_policy(self, value: Optional[pulumi.Input['ComputeEnvironmentUpdatePolicyArgs']]):
        pulumi.set(self, "update_policy", value)


class ComputeEnvironment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compute_environment_name: Optional[pulumi.Input[str]] = None,
                 compute_resources: Optional[pulumi.Input[pulumi.InputType['ComputeEnvironmentComputeResourcesArgs']]] = None,
                 eks_configuration: Optional[pulumi.Input[pulumi.InputType['ComputeEnvironmentEksConfigurationArgs']]] = None,
                 replace_compute_environment: Optional[pulumi.Input[bool]] = None,
                 service_role: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 unmanagedv_cpus: Optional[pulumi.Input[int]] = None,
                 update_policy: Optional[pulumi.Input[pulumi.InputType['ComputeEnvironmentUpdatePolicyArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Batch::ComputeEnvironment

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A key-value pair to associate with a resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ComputeEnvironmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Batch::ComputeEnvironment

        :param str resource_name: The name of the resource.
        :param ComputeEnvironmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ComputeEnvironmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compute_environment_name: Optional[pulumi.Input[str]] = None,
                 compute_resources: Optional[pulumi.Input[pulumi.InputType['ComputeEnvironmentComputeResourcesArgs']]] = None,
                 eks_configuration: Optional[pulumi.Input[pulumi.InputType['ComputeEnvironmentEksConfigurationArgs']]] = None,
                 replace_compute_environment: Optional[pulumi.Input[bool]] = None,
                 service_role: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 unmanagedv_cpus: Optional[pulumi.Input[int]] = None,
                 update_policy: Optional[pulumi.Input[pulumi.InputType['ComputeEnvironmentUpdatePolicyArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ComputeEnvironmentArgs.__new__(ComputeEnvironmentArgs)

            __props__.__dict__["compute_environment_name"] = compute_environment_name
            __props__.__dict__["compute_resources"] = compute_resources
            __props__.__dict__["eks_configuration"] = eks_configuration
            __props__.__dict__["replace_compute_environment"] = replace_compute_environment
            __props__.__dict__["service_role"] = service_role
            __props__.__dict__["state"] = state
            __props__.__dict__["tags"] = tags
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["unmanagedv_cpus"] = unmanagedv_cpus
            __props__.__dict__["update_policy"] = update_policy
            __props__.__dict__["compute_environment_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["compute_environment_name", "compute_resources.spot_iam_fleet_role", "eks_configuration", "tags.*", "type"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ComputeEnvironment, __self__).__init__(
            'aws-native:batch:ComputeEnvironment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ComputeEnvironment':
        """
        Get an existing ComputeEnvironment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ComputeEnvironmentArgs.__new__(ComputeEnvironmentArgs)

        __props__.__dict__["compute_environment_arn"] = None
        __props__.__dict__["compute_environment_name"] = None
        __props__.__dict__["compute_resources"] = None
        __props__.__dict__["eks_configuration"] = None
        __props__.__dict__["replace_compute_environment"] = None
        __props__.__dict__["service_role"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["unmanagedv_cpus"] = None
        __props__.__dict__["update_policy"] = None
        return ComputeEnvironment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="computeEnvironmentArn")
    def compute_environment_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "compute_environment_arn")

    @property
    @pulumi.getter(name="computeEnvironmentName")
    def compute_environment_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "compute_environment_name")

    @property
    @pulumi.getter(name="computeResources")
    def compute_resources(self) -> pulumi.Output[Optional['outputs.ComputeEnvironmentComputeResources']]:
        return pulumi.get(self, "compute_resources")

    @property
    @pulumi.getter(name="eksConfiguration")
    def eks_configuration(self) -> pulumi.Output[Optional['outputs.ComputeEnvironmentEksConfiguration']]:
        return pulumi.get(self, "eks_configuration")

    @property
    @pulumi.getter(name="replaceComputeEnvironment")
    def replace_compute_environment(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "replace_compute_environment")

    @property
    @pulumi.getter(name="serviceRole")
    def service_role(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "service_role")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A key-value pair to associate with a resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="unmanagedvCpus")
    def unmanagedv_cpus(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "unmanagedv_cpus")

    @property
    @pulumi.getter(name="updatePolicy")
    def update_policy(self) -> pulumi.Output[Optional['outputs.ComputeEnvironmentUpdatePolicy']]:
        return pulumi.get(self, "update_policy")

