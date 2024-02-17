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

__all__ = ['PackageArgs', 'Package']

@pulumi.input_type
class PackageArgs:
    def __init__(__self__, *,
                 package_name: Optional[pulumi.Input[str]] = None,
                 storage_location: Optional[pulumi.Input['PackageStorageLocationArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['PackageTagArgs']]]] = None):
        """
        The set of arguments for constructing a Package resource.
        """
        if package_name is not None:
            pulumi.set(__self__, "package_name", package_name)
        if storage_location is not None:
            pulumi.set(__self__, "storage_location", storage_location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="packageName")
    def package_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "package_name")

    @package_name.setter
    def package_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_name", value)

    @property
    @pulumi.getter(name="storageLocation")
    def storage_location(self) -> Optional[pulumi.Input['PackageStorageLocationArgs']]:
        return pulumi.get(self, "storage_location")

    @storage_location.setter
    def storage_location(self, value: Optional[pulumi.Input['PackageStorageLocationArgs']]):
        pulumi.set(self, "storage_location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PackageTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PackageTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Package(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 package_name: Optional[pulumi.Input[str]] = None,
                 storage_location: Optional[pulumi.Input[pulumi.InputType['PackageStorageLocationArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PackageTagArgs']]]]] = None,
                 __props__=None):
        """
        Schema for Package CloudFormation Resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[PackageArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Schema for Package CloudFormation Resource

        :param str resource_name: The name of the resource.
        :param PackageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PackageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 package_name: Optional[pulumi.Input[str]] = None,
                 storage_location: Optional[pulumi.Input[pulumi.InputType['PackageStorageLocationArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PackageTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PackageArgs.__new__(PackageArgs)

            __props__.__dict__["package_name"] = package_name
            __props__.__dict__["storage_location"] = storage_location
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["created_time"] = None
            __props__.__dict__["package_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["package_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Package, __self__).__init__(
            'aws-native:panorama:Package',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Package':
        """
        Get an existing Package resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PackageArgs.__new__(PackageArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["created_time"] = None
        __props__.__dict__["package_id"] = None
        __props__.__dict__["package_name"] = None
        __props__.__dict__["storage_location"] = None
        __props__.__dict__["tags"] = None
        return Package(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> pulumi.Output[int]:
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="packageId")
    def package_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "package_id")

    @property
    @pulumi.getter(name="packageName")
    def package_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "package_name")

    @property
    @pulumi.getter(name="storageLocation")
    def storage_location(self) -> pulumi.Output[Optional['outputs.PackageStorageLocation']]:
        return pulumi.get(self, "storage_location")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.PackageTag']]]:
        return pulumi.get(self, "tags")

