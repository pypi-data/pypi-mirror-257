# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DefaultViewAssociationArgs', 'DefaultViewAssociation']

@pulumi.input_type
class DefaultViewAssociationArgs:
    def __init__(__self__, *,
                 view_arn: pulumi.Input[str]):
        """
        The set of arguments for constructing a DefaultViewAssociation resource.
        """
        pulumi.set(__self__, "view_arn", view_arn)

    @property
    @pulumi.getter(name="viewArn")
    def view_arn(self) -> pulumi.Input[str]:
        return pulumi.get(self, "view_arn")

    @view_arn.setter
    def view_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "view_arn", value)


class DefaultViewAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 view_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Definition of AWS::ResourceExplorer2::DefaultViewAssociation Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DefaultViewAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::ResourceExplorer2::DefaultViewAssociation Resource Type

        :param str resource_name: The name of the resource.
        :param DefaultViewAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DefaultViewAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 view_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DefaultViewAssociationArgs.__new__(DefaultViewAssociationArgs)

            if view_arn is None and not opts.urn:
                raise TypeError("Missing required property 'view_arn'")
            __props__.__dict__["view_arn"] = view_arn
            __props__.__dict__["associated_aws_principal"] = None
        super(DefaultViewAssociation, __self__).__init__(
            'aws-native:resourceexplorer2:DefaultViewAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DefaultViewAssociation':
        """
        Get an existing DefaultViewAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DefaultViewAssociationArgs.__new__(DefaultViewAssociationArgs)

        __props__.__dict__["associated_aws_principal"] = None
        __props__.__dict__["view_arn"] = None
        return DefaultViewAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="associatedAwsPrincipal")
    def associated_aws_principal(self) -> pulumi.Output[str]:
        """
        The AWS principal that the default view is associated with, used as the unique identifier for this resource.
        """
        return pulumi.get(self, "associated_aws_principal")

    @property
    @pulumi.getter(name="viewArn")
    def view_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "view_arn")

