# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AttributeGroupAssociationArgs', 'AttributeGroupAssociation']

@pulumi.input_type
class AttributeGroupAssociationArgs:
    def __init__(__self__, *,
                 application: pulumi.Input[str],
                 attribute_group: pulumi.Input[str]):
        """
        The set of arguments for constructing a AttributeGroupAssociation resource.
        :param pulumi.Input[str] application: The name or the Id of the Application.
        :param pulumi.Input[str] attribute_group: The name or the Id of the AttributeGroup.
        """
        pulumi.set(__self__, "application", application)
        pulumi.set(__self__, "attribute_group", attribute_group)

    @property
    @pulumi.getter
    def application(self) -> pulumi.Input[str]:
        """
        The name or the Id of the Application.
        """
        return pulumi.get(self, "application")

    @application.setter
    def application(self, value: pulumi.Input[str]):
        pulumi.set(self, "application", value)

    @property
    @pulumi.getter(name="attributeGroup")
    def attribute_group(self) -> pulumi.Input[str]:
        """
        The name or the Id of the AttributeGroup.
        """
        return pulumi.get(self, "attribute_group")

    @attribute_group.setter
    def attribute_group(self, value: pulumi.Input[str]):
        pulumi.set(self, "attribute_group", value)


class AttributeGroupAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application: Optional[pulumi.Input[str]] = None,
                 attribute_group: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Schema for AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application: The name or the Id of the Application.
        :param pulumi.Input[str] attribute_group: The name or the Id of the AttributeGroup.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AttributeGroupAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Schema for AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.

        :param str resource_name: The name of the resource.
        :param AttributeGroupAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AttributeGroupAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application: Optional[pulumi.Input[str]] = None,
                 attribute_group: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AttributeGroupAssociationArgs.__new__(AttributeGroupAssociationArgs)

            if application is None and not opts.urn:
                raise TypeError("Missing required property 'application'")
            __props__.__dict__["application"] = application
            if attribute_group is None and not opts.urn:
                raise TypeError("Missing required property 'attribute_group'")
            __props__.__dict__["attribute_group"] = attribute_group
            __props__.__dict__["application_arn"] = None
            __props__.__dict__["attribute_group_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["application", "attribute_group"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(AttributeGroupAssociation, __self__).__init__(
            'aws-native:servicecatalogappregistry:AttributeGroupAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AttributeGroupAssociation':
        """
        Get an existing AttributeGroupAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AttributeGroupAssociationArgs.__new__(AttributeGroupAssociationArgs)

        __props__.__dict__["application"] = None
        __props__.__dict__["application_arn"] = None
        __props__.__dict__["attribute_group"] = None
        __props__.__dict__["attribute_group_arn"] = None
        return AttributeGroupAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def application(self) -> pulumi.Output[str]:
        """
        The name or the Id of the Application.
        """
        return pulumi.get(self, "application")

    @property
    @pulumi.getter(name="applicationArn")
    def application_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "application_arn")

    @property
    @pulumi.getter(name="attributeGroup")
    def attribute_group(self) -> pulumi.Output[str]:
        """
        The name or the Id of the AttributeGroup.
        """
        return pulumi.get(self, "attribute_group")

    @property
    @pulumi.getter(name="attributeGroupArn")
    def attribute_group_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "attribute_group_arn")

