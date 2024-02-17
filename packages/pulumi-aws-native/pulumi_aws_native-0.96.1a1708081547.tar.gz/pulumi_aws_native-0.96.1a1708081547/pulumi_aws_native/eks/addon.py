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

__all__ = ['AddonArgs', 'Addon']

@pulumi.input_type
class AddonArgs:
    def __init__(__self__, *,
                 cluster_name: pulumi.Input[str],
                 addon_name: Optional[pulumi.Input[str]] = None,
                 addon_version: Optional[pulumi.Input[str]] = None,
                 configuration_values: Optional[pulumi.Input[str]] = None,
                 preserve_on_delete: Optional[pulumi.Input[bool]] = None,
                 resolve_conflicts: Optional[pulumi.Input['AddonResolveConflicts']] = None,
                 service_account_role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['AddonTagArgs']]]] = None):
        """
        The set of arguments for constructing a Addon resource.
        :param pulumi.Input[str] cluster_name: Name of Cluster
        :param pulumi.Input[str] addon_name: Name of Addon
        :param pulumi.Input[str] addon_version: Version of Addon
        :param pulumi.Input[str] configuration_values: The configuration values to use with the add-on
        :param pulumi.Input[bool] preserve_on_delete: PreserveOnDelete parameter value
        :param pulumi.Input['AddonResolveConflicts'] resolve_conflicts: Resolve parameter value conflicts
        :param pulumi.Input[str] service_account_role_arn: IAM role to bind to the add-on's service account
        :param pulumi.Input[Sequence[pulumi.Input['AddonTagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        pulumi.set(__self__, "cluster_name", cluster_name)
        if addon_name is not None:
            pulumi.set(__self__, "addon_name", addon_name)
        if addon_version is not None:
            pulumi.set(__self__, "addon_version", addon_version)
        if configuration_values is not None:
            pulumi.set(__self__, "configuration_values", configuration_values)
        if preserve_on_delete is not None:
            pulumi.set(__self__, "preserve_on_delete", preserve_on_delete)
        if resolve_conflicts is not None:
            pulumi.set(__self__, "resolve_conflicts", resolve_conflicts)
        if service_account_role_arn is not None:
            pulumi.set(__self__, "service_account_role_arn", service_account_role_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Input[str]:
        """
        Name of Cluster
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter(name="addonName")
    def addon_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of Addon
        """
        return pulumi.get(self, "addon_name")

    @addon_name.setter
    def addon_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "addon_name", value)

    @property
    @pulumi.getter(name="addonVersion")
    def addon_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of Addon
        """
        return pulumi.get(self, "addon_version")

    @addon_version.setter
    def addon_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "addon_version", value)

    @property
    @pulumi.getter(name="configurationValues")
    def configuration_values(self) -> Optional[pulumi.Input[str]]:
        """
        The configuration values to use with the add-on
        """
        return pulumi.get(self, "configuration_values")

    @configuration_values.setter
    def configuration_values(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configuration_values", value)

    @property
    @pulumi.getter(name="preserveOnDelete")
    def preserve_on_delete(self) -> Optional[pulumi.Input[bool]]:
        """
        PreserveOnDelete parameter value
        """
        return pulumi.get(self, "preserve_on_delete")

    @preserve_on_delete.setter
    def preserve_on_delete(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "preserve_on_delete", value)

    @property
    @pulumi.getter(name="resolveConflicts")
    def resolve_conflicts(self) -> Optional[pulumi.Input['AddonResolveConflicts']]:
        """
        Resolve parameter value conflicts
        """
        return pulumi.get(self, "resolve_conflicts")

    @resolve_conflicts.setter
    def resolve_conflicts(self, value: Optional[pulumi.Input['AddonResolveConflicts']]):
        pulumi.set(self, "resolve_conflicts", value)

    @property
    @pulumi.getter(name="serviceAccountRoleArn")
    def service_account_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        IAM role to bind to the add-on's service account
        """
        return pulumi.get(self, "service_account_role_arn")

    @service_account_role_arn.setter
    def service_account_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_account_role_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AddonTagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AddonTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Addon(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 addon_name: Optional[pulumi.Input[str]] = None,
                 addon_version: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 configuration_values: Optional[pulumi.Input[str]] = None,
                 preserve_on_delete: Optional[pulumi.Input[bool]] = None,
                 resolve_conflicts: Optional[pulumi.Input['AddonResolveConflicts']] = None,
                 service_account_role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AddonTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Schema for AWS::EKS::Addon

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] addon_name: Name of Addon
        :param pulumi.Input[str] addon_version: Version of Addon
        :param pulumi.Input[str] cluster_name: Name of Cluster
        :param pulumi.Input[str] configuration_values: The configuration values to use with the add-on
        :param pulumi.Input[bool] preserve_on_delete: PreserveOnDelete parameter value
        :param pulumi.Input['AddonResolveConflicts'] resolve_conflicts: Resolve parameter value conflicts
        :param pulumi.Input[str] service_account_role_arn: IAM role to bind to the add-on's service account
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AddonTagArgs']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AddonArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Schema for AWS::EKS::Addon

        :param str resource_name: The name of the resource.
        :param AddonArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AddonArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 addon_name: Optional[pulumi.Input[str]] = None,
                 addon_version: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 configuration_values: Optional[pulumi.Input[str]] = None,
                 preserve_on_delete: Optional[pulumi.Input[bool]] = None,
                 resolve_conflicts: Optional[pulumi.Input['AddonResolveConflicts']] = None,
                 service_account_role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AddonTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AddonArgs.__new__(AddonArgs)

            __props__.__dict__["addon_name"] = addon_name
            __props__.__dict__["addon_version"] = addon_version
            if cluster_name is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_name'")
            __props__.__dict__["cluster_name"] = cluster_name
            __props__.__dict__["configuration_values"] = configuration_values
            __props__.__dict__["preserve_on_delete"] = preserve_on_delete
            __props__.__dict__["resolve_conflicts"] = resolve_conflicts
            __props__.__dict__["service_account_role_arn"] = service_account_role_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["addon_name", "cluster_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Addon, __self__).__init__(
            'aws-native:eks:Addon',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Addon':
        """
        Get an existing Addon resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AddonArgs.__new__(AddonArgs)

        __props__.__dict__["addon_name"] = None
        __props__.__dict__["addon_version"] = None
        __props__.__dict__["arn"] = None
        __props__.__dict__["cluster_name"] = None
        __props__.__dict__["configuration_values"] = None
        __props__.__dict__["preserve_on_delete"] = None
        __props__.__dict__["resolve_conflicts"] = None
        __props__.__dict__["service_account_role_arn"] = None
        __props__.__dict__["tags"] = None
        return Addon(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addonName")
    def addon_name(self) -> pulumi.Output[str]:
        """
        Name of Addon
        """
        return pulumi.get(self, "addon_name")

    @property
    @pulumi.getter(name="addonVersion")
    def addon_version(self) -> pulumi.Output[Optional[str]]:
        """
        Version of Addon
        """
        return pulumi.get(self, "addon_version")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the add-on
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Output[str]:
        """
        Name of Cluster
        """
        return pulumi.get(self, "cluster_name")

    @property
    @pulumi.getter(name="configurationValues")
    def configuration_values(self) -> pulumi.Output[Optional[str]]:
        """
        The configuration values to use with the add-on
        """
        return pulumi.get(self, "configuration_values")

    @property
    @pulumi.getter(name="preserveOnDelete")
    def preserve_on_delete(self) -> pulumi.Output[Optional[bool]]:
        """
        PreserveOnDelete parameter value
        """
        return pulumi.get(self, "preserve_on_delete")

    @property
    @pulumi.getter(name="resolveConflicts")
    def resolve_conflicts(self) -> pulumi.Output[Optional['AddonResolveConflicts']]:
        """
        Resolve parameter value conflicts
        """
        return pulumi.get(self, "resolve_conflicts")

    @property
    @pulumi.getter(name="serviceAccountRoleArn")
    def service_account_role_arn(self) -> pulumi.Output[Optional[str]]:
        """
        IAM role to bind to the add-on's service account
        """
        return pulumi.get(self, "service_account_role_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.AddonTag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

