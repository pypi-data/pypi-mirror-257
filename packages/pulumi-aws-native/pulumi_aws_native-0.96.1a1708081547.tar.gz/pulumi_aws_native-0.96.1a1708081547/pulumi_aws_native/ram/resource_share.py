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

__all__ = ['ResourceShareArgs', 'ResourceShare']

@pulumi.input_type
class ResourceShareArgs:
    def __init__(__self__, *,
                 allow_external_principals: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permission_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 principals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resource_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceShareTagArgs']]]] = None):
        """
        The set of arguments for constructing a ResourceShare resource.
        """
        if allow_external_principals is not None:
            pulumi.set(__self__, "allow_external_principals", allow_external_principals)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if permission_arns is not None:
            pulumi.set(__self__, "permission_arns", permission_arns)
        if principals is not None:
            pulumi.set(__self__, "principals", principals)
        if resource_arns is not None:
            pulumi.set(__self__, "resource_arns", resource_arns)
        if sources is not None:
            pulumi.set(__self__, "sources", sources)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="allowExternalPrincipals")
    def allow_external_principals(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "allow_external_principals")

    @allow_external_principals.setter
    def allow_external_principals(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_external_principals", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="permissionArns")
    def permission_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "permission_arns")

    @permission_arns.setter
    def permission_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "permission_arns", value)

    @property
    @pulumi.getter
    def principals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "principals")

    @principals.setter
    def principals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "principals", value)

    @property
    @pulumi.getter(name="resourceArns")
    def resource_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "resource_arns")

    @resource_arns.setter
    def resource_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resource_arns", value)

    @property
    @pulumi.getter
    def sources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "sources")

    @sources.setter
    def sources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "sources", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ResourceShareTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceShareTagArgs']]]]):
        pulumi.set(self, "tags", value)


warnings.warn("""ResourceShare is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class ResourceShare(pulumi.CustomResource):
    warnings.warn("""ResourceShare is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_external_principals: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permission_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 principals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resource_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceShareTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::RAM::ResourceShare

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ResourceShareArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::RAM::ResourceShare

        :param str resource_name: The name of the resource.
        :param ResourceShareArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceShareArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_external_principals: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permission_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 principals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resource_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceShareTagArgs']]]]] = None,
                 __props__=None):
        pulumi.log.warn("""ResourceShare is deprecated: ResourceShare is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceShareArgs.__new__(ResourceShareArgs)

            __props__.__dict__["allow_external_principals"] = allow_external_principals
            __props__.__dict__["name"] = name
            __props__.__dict__["permission_arns"] = permission_arns
            __props__.__dict__["principals"] = principals
            __props__.__dict__["resource_arns"] = resource_arns
            __props__.__dict__["sources"] = sources
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
        super(ResourceShare, __self__).__init__(
            'aws-native:ram:ResourceShare',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ResourceShare':
        """
        Get an existing ResourceShare resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ResourceShareArgs.__new__(ResourceShareArgs)

        __props__.__dict__["allow_external_principals"] = None
        __props__.__dict__["arn"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["permission_arns"] = None
        __props__.__dict__["principals"] = None
        __props__.__dict__["resource_arns"] = None
        __props__.__dict__["sources"] = None
        __props__.__dict__["tags"] = None
        return ResourceShare(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowExternalPrincipals")
    def allow_external_principals(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "allow_external_principals")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="permissionArns")
    def permission_arns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "permission_arns")

    @property
    @pulumi.getter
    def principals(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "principals")

    @property
    @pulumi.getter(name="resourceArns")
    def resource_arns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "resource_arns")

    @property
    @pulumi.getter
    def sources(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "sources")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.ResourceShareTag']]]:
        return pulumi.get(self, "tags")

