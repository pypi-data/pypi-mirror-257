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

__all__ = ['RuleGroupsNamespaceArgs', 'RuleGroupsNamespace']

@pulumi.input_type
class RuleGroupsNamespaceArgs:
    def __init__(__self__, *,
                 data: pulumi.Input[str],
                 workspace: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['RuleGroupsNamespaceTagArgs']]]] = None):
        """
        The set of arguments for constructing a RuleGroupsNamespace resource.
        :param pulumi.Input[str] data: The RuleGroupsNamespace data.
        :param pulumi.Input[str] workspace: Required to identify a specific APS Workspace associated with this RuleGroupsNamespace.
        :param pulumi.Input[str] name: The RuleGroupsNamespace name.
        :param pulumi.Input[Sequence[pulumi.Input['RuleGroupsNamespaceTagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        pulumi.set(__self__, "data", data)
        pulumi.set(__self__, "workspace", workspace)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def data(self) -> pulumi.Input[str]:
        """
        The RuleGroupsNamespace data.
        """
        return pulumi.get(self, "data")

    @data.setter
    def data(self, value: pulumi.Input[str]):
        pulumi.set(self, "data", value)

    @property
    @pulumi.getter
    def workspace(self) -> pulumi.Input[str]:
        """
        Required to identify a specific APS Workspace associated with this RuleGroupsNamespace.
        """
        return pulumi.get(self, "workspace")

    @workspace.setter
    def workspace(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The RuleGroupsNamespace name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RuleGroupsNamespaceTagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RuleGroupsNamespaceTagArgs']]]]):
        pulumi.set(self, "tags", value)


class RuleGroupsNamespace(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleGroupsNamespaceTagArgs']]]]] = None,
                 workspace: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        RuleGroupsNamespace schema for cloudformation.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data: The RuleGroupsNamespace data.
        :param pulumi.Input[str] name: The RuleGroupsNamespace name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleGroupsNamespaceTagArgs']]]] tags: An array of key-value pairs to apply to this resource.
        :param pulumi.Input[str] workspace: Required to identify a specific APS Workspace associated with this RuleGroupsNamespace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RuleGroupsNamespaceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        RuleGroupsNamespace schema for cloudformation.

        :param str resource_name: The name of the resource.
        :param RuleGroupsNamespaceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RuleGroupsNamespaceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleGroupsNamespaceTagArgs']]]]] = None,
                 workspace: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RuleGroupsNamespaceArgs.__new__(RuleGroupsNamespaceArgs)

            if data is None and not opts.urn:
                raise TypeError("Missing required property 'data'")
            __props__.__dict__["data"] = data
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            if workspace is None and not opts.urn:
                raise TypeError("Missing required property 'workspace'")
            __props__.__dict__["workspace"] = workspace
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["name", "workspace"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(RuleGroupsNamespace, __self__).__init__(
            'aws-native:aps:RuleGroupsNamespace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RuleGroupsNamespace':
        """
        Get an existing RuleGroupsNamespace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RuleGroupsNamespaceArgs.__new__(RuleGroupsNamespaceArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["data"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["workspace"] = None
        return RuleGroupsNamespace(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The RuleGroupsNamespace ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def data(self) -> pulumi.Output[str]:
        """
        The RuleGroupsNamespace data.
        """
        return pulumi.get(self, "data")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The RuleGroupsNamespace name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.RuleGroupsNamespaceTag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def workspace(self) -> pulumi.Output[str]:
        """
        Required to identify a specific APS Workspace associated with this RuleGroupsNamespace.
        """
        return pulumi.get(self, "workspace")

