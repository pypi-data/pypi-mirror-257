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

__all__ = ['SourceApiAssociationArgs', 'SourceApiAssociation']

@pulumi.input_type
class SourceApiAssociationArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 merged_api_identifier: Optional[pulumi.Input[str]] = None,
                 source_api_association_config: Optional[pulumi.Input['SourceApiAssociationConfigArgs']] = None,
                 source_api_identifier: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SourceApiAssociation resource.
        :param pulumi.Input[str] description: Description of the SourceApiAssociation.
        :param pulumi.Input[str] merged_api_identifier: Identifier of the Merged GraphQLApi to associate. It could be either GraphQLApi ApiId or ARN
        :param pulumi.Input['SourceApiAssociationConfigArgs'] source_api_association_config: Customized configuration for SourceApiAssociation.
        :param pulumi.Input[str] source_api_identifier: Identifier of the Source GraphQLApi to associate. It could be either GraphQLApi ApiId or ARN
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if merged_api_identifier is not None:
            pulumi.set(__self__, "merged_api_identifier", merged_api_identifier)
        if source_api_association_config is not None:
            pulumi.set(__self__, "source_api_association_config", source_api_association_config)
        if source_api_identifier is not None:
            pulumi.set(__self__, "source_api_identifier", source_api_identifier)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the SourceApiAssociation.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="mergedApiIdentifier")
    def merged_api_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of the Merged GraphQLApi to associate. It could be either GraphQLApi ApiId or ARN
        """
        return pulumi.get(self, "merged_api_identifier")

    @merged_api_identifier.setter
    def merged_api_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "merged_api_identifier", value)

    @property
    @pulumi.getter(name="sourceApiAssociationConfig")
    def source_api_association_config(self) -> Optional[pulumi.Input['SourceApiAssociationConfigArgs']]:
        """
        Customized configuration for SourceApiAssociation.
        """
        return pulumi.get(self, "source_api_association_config")

    @source_api_association_config.setter
    def source_api_association_config(self, value: Optional[pulumi.Input['SourceApiAssociationConfigArgs']]):
        pulumi.set(self, "source_api_association_config", value)

    @property
    @pulumi.getter(name="sourceApiIdentifier")
    def source_api_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of the Source GraphQLApi to associate. It could be either GraphQLApi ApiId or ARN
        """
        return pulumi.get(self, "source_api_identifier")

    @source_api_identifier.setter
    def source_api_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_api_identifier", value)


class SourceApiAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 merged_api_identifier: Optional[pulumi.Input[str]] = None,
                 source_api_association_config: Optional[pulumi.Input[pulumi.InputType['SourceApiAssociationConfigArgs']]] = None,
                 source_api_identifier: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::AppSync::SourceApiAssociation

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the SourceApiAssociation.
        :param pulumi.Input[str] merged_api_identifier: Identifier of the Merged GraphQLApi to associate. It could be either GraphQLApi ApiId or ARN
        :param pulumi.Input[pulumi.InputType['SourceApiAssociationConfigArgs']] source_api_association_config: Customized configuration for SourceApiAssociation.
        :param pulumi.Input[str] source_api_identifier: Identifier of the Source GraphQLApi to associate. It could be either GraphQLApi ApiId or ARN
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[SourceApiAssociationArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::AppSync::SourceApiAssociation

        :param str resource_name: The name of the resource.
        :param SourceApiAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SourceApiAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 merged_api_identifier: Optional[pulumi.Input[str]] = None,
                 source_api_association_config: Optional[pulumi.Input[pulumi.InputType['SourceApiAssociationConfigArgs']]] = None,
                 source_api_identifier: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SourceApiAssociationArgs.__new__(SourceApiAssociationArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["merged_api_identifier"] = merged_api_identifier
            __props__.__dict__["source_api_association_config"] = source_api_association_config
            __props__.__dict__["source_api_identifier"] = source_api_identifier
            __props__.__dict__["association_arn"] = None
            __props__.__dict__["association_id"] = None
            __props__.__dict__["last_successful_merge_date"] = None
            __props__.__dict__["merged_api_arn"] = None
            __props__.__dict__["merged_api_id"] = None
            __props__.__dict__["source_api_arn"] = None
            __props__.__dict__["source_api_association_status"] = None
            __props__.__dict__["source_api_association_status_detail"] = None
            __props__.__dict__["source_api_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["merged_api_identifier", "source_api_identifier"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(SourceApiAssociation, __self__).__init__(
            'aws-native:appsync:SourceApiAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SourceApiAssociation':
        """
        Get an existing SourceApiAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SourceApiAssociationArgs.__new__(SourceApiAssociationArgs)

        __props__.__dict__["association_arn"] = None
        __props__.__dict__["association_id"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["last_successful_merge_date"] = None
        __props__.__dict__["merged_api_arn"] = None
        __props__.__dict__["merged_api_id"] = None
        __props__.__dict__["merged_api_identifier"] = None
        __props__.__dict__["source_api_arn"] = None
        __props__.__dict__["source_api_association_config"] = None
        __props__.__dict__["source_api_association_status"] = None
        __props__.__dict__["source_api_association_status_detail"] = None
        __props__.__dict__["source_api_id"] = None
        __props__.__dict__["source_api_identifier"] = None
        return SourceApiAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="associationArn")
    def association_arn(self) -> pulumi.Output[str]:
        """
        ARN of the SourceApiAssociation.
        """
        return pulumi.get(self, "association_arn")

    @property
    @pulumi.getter(name="associationId")
    def association_id(self) -> pulumi.Output[str]:
        """
        Id of the SourceApiAssociation.
        """
        return pulumi.get(self, "association_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the SourceApiAssociation.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="lastSuccessfulMergeDate")
    def last_successful_merge_date(self) -> pulumi.Output[str]:
        """
        Date of last schema successful merge.
        """
        return pulumi.get(self, "last_successful_merge_date")

    @property
    @pulumi.getter(name="mergedApiArn")
    def merged_api_arn(self) -> pulumi.Output[str]:
        """
        ARN of the Merged API in the association.
        """
        return pulumi.get(self, "merged_api_arn")

    @property
    @pulumi.getter(name="mergedApiId")
    def merged_api_id(self) -> pulumi.Output[str]:
        """
        GraphQLApiId of the Merged API in the association.
        """
        return pulumi.get(self, "merged_api_id")

    @property
    @pulumi.getter(name="mergedApiIdentifier")
    def merged_api_identifier(self) -> pulumi.Output[Optional[str]]:
        """
        Identifier of the Merged GraphQLApi to associate. It could be either GraphQLApi ApiId or ARN
        """
        return pulumi.get(self, "merged_api_identifier")

    @property
    @pulumi.getter(name="sourceApiArn")
    def source_api_arn(self) -> pulumi.Output[str]:
        """
        ARN of the source API in the association.
        """
        return pulumi.get(self, "source_api_arn")

    @property
    @pulumi.getter(name="sourceApiAssociationConfig")
    def source_api_association_config(self) -> pulumi.Output[Optional['outputs.SourceApiAssociationConfig']]:
        """
        Customized configuration for SourceApiAssociation.
        """
        return pulumi.get(self, "source_api_association_config")

    @property
    @pulumi.getter(name="sourceApiAssociationStatus")
    def source_api_association_status(self) -> pulumi.Output['SourceApiAssociationStatus']:
        """
        Current status of SourceApiAssociation.
        """
        return pulumi.get(self, "source_api_association_status")

    @property
    @pulumi.getter(name="sourceApiAssociationStatusDetail")
    def source_api_association_status_detail(self) -> pulumi.Output[str]:
        """
        Current SourceApiAssociation status details.
        """
        return pulumi.get(self, "source_api_association_status_detail")

    @property
    @pulumi.getter(name="sourceApiId")
    def source_api_id(self) -> pulumi.Output[str]:
        """
        GraphQLApiId of the source API in the association.
        """
        return pulumi.get(self, "source_api_id")

    @property
    @pulumi.getter(name="sourceApiIdentifier")
    def source_api_identifier(self) -> pulumi.Output[Optional[str]]:
        """
        Identifier of the Source GraphQLApi to associate. It could be either GraphQLApi ApiId or ARN
        """
        return pulumi.get(self, "source_api_identifier")

