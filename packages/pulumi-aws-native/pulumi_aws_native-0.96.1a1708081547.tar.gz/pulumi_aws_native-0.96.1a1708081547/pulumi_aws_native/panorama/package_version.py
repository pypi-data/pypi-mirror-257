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

__all__ = ['PackageVersionArgs', 'PackageVersion']

@pulumi.input_type
class PackageVersionArgs:
    def __init__(__self__, *,
                 package_id: pulumi.Input[str],
                 package_version: pulumi.Input[str],
                 patch_version: pulumi.Input[str],
                 mark_latest: Optional[pulumi.Input[bool]] = None,
                 owner_account: Optional[pulumi.Input[str]] = None,
                 updated_latest_patch_version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PackageVersion resource.
        """
        pulumi.set(__self__, "package_id", package_id)
        pulumi.set(__self__, "package_version", package_version)
        pulumi.set(__self__, "patch_version", patch_version)
        if mark_latest is not None:
            pulumi.set(__self__, "mark_latest", mark_latest)
        if owner_account is not None:
            pulumi.set(__self__, "owner_account", owner_account)
        if updated_latest_patch_version is not None:
            pulumi.set(__self__, "updated_latest_patch_version", updated_latest_patch_version)

    @property
    @pulumi.getter(name="packageId")
    def package_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "package_id")

    @package_id.setter
    def package_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "package_id", value)

    @property
    @pulumi.getter(name="packageVersion")
    def package_version(self) -> pulumi.Input[str]:
        return pulumi.get(self, "package_version")

    @package_version.setter
    def package_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "package_version", value)

    @property
    @pulumi.getter(name="patchVersion")
    def patch_version(self) -> pulumi.Input[str]:
        return pulumi.get(self, "patch_version")

    @patch_version.setter
    def patch_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "patch_version", value)

    @property
    @pulumi.getter(name="markLatest")
    def mark_latest(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "mark_latest")

    @mark_latest.setter
    def mark_latest(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "mark_latest", value)

    @property
    @pulumi.getter(name="ownerAccount")
    def owner_account(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "owner_account")

    @owner_account.setter
    def owner_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_account", value)

    @property
    @pulumi.getter(name="updatedLatestPatchVersion")
    def updated_latest_patch_version(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "updated_latest_patch_version")

    @updated_latest_patch_version.setter
    def updated_latest_patch_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "updated_latest_patch_version", value)


class PackageVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 mark_latest: Optional[pulumi.Input[bool]] = None,
                 owner_account: Optional[pulumi.Input[str]] = None,
                 package_id: Optional[pulumi.Input[str]] = None,
                 package_version: Optional[pulumi.Input[str]] = None,
                 patch_version: Optional[pulumi.Input[str]] = None,
                 updated_latest_patch_version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Schema for PackageVersion Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PackageVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Schema for PackageVersion Resource Type

        :param str resource_name: The name of the resource.
        :param PackageVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PackageVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 mark_latest: Optional[pulumi.Input[bool]] = None,
                 owner_account: Optional[pulumi.Input[str]] = None,
                 package_id: Optional[pulumi.Input[str]] = None,
                 package_version: Optional[pulumi.Input[str]] = None,
                 patch_version: Optional[pulumi.Input[str]] = None,
                 updated_latest_patch_version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PackageVersionArgs.__new__(PackageVersionArgs)

            __props__.__dict__["mark_latest"] = mark_latest
            __props__.__dict__["owner_account"] = owner_account
            if package_id is None and not opts.urn:
                raise TypeError("Missing required property 'package_id'")
            __props__.__dict__["package_id"] = package_id
            if package_version is None and not opts.urn:
                raise TypeError("Missing required property 'package_version'")
            __props__.__dict__["package_version"] = package_version
            if patch_version is None and not opts.urn:
                raise TypeError("Missing required property 'patch_version'")
            __props__.__dict__["patch_version"] = patch_version
            __props__.__dict__["updated_latest_patch_version"] = updated_latest_patch_version
            __props__.__dict__["is_latest_patch"] = None
            __props__.__dict__["package_arn"] = None
            __props__.__dict__["package_name"] = None
            __props__.__dict__["registered_time"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["status_description"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["owner_account", "package_id", "package_version", "patch_version"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(PackageVersion, __self__).__init__(
            'aws-native:panorama:PackageVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PackageVersion':
        """
        Get an existing PackageVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PackageVersionArgs.__new__(PackageVersionArgs)

        __props__.__dict__["is_latest_patch"] = None
        __props__.__dict__["mark_latest"] = None
        __props__.__dict__["owner_account"] = None
        __props__.__dict__["package_arn"] = None
        __props__.__dict__["package_id"] = None
        __props__.__dict__["package_name"] = None
        __props__.__dict__["package_version"] = None
        __props__.__dict__["patch_version"] = None
        __props__.__dict__["registered_time"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["status_description"] = None
        __props__.__dict__["updated_latest_patch_version"] = None
        return PackageVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="isLatestPatch")
    def is_latest_patch(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "is_latest_patch")

    @property
    @pulumi.getter(name="markLatest")
    def mark_latest(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "mark_latest")

    @property
    @pulumi.getter(name="ownerAccount")
    def owner_account(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "owner_account")

    @property
    @pulumi.getter(name="packageArn")
    def package_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "package_arn")

    @property
    @pulumi.getter(name="packageId")
    def package_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "package_id")

    @property
    @pulumi.getter(name="packageName")
    def package_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "package_name")

    @property
    @pulumi.getter(name="packageVersion")
    def package_version(self) -> pulumi.Output[str]:
        return pulumi.get(self, "package_version")

    @property
    @pulumi.getter(name="patchVersion")
    def patch_version(self) -> pulumi.Output[str]:
        return pulumi.get(self, "patch_version")

    @property
    @pulumi.getter(name="registeredTime")
    def registered_time(self) -> pulumi.Output[int]:
        return pulumi.get(self, "registered_time")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['PackageVersionStatus']:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusDescription")
    def status_description(self) -> pulumi.Output[str]:
        return pulumi.get(self, "status_description")

    @property
    @pulumi.getter(name="updatedLatestPatchVersion")
    def updated_latest_patch_version(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "updated_latest_patch_version")

