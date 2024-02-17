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

__all__ = ['SecurityConfigArgs', 'SecurityConfig']

@pulumi.input_type
class SecurityConfigArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 saml_options: Optional[pulumi.Input['SecurityConfigSamlConfigOptionsArgs']] = None,
                 type: Optional[pulumi.Input['SecurityConfigType']] = None):
        """
        The set of arguments for constructing a SecurityConfig resource.
        :param pulumi.Input[str] description: Security config description
        :param pulumi.Input[str] name: The friendly name of the security config
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if saml_options is not None:
            pulumi.set(__self__, "saml_options", saml_options)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Security config description
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The friendly name of the security config
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="samlOptions")
    def saml_options(self) -> Optional[pulumi.Input['SecurityConfigSamlConfigOptionsArgs']]:
        return pulumi.get(self, "saml_options")

    @saml_options.setter
    def saml_options(self, value: Optional[pulumi.Input['SecurityConfigSamlConfigOptionsArgs']]):
        pulumi.set(self, "saml_options", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['SecurityConfigType']]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['SecurityConfigType']]):
        pulumi.set(self, "type", value)


class SecurityConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 saml_options: Optional[pulumi.Input[pulumi.InputType['SecurityConfigSamlConfigOptionsArgs']]] = None,
                 type: Optional[pulumi.Input['SecurityConfigType']] = None,
                 __props__=None):
        """
        Amazon OpenSearchServerless security config resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Security config description
        :param pulumi.Input[str] name: The friendly name of the security config
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[SecurityConfigArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Amazon OpenSearchServerless security config resource

        :param str resource_name: The name of the resource.
        :param SecurityConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecurityConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 saml_options: Optional[pulumi.Input[pulumi.InputType['SecurityConfigSamlConfigOptionsArgs']]] = None,
                 type: Optional[pulumi.Input['SecurityConfigType']] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SecurityConfigArgs.__new__(SecurityConfigArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["saml_options"] = saml_options
            __props__.__dict__["type"] = type
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["name", "type"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(SecurityConfig, __self__).__init__(
            'aws-native:opensearchserverless:SecurityConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SecurityConfig':
        """
        Get an existing SecurityConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SecurityConfigArgs.__new__(SecurityConfigArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["saml_options"] = None
        __props__.__dict__["type"] = None
        return SecurityConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Security config description
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The friendly name of the security config
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="samlOptions")
    def saml_options(self) -> pulumi.Output[Optional['outputs.SecurityConfigSamlConfigOptions']]:
        return pulumi.get(self, "saml_options")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional['SecurityConfigType']]:
        return pulumi.get(self, "type")

