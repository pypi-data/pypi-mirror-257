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

__all__ = ['HookTypeConfigArgs', 'HookTypeConfig']

@pulumi.input_type
class HookTypeConfigArgs:
    def __init__(__self__, *,
                 configuration: Optional[pulumi.Input[str]] = None,
                 configuration_alias: Optional[pulumi.Input['HookTypeConfigConfigurationAlias']] = None,
                 type_arn: Optional[pulumi.Input[str]] = None,
                 type_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a HookTypeConfig resource.
        :param pulumi.Input[str] configuration: The configuration data for the extension, in this account and region.
        :param pulumi.Input['HookTypeConfigConfigurationAlias'] configuration_alias: An alias by which to refer to this extension configuration data.
        :param pulumi.Input[str] type_arn: The Amazon Resource Name (ARN) of the type without version number.
        :param pulumi.Input[str] type_name: The name of the type being registered.
               
               We recommend that type names adhere to the following pattern: company_or_organization::service::type.
        """
        if configuration is not None:
            pulumi.set(__self__, "configuration", configuration)
        if configuration_alias is not None:
            pulumi.set(__self__, "configuration_alias", configuration_alias)
        if type_arn is not None:
            pulumi.set(__self__, "type_arn", type_arn)
        if type_name is not None:
            pulumi.set(__self__, "type_name", type_name)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[pulumi.Input[str]]:
        """
        The configuration data for the extension, in this account and region.
        """
        return pulumi.get(self, "configuration")

    @configuration.setter
    def configuration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configuration", value)

    @property
    @pulumi.getter(name="configurationAlias")
    def configuration_alias(self) -> Optional[pulumi.Input['HookTypeConfigConfigurationAlias']]:
        """
        An alias by which to refer to this extension configuration data.
        """
        return pulumi.get(self, "configuration_alias")

    @configuration_alias.setter
    def configuration_alias(self, value: Optional[pulumi.Input['HookTypeConfigConfigurationAlias']]):
        pulumi.set(self, "configuration_alias", value)

    @property
    @pulumi.getter(name="typeArn")
    def type_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the type without version number.
        """
        return pulumi.get(self, "type_arn")

    @type_arn.setter
    def type_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type_arn", value)

    @property
    @pulumi.getter(name="typeName")
    def type_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the type being registered.

        We recommend that type names adhere to the following pattern: company_or_organization::service::type.
        """
        return pulumi.get(self, "type_name")

    @type_name.setter
    def type_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type_name", value)


class HookTypeConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration: Optional[pulumi.Input[str]] = None,
                 configuration_alias: Optional[pulumi.Input['HookTypeConfigConfigurationAlias']] = None,
                 type_arn: Optional[pulumi.Input[str]] = None,
                 type_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Specifies the configuration data for a registered hook in CloudFormation Registry.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configuration: The configuration data for the extension, in this account and region.
        :param pulumi.Input['HookTypeConfigConfigurationAlias'] configuration_alias: An alias by which to refer to this extension configuration data.
        :param pulumi.Input[str] type_arn: The Amazon Resource Name (ARN) of the type without version number.
        :param pulumi.Input[str] type_name: The name of the type being registered.
               
               We recommend that type names adhere to the following pattern: company_or_organization::service::type.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[HookTypeConfigArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Specifies the configuration data for a registered hook in CloudFormation Registry.

        :param str resource_name: The name of the resource.
        :param HookTypeConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HookTypeConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration: Optional[pulumi.Input[str]] = None,
                 configuration_alias: Optional[pulumi.Input['HookTypeConfigConfigurationAlias']] = None,
                 type_arn: Optional[pulumi.Input[str]] = None,
                 type_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HookTypeConfigArgs.__new__(HookTypeConfigArgs)

            __props__.__dict__["configuration"] = configuration
            __props__.__dict__["configuration_alias"] = configuration_alias
            __props__.__dict__["type_arn"] = type_arn
            __props__.__dict__["type_name"] = type_name
            __props__.__dict__["configuration_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["configuration_alias"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(HookTypeConfig, __self__).__init__(
            'aws-native:cloudformation:HookTypeConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'HookTypeConfig':
        """
        Get an existing HookTypeConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = HookTypeConfigArgs.__new__(HookTypeConfigArgs)

        __props__.__dict__["configuration"] = None
        __props__.__dict__["configuration_alias"] = None
        __props__.__dict__["configuration_arn"] = None
        __props__.__dict__["type_arn"] = None
        __props__.__dict__["type_name"] = None
        return HookTypeConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def configuration(self) -> pulumi.Output[Optional[str]]:
        """
        The configuration data for the extension, in this account and region.
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter(name="configurationAlias")
    def configuration_alias(self) -> pulumi.Output[Optional['HookTypeConfigConfigurationAlias']]:
        """
        An alias by which to refer to this extension configuration data.
        """
        return pulumi.get(self, "configuration_alias")

    @property
    @pulumi.getter(name="configurationArn")
    def configuration_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) for the configuration data, in this account and region.
        """
        return pulumi.get(self, "configuration_arn")

    @property
    @pulumi.getter(name="typeArn")
    def type_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the type without version number.
        """
        return pulumi.get(self, "type_arn")

    @property
    @pulumi.getter(name="typeName")
    def type_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the type being registered.

        We recommend that type names adhere to the following pattern: company_or_organization::service::type.
        """
        return pulumi.get(self, "type_name")

