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

__all__ = ['PrivateDnsNamespaceArgs', 'PrivateDnsNamespace']

@pulumi.input_type
class PrivateDnsNamespaceArgs:
    def __init__(__self__, *,
                 vpc: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['PrivateDnsNamespacePropertiesArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateDnsNamespaceTagArgs']]]] = None):
        """
        The set of arguments for constructing a PrivateDnsNamespace resource.
        """
        pulumi.set(__self__, "vpc", vpc)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def vpc(self) -> pulumi.Input[str]:
        return pulumi.get(self, "vpc")

    @vpc.setter
    def vpc(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc", value)

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
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['PrivateDnsNamespacePropertiesArgs']]:
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['PrivateDnsNamespacePropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PrivateDnsNamespaceTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateDnsNamespaceTagArgs']]]]):
        pulumi.set(self, "tags", value)


warnings.warn("""PrivateDnsNamespace is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class PrivateDnsNamespace(pulumi.CustomResource):
    warnings.warn("""PrivateDnsNamespace is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['PrivateDnsNamespacePropertiesArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivateDnsNamespaceTagArgs']]]]] = None,
                 vpc: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::ServiceDiscovery::PrivateDnsNamespace

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PrivateDnsNamespaceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::ServiceDiscovery::PrivateDnsNamespace

        :param str resource_name: The name of the resource.
        :param PrivateDnsNamespaceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PrivateDnsNamespaceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['PrivateDnsNamespacePropertiesArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivateDnsNamespaceTagArgs']]]]] = None,
                 vpc: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""PrivateDnsNamespace is deprecated: PrivateDnsNamespace is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PrivateDnsNamespaceArgs.__new__(PrivateDnsNamespaceArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["properties"] = properties
            __props__.__dict__["tags"] = tags
            if vpc is None and not opts.urn:
                raise TypeError("Missing required property 'vpc'")
            __props__.__dict__["vpc"] = vpc
            __props__.__dict__["arn"] = None
            __props__.__dict__["hosted_zone_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["name", "vpc"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(PrivateDnsNamespace, __self__).__init__(
            'aws-native:servicediscovery:PrivateDnsNamespace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PrivateDnsNamespace':
        """
        Get an existing PrivateDnsNamespace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PrivateDnsNamespaceArgs.__new__(PrivateDnsNamespaceArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["hosted_zone_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["vpc"] = None
        return PrivateDnsNamespace(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="hostedZoneId")
    def hosted_zone_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "hosted_zone_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Optional['outputs.PrivateDnsNamespaceProperties']]:
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.PrivateDnsNamespaceTag']]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def vpc(self) -> pulumi.Output[str]:
        return pulumi.get(self, "vpc")

