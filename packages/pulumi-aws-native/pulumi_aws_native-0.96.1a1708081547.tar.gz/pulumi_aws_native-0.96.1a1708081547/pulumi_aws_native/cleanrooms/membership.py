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

__all__ = ['MembershipArgs', 'Membership']

@pulumi.input_type
class MembershipArgs:
    def __init__(__self__, *,
                 collaboration_identifier: pulumi.Input[str],
                 query_log_status: pulumi.Input['MembershipQueryLogStatus'],
                 default_result_configuration: Optional[pulumi.Input['MembershipProtectedQueryResultConfigurationArgs']] = None,
                 payment_configuration: Optional[pulumi.Input['MembershipPaymentConfigurationArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['MembershipTagArgs']]]] = None):
        """
        The set of arguments for constructing a Membership resource.
        :param pulumi.Input[Sequence[pulumi.Input['MembershipTagArgs']]] tags: An arbitrary set of tags (key-value pairs) for this cleanrooms membership.
        """
        pulumi.set(__self__, "collaboration_identifier", collaboration_identifier)
        pulumi.set(__self__, "query_log_status", query_log_status)
        if default_result_configuration is not None:
            pulumi.set(__self__, "default_result_configuration", default_result_configuration)
        if payment_configuration is not None:
            pulumi.set(__self__, "payment_configuration", payment_configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="collaborationIdentifier")
    def collaboration_identifier(self) -> pulumi.Input[str]:
        return pulumi.get(self, "collaboration_identifier")

    @collaboration_identifier.setter
    def collaboration_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "collaboration_identifier", value)

    @property
    @pulumi.getter(name="queryLogStatus")
    def query_log_status(self) -> pulumi.Input['MembershipQueryLogStatus']:
        return pulumi.get(self, "query_log_status")

    @query_log_status.setter
    def query_log_status(self, value: pulumi.Input['MembershipQueryLogStatus']):
        pulumi.set(self, "query_log_status", value)

    @property
    @pulumi.getter(name="defaultResultConfiguration")
    def default_result_configuration(self) -> Optional[pulumi.Input['MembershipProtectedQueryResultConfigurationArgs']]:
        return pulumi.get(self, "default_result_configuration")

    @default_result_configuration.setter
    def default_result_configuration(self, value: Optional[pulumi.Input['MembershipProtectedQueryResultConfigurationArgs']]):
        pulumi.set(self, "default_result_configuration", value)

    @property
    @pulumi.getter(name="paymentConfiguration")
    def payment_configuration(self) -> Optional[pulumi.Input['MembershipPaymentConfigurationArgs']]:
        return pulumi.get(self, "payment_configuration")

    @payment_configuration.setter
    def payment_configuration(self, value: Optional[pulumi.Input['MembershipPaymentConfigurationArgs']]):
        pulumi.set(self, "payment_configuration", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MembershipTagArgs']]]]:
        """
        An arbitrary set of tags (key-value pairs) for this cleanrooms membership.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MembershipTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Membership(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 collaboration_identifier: Optional[pulumi.Input[str]] = None,
                 default_result_configuration: Optional[pulumi.Input[pulumi.InputType['MembershipProtectedQueryResultConfigurationArgs']]] = None,
                 payment_configuration: Optional[pulumi.Input[pulumi.InputType['MembershipPaymentConfigurationArgs']]] = None,
                 query_log_status: Optional[pulumi.Input['MembershipQueryLogStatus']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MembershipTagArgs']]]]] = None,
                 __props__=None):
        """
        Represents an AWS account that is a part of a collaboration

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MembershipTagArgs']]]] tags: An arbitrary set of tags (key-value pairs) for this cleanrooms membership.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MembershipArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents an AWS account that is a part of a collaboration

        :param str resource_name: The name of the resource.
        :param MembershipArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MembershipArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 collaboration_identifier: Optional[pulumi.Input[str]] = None,
                 default_result_configuration: Optional[pulumi.Input[pulumi.InputType['MembershipProtectedQueryResultConfigurationArgs']]] = None,
                 payment_configuration: Optional[pulumi.Input[pulumi.InputType['MembershipPaymentConfigurationArgs']]] = None,
                 query_log_status: Optional[pulumi.Input['MembershipQueryLogStatus']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MembershipTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MembershipArgs.__new__(MembershipArgs)

            if collaboration_identifier is None and not opts.urn:
                raise TypeError("Missing required property 'collaboration_identifier'")
            __props__.__dict__["collaboration_identifier"] = collaboration_identifier
            __props__.__dict__["default_result_configuration"] = default_result_configuration
            __props__.__dict__["payment_configuration"] = payment_configuration
            if query_log_status is None and not opts.urn:
                raise TypeError("Missing required property 'query_log_status'")
            __props__.__dict__["query_log_status"] = query_log_status
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["collaboration_arn"] = None
            __props__.__dict__["collaboration_creator_account_id"] = None
            __props__.__dict__["membership_identifier"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["collaboration_identifier"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Membership, __self__).__init__(
            'aws-native:cleanrooms:Membership',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Membership':
        """
        Get an existing Membership resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MembershipArgs.__new__(MembershipArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["collaboration_arn"] = None
        __props__.__dict__["collaboration_creator_account_id"] = None
        __props__.__dict__["collaboration_identifier"] = None
        __props__.__dict__["default_result_configuration"] = None
        __props__.__dict__["membership_identifier"] = None
        __props__.__dict__["payment_configuration"] = None
        __props__.__dict__["query_log_status"] = None
        __props__.__dict__["tags"] = None
        return Membership(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="collaborationArn")
    def collaboration_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "collaboration_arn")

    @property
    @pulumi.getter(name="collaborationCreatorAccountId")
    def collaboration_creator_account_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "collaboration_creator_account_id")

    @property
    @pulumi.getter(name="collaborationIdentifier")
    def collaboration_identifier(self) -> pulumi.Output[str]:
        return pulumi.get(self, "collaboration_identifier")

    @property
    @pulumi.getter(name="defaultResultConfiguration")
    def default_result_configuration(self) -> pulumi.Output[Optional['outputs.MembershipProtectedQueryResultConfiguration']]:
        return pulumi.get(self, "default_result_configuration")

    @property
    @pulumi.getter(name="membershipIdentifier")
    def membership_identifier(self) -> pulumi.Output[str]:
        return pulumi.get(self, "membership_identifier")

    @property
    @pulumi.getter(name="paymentConfiguration")
    def payment_configuration(self) -> pulumi.Output[Optional['outputs.MembershipPaymentConfiguration']]:
        return pulumi.get(self, "payment_configuration")

    @property
    @pulumi.getter(name="queryLogStatus")
    def query_log_status(self) -> pulumi.Output['MembershipQueryLogStatus']:
        return pulumi.get(self, "query_log_status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.MembershipTag']]]:
        """
        An arbitrary set of tags (key-value pairs) for this cleanrooms membership.
        """
        return pulumi.get(self, "tags")

