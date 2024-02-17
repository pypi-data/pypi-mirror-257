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

__all__ = ['AliasArgs', 'Alias']

@pulumi.input_type
class AliasArgs:
    def __init__(__self__, *,
                 function_name: pulumi.Input[str],
                 function_version: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provisioned_concurrency_config: Optional[pulumi.Input['AliasProvisionedConcurrencyConfigurationArgs']] = None,
                 routing_config: Optional[pulumi.Input['AliasRoutingConfigurationArgs']] = None):
        """
        The set of arguments for constructing a Alias resource.
        """
        pulumi.set(__self__, "function_name", function_name)
        pulumi.set(__self__, "function_version", function_version)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if provisioned_concurrency_config is not None:
            pulumi.set(__self__, "provisioned_concurrency_config", provisioned_concurrency_config)
        if routing_config is not None:
            pulumi.set(__self__, "routing_config", routing_config)

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "function_name")

    @function_name.setter
    def function_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "function_name", value)

    @property
    @pulumi.getter(name="functionVersion")
    def function_version(self) -> pulumi.Input[str]:
        return pulumi.get(self, "function_version")

    @function_version.setter
    def function_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "function_version", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="provisionedConcurrencyConfig")
    def provisioned_concurrency_config(self) -> Optional[pulumi.Input['AliasProvisionedConcurrencyConfigurationArgs']]:
        return pulumi.get(self, "provisioned_concurrency_config")

    @provisioned_concurrency_config.setter
    def provisioned_concurrency_config(self, value: Optional[pulumi.Input['AliasProvisionedConcurrencyConfigurationArgs']]):
        pulumi.set(self, "provisioned_concurrency_config", value)

    @property
    @pulumi.getter(name="routingConfig")
    def routing_config(self) -> Optional[pulumi.Input['AliasRoutingConfigurationArgs']]:
        return pulumi.get(self, "routing_config")

    @routing_config.setter
    def routing_config(self, value: Optional[pulumi.Input['AliasRoutingConfigurationArgs']]):
        pulumi.set(self, "routing_config", value)


warnings.warn("""Alias is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class Alias(pulumi.CustomResource):
    warnings.warn("""Alias is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 function_name: Optional[pulumi.Input[str]] = None,
                 function_version: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provisioned_concurrency_config: Optional[pulumi.Input[pulumi.InputType['AliasProvisionedConcurrencyConfigurationArgs']]] = None,
                 routing_config: Optional[pulumi.Input[pulumi.InputType['AliasRoutingConfigurationArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Lambda::Alias

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AliasArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Lambda::Alias

        :param str resource_name: The name of the resource.
        :param AliasArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AliasArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 function_name: Optional[pulumi.Input[str]] = None,
                 function_version: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provisioned_concurrency_config: Optional[pulumi.Input[pulumi.InputType['AliasProvisionedConcurrencyConfigurationArgs']]] = None,
                 routing_config: Optional[pulumi.Input[pulumi.InputType['AliasRoutingConfigurationArgs']]] = None,
                 __props__=None):
        pulumi.log.warn("""Alias is deprecated: Alias is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AliasArgs.__new__(AliasArgs)

            __props__.__dict__["description"] = description
            if function_name is None and not opts.urn:
                raise TypeError("Missing required property 'function_name'")
            __props__.__dict__["function_name"] = function_name
            if function_version is None and not opts.urn:
                raise TypeError("Missing required property 'function_version'")
            __props__.__dict__["function_version"] = function_version
            __props__.__dict__["name"] = name
            __props__.__dict__["provisioned_concurrency_config"] = provisioned_concurrency_config
            __props__.__dict__["routing_config"] = routing_config
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["function_name", "name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Alias, __self__).__init__(
            'aws-native:lambda:Alias',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Alias':
        """
        Get an existing Alias resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AliasArgs.__new__(AliasArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["function_name"] = None
        __props__.__dict__["function_version"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioned_concurrency_config"] = None
        __props__.__dict__["routing_config"] = None
        return Alias(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "function_name")

    @property
    @pulumi.getter(name="functionVersion")
    def function_version(self) -> pulumi.Output[str]:
        return pulumi.get(self, "function_version")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisionedConcurrencyConfig")
    def provisioned_concurrency_config(self) -> pulumi.Output[Optional['outputs.AliasProvisionedConcurrencyConfiguration']]:
        return pulumi.get(self, "provisioned_concurrency_config")

    @property
    @pulumi.getter(name="routingConfig")
    def routing_config(self) -> pulumi.Output[Optional['outputs.AliasRoutingConfiguration']]:
        return pulumi.get(self, "routing_config")

