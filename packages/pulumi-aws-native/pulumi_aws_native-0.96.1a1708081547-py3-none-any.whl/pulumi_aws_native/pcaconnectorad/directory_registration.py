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

__all__ = ['DirectoryRegistrationArgs', 'DirectoryRegistration']

@pulumi.input_type
class DirectoryRegistrationArgs:
    def __init__(__self__, *,
                 directory_id: pulumi.Input[str],
                 tags: Optional[pulumi.Input['DirectoryRegistrationTagsArgs']] = None):
        """
        The set of arguments for constructing a DirectoryRegistration resource.
        """
        pulumi.set(__self__, "directory_id", directory_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "directory_id")

    @directory_id.setter
    def directory_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "directory_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input['DirectoryRegistrationTagsArgs']]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input['DirectoryRegistrationTagsArgs']]):
        pulumi.set(self, "tags", value)


class DirectoryRegistration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[pulumi.InputType['DirectoryRegistrationTagsArgs']]] = None,
                 __props__=None):
        """
        Definition of AWS::PCAConnectorAD::DirectoryRegistration Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DirectoryRegistrationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::PCAConnectorAD::DirectoryRegistration Resource Type

        :param str resource_name: The name of the resource.
        :param DirectoryRegistrationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DirectoryRegistrationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[pulumi.InputType['DirectoryRegistrationTagsArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DirectoryRegistrationArgs.__new__(DirectoryRegistrationArgs)

            if directory_id is None and not opts.urn:
                raise TypeError("Missing required property 'directory_id'")
            __props__.__dict__["directory_id"] = directory_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["directory_registration_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["directory_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(DirectoryRegistration, __self__).__init__(
            'aws-native:pcaconnectorad:DirectoryRegistration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DirectoryRegistration':
        """
        Get an existing DirectoryRegistration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DirectoryRegistrationArgs.__new__(DirectoryRegistrationArgs)

        __props__.__dict__["directory_id"] = None
        __props__.__dict__["directory_registration_arn"] = None
        __props__.__dict__["tags"] = None
        return DirectoryRegistration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "directory_id")

    @property
    @pulumi.getter(name="directoryRegistrationArn")
    def directory_registration_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "directory_registration_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional['outputs.DirectoryRegistrationTags']]:
        return pulumi.get(self, "tags")

