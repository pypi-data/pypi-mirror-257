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

__all__ = ['GroupArgs', 'Group']

@pulumi.input_type
class GroupArgs:
    def __init__(__self__, *,
                 initial_version: Optional[pulumi.Input['GroupVersionArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None):
        """
        The set of arguments for constructing a Group resource.
        """
        if initial_version is not None:
            pulumi.set(__self__, "initial_version", initial_version)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="initialVersion")
    def initial_version(self) -> Optional[pulumi.Input['GroupVersionArgs']]:
        return pulumi.get(self, "initial_version")

    @initial_version.setter
    def initial_version(self, value: Optional[pulumi.Input['GroupVersionArgs']]):
        pulumi.set(self, "initial_version", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[Any]):
        pulumi.set(self, "tags", value)


warnings.warn("""Group is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class Group(pulumi.CustomResource):
    warnings.warn("""Group is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 initial_version: Optional[pulumi.Input[pulumi.InputType['GroupVersionArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Greengrass::Group

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[GroupArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Greengrass::Group

        :param str resource_name: The name of the resource.
        :param GroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 initial_version: Optional[pulumi.Input[pulumi.InputType['GroupVersionArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 __props__=None):
        pulumi.log.warn("""Group is deprecated: Group is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GroupArgs.__new__(GroupArgs)

            __props__.__dict__["initial_version"] = initial_version
            __props__.__dict__["name"] = name
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["latest_version_arn"] = None
            __props__.__dict__["role_attached_at"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["initial_version"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Group, __self__).__init__(
            'aws-native:greengrass:Group',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Group':
        """
        Get an existing Group resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = GroupArgs.__new__(GroupArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["initial_version"] = None
        __props__.__dict__["latest_version_arn"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["role_arn"] = None
        __props__.__dict__["role_attached_at"] = None
        __props__.__dict__["tags"] = None
        return Group(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="initialVersion")
    def initial_version(self) -> pulumi.Output[Optional['outputs.GroupVersion']]:
        return pulumi.get(self, "initial_version")

    @property
    @pulumi.getter(name="latestVersionArn")
    def latest_version_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "latest_version_arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="roleAttachedAt")
    def role_attached_at(self) -> pulumi.Output[str]:
        return pulumi.get(self, "role_attached_at")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Any]]:
        return pulumi.get(self, "tags")

