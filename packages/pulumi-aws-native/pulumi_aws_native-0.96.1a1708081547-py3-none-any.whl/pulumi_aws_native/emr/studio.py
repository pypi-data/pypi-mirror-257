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

__all__ = ['StudioArgs', 'Studio']

@pulumi.input_type
class StudioArgs:
    def __init__(__self__, *,
                 auth_mode: pulumi.Input['StudioAuthMode'],
                 default_s3_location: pulumi.Input[str],
                 engine_security_group_id: pulumi.Input[str],
                 service_role: pulumi.Input[str],
                 subnet_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 vpc_id: pulumi.Input[str],
                 workspace_security_group_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_key_arn: Optional[pulumi.Input[str]] = None,
                 idc_instance_arn: Optional[pulumi.Input[str]] = None,
                 idc_user_assignment: Optional[pulumi.Input['StudioIdcUserAssignment']] = None,
                 idp_auth_url: Optional[pulumi.Input[str]] = None,
                 idp_relay_state_parameter_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['StudioTagArgs']]]] = None,
                 trusted_identity_propagation_enabled: Optional[pulumi.Input[bool]] = None,
                 user_role: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Studio resource.
        :param pulumi.Input['StudioAuthMode'] auth_mode: Specifies whether the Studio authenticates users using single sign-on (SSO) or IAM. Amazon EMR Studio currently only supports SSO authentication.
        :param pulumi.Input[str] default_s3_location: The default Amazon S3 location to back up EMR Studio Workspaces and notebook files. A Studio user can select an alternative Amazon S3 location when creating a Workspace.
        :param pulumi.Input[str] engine_security_group_id: The ID of the Amazon EMR Studio Engine security group. The Engine security group allows inbound network traffic from the Workspace security group, and it must be in the same VPC specified by VpcId.
        :param pulumi.Input[str] service_role: The IAM role that will be assumed by the Amazon EMR Studio. The service role provides a way for Amazon EMR Studio to interoperate with other AWS services.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: A list of up to 5 subnet IDs to associate with the Studio. The subnets must belong to the VPC specified by VpcId. Studio users can create a Workspace in any of the specified subnets.
        :param pulumi.Input[str] vpc_id: The ID of the Amazon Virtual Private Cloud (Amazon VPC) to associate with the Studio.
        :param pulumi.Input[str] workspace_security_group_id: The ID of the Amazon EMR Studio Workspace security group. The Workspace security group allows outbound network traffic to resources in the Engine security group, and it must be in the same VPC specified by VpcId.
        :param pulumi.Input[str] description: A detailed description of the Studio.
        :param pulumi.Input[str] encryption_key_arn: The AWS KMS key identifier (ARN) used to encrypt AWS EMR Studio workspace and notebook files when backed up to AWS S3.
        :param pulumi.Input[str] idc_instance_arn: The ARN of the IAM Identity Center instance to create the Studio application.
        :param pulumi.Input['StudioIdcUserAssignment'] idc_user_assignment: Specifies whether IAM Identity Center user assignment is REQUIRED or OPTIONAL. If the value is set to REQUIRED, users must be explicitly assigned to the Studio application to access the Studio.
        :param pulumi.Input[str] idp_auth_url: Your identity provider's authentication endpoint. Amazon EMR Studio redirects federated users to this endpoint for authentication when logging in to a Studio with the Studio URL.
        :param pulumi.Input[str] idp_relay_state_parameter_name: The name of relay state parameter for external Identity Provider.
        :param pulumi.Input[str] name: A descriptive name for the Amazon EMR Studio.
        :param pulumi.Input[Sequence[pulumi.Input['StudioTagArgs']]] tags: A list of tags to associate with the Studio. Tags are user-defined key-value pairs that consist of a required key string with a maximum of 128 characters, and an optional value string with a maximum of 256 characters.
        :param pulumi.Input[bool] trusted_identity_propagation_enabled: A Boolean indicating whether to enable Trusted identity propagation for the Studio. The default value is false.
        :param pulumi.Input[str] user_role: The IAM user role that will be assumed by users and groups logged in to a Studio. The permissions attached to this IAM role can be scoped down for each user or group using session policies.
        """
        pulumi.set(__self__, "auth_mode", auth_mode)
        pulumi.set(__self__, "default_s3_location", default_s3_location)
        pulumi.set(__self__, "engine_security_group_id", engine_security_group_id)
        pulumi.set(__self__, "service_role", service_role)
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        pulumi.set(__self__, "vpc_id", vpc_id)
        pulumi.set(__self__, "workspace_security_group_id", workspace_security_group_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encryption_key_arn is not None:
            pulumi.set(__self__, "encryption_key_arn", encryption_key_arn)
        if idc_instance_arn is not None:
            pulumi.set(__self__, "idc_instance_arn", idc_instance_arn)
        if idc_user_assignment is not None:
            pulumi.set(__self__, "idc_user_assignment", idc_user_assignment)
        if idp_auth_url is not None:
            pulumi.set(__self__, "idp_auth_url", idp_auth_url)
        if idp_relay_state_parameter_name is not None:
            pulumi.set(__self__, "idp_relay_state_parameter_name", idp_relay_state_parameter_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if trusted_identity_propagation_enabled is not None:
            pulumi.set(__self__, "trusted_identity_propagation_enabled", trusted_identity_propagation_enabled)
        if user_role is not None:
            pulumi.set(__self__, "user_role", user_role)

    @property
    @pulumi.getter(name="authMode")
    def auth_mode(self) -> pulumi.Input['StudioAuthMode']:
        """
        Specifies whether the Studio authenticates users using single sign-on (SSO) or IAM. Amazon EMR Studio currently only supports SSO authentication.
        """
        return pulumi.get(self, "auth_mode")

    @auth_mode.setter
    def auth_mode(self, value: pulumi.Input['StudioAuthMode']):
        pulumi.set(self, "auth_mode", value)

    @property
    @pulumi.getter(name="defaultS3Location")
    def default_s3_location(self) -> pulumi.Input[str]:
        """
        The default Amazon S3 location to back up EMR Studio Workspaces and notebook files. A Studio user can select an alternative Amazon S3 location when creating a Workspace.
        """
        return pulumi.get(self, "default_s3_location")

    @default_s3_location.setter
    def default_s3_location(self, value: pulumi.Input[str]):
        pulumi.set(self, "default_s3_location", value)

    @property
    @pulumi.getter(name="engineSecurityGroupId")
    def engine_security_group_id(self) -> pulumi.Input[str]:
        """
        The ID of the Amazon EMR Studio Engine security group. The Engine security group allows inbound network traffic from the Workspace security group, and it must be in the same VPC specified by VpcId.
        """
        return pulumi.get(self, "engine_security_group_id")

    @engine_security_group_id.setter
    def engine_security_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "engine_security_group_id", value)

    @property
    @pulumi.getter(name="serviceRole")
    def service_role(self) -> pulumi.Input[str]:
        """
        The IAM role that will be assumed by the Amazon EMR Studio. The service role provides a way for Amazon EMR Studio to interoperate with other AWS services.
        """
        return pulumi.get(self, "service_role")

    @service_role.setter
    def service_role(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_role", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of up to 5 subnet IDs to associate with the Studio. The subnets must belong to the VPC specified by VpcId. Studio users can create a Workspace in any of the specified subnets.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "subnet_ids", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The ID of the Amazon Virtual Private Cloud (Amazon VPC) to associate with the Studio.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter(name="workspaceSecurityGroupId")
    def workspace_security_group_id(self) -> pulumi.Input[str]:
        """
        The ID of the Amazon EMR Studio Workspace security group. The Workspace security group allows outbound network traffic to resources in the Engine security group, and it must be in the same VPC specified by VpcId.
        """
        return pulumi.get(self, "workspace_security_group_id")

    @workspace_security_group_id.setter
    def workspace_security_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_security_group_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A detailed description of the Studio.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="encryptionKeyArn")
    def encryption_key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS KMS key identifier (ARN) used to encrypt AWS EMR Studio workspace and notebook files when backed up to AWS S3.
        """
        return pulumi.get(self, "encryption_key_arn")

    @encryption_key_arn.setter
    def encryption_key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encryption_key_arn", value)

    @property
    @pulumi.getter(name="idcInstanceArn")
    def idc_instance_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the IAM Identity Center instance to create the Studio application.
        """
        return pulumi.get(self, "idc_instance_arn")

    @idc_instance_arn.setter
    def idc_instance_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "idc_instance_arn", value)

    @property
    @pulumi.getter(name="idcUserAssignment")
    def idc_user_assignment(self) -> Optional[pulumi.Input['StudioIdcUserAssignment']]:
        """
        Specifies whether IAM Identity Center user assignment is REQUIRED or OPTIONAL. If the value is set to REQUIRED, users must be explicitly assigned to the Studio application to access the Studio.
        """
        return pulumi.get(self, "idc_user_assignment")

    @idc_user_assignment.setter
    def idc_user_assignment(self, value: Optional[pulumi.Input['StudioIdcUserAssignment']]):
        pulumi.set(self, "idc_user_assignment", value)

    @property
    @pulumi.getter(name="idpAuthUrl")
    def idp_auth_url(self) -> Optional[pulumi.Input[str]]:
        """
        Your identity provider's authentication endpoint. Amazon EMR Studio redirects federated users to this endpoint for authentication when logging in to a Studio with the Studio URL.
        """
        return pulumi.get(self, "idp_auth_url")

    @idp_auth_url.setter
    def idp_auth_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "idp_auth_url", value)

    @property
    @pulumi.getter(name="idpRelayStateParameterName")
    def idp_relay_state_parameter_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of relay state parameter for external Identity Provider.
        """
        return pulumi.get(self, "idp_relay_state_parameter_name")

    @idp_relay_state_parameter_name.setter
    def idp_relay_state_parameter_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "idp_relay_state_parameter_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A descriptive name for the Amazon EMR Studio.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StudioTagArgs']]]]:
        """
        A list of tags to associate with the Studio. Tags are user-defined key-value pairs that consist of a required key string with a maximum of 128 characters, and an optional value string with a maximum of 256 characters.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StudioTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="trustedIdentityPropagationEnabled")
    def trusted_identity_propagation_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        A Boolean indicating whether to enable Trusted identity propagation for the Studio. The default value is false.
        """
        return pulumi.get(self, "trusted_identity_propagation_enabled")

    @trusted_identity_propagation_enabled.setter
    def trusted_identity_propagation_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "trusted_identity_propagation_enabled", value)

    @property
    @pulumi.getter(name="userRole")
    def user_role(self) -> Optional[pulumi.Input[str]]:
        """
        The IAM user role that will be assumed by users and groups logged in to a Studio. The permissions attached to this IAM role can be scoped down for each user or group using session policies.
        """
        return pulumi.get(self, "user_role")

    @user_role.setter
    def user_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_role", value)


class Studio(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auth_mode: Optional[pulumi.Input['StudioAuthMode']] = None,
                 default_s3_location: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_key_arn: Optional[pulumi.Input[str]] = None,
                 engine_security_group_id: Optional[pulumi.Input[str]] = None,
                 idc_instance_arn: Optional[pulumi.Input[str]] = None,
                 idc_user_assignment: Optional[pulumi.Input['StudioIdcUserAssignment']] = None,
                 idp_auth_url: Optional[pulumi.Input[str]] = None,
                 idp_relay_state_parameter_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service_role: Optional[pulumi.Input[str]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StudioTagArgs']]]]] = None,
                 trusted_identity_propagation_enabled: Optional[pulumi.Input[bool]] = None,
                 user_role: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 workspace_security_group_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource schema for AWS::EMR::Studio

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input['StudioAuthMode'] auth_mode: Specifies whether the Studio authenticates users using single sign-on (SSO) or IAM. Amazon EMR Studio currently only supports SSO authentication.
        :param pulumi.Input[str] default_s3_location: The default Amazon S3 location to back up EMR Studio Workspaces and notebook files. A Studio user can select an alternative Amazon S3 location when creating a Workspace.
        :param pulumi.Input[str] description: A detailed description of the Studio.
        :param pulumi.Input[str] encryption_key_arn: The AWS KMS key identifier (ARN) used to encrypt AWS EMR Studio workspace and notebook files when backed up to AWS S3.
        :param pulumi.Input[str] engine_security_group_id: The ID of the Amazon EMR Studio Engine security group. The Engine security group allows inbound network traffic from the Workspace security group, and it must be in the same VPC specified by VpcId.
        :param pulumi.Input[str] idc_instance_arn: The ARN of the IAM Identity Center instance to create the Studio application.
        :param pulumi.Input['StudioIdcUserAssignment'] idc_user_assignment: Specifies whether IAM Identity Center user assignment is REQUIRED or OPTIONAL. If the value is set to REQUIRED, users must be explicitly assigned to the Studio application to access the Studio.
        :param pulumi.Input[str] idp_auth_url: Your identity provider's authentication endpoint. Amazon EMR Studio redirects federated users to this endpoint for authentication when logging in to a Studio with the Studio URL.
        :param pulumi.Input[str] idp_relay_state_parameter_name: The name of relay state parameter for external Identity Provider.
        :param pulumi.Input[str] name: A descriptive name for the Amazon EMR Studio.
        :param pulumi.Input[str] service_role: The IAM role that will be assumed by the Amazon EMR Studio. The service role provides a way for Amazon EMR Studio to interoperate with other AWS services.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: A list of up to 5 subnet IDs to associate with the Studio. The subnets must belong to the VPC specified by VpcId. Studio users can create a Workspace in any of the specified subnets.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StudioTagArgs']]]] tags: A list of tags to associate with the Studio. Tags are user-defined key-value pairs that consist of a required key string with a maximum of 128 characters, and an optional value string with a maximum of 256 characters.
        :param pulumi.Input[bool] trusted_identity_propagation_enabled: A Boolean indicating whether to enable Trusted identity propagation for the Studio. The default value is false.
        :param pulumi.Input[str] user_role: The IAM user role that will be assumed by users and groups logged in to a Studio. The permissions attached to this IAM role can be scoped down for each user or group using session policies.
        :param pulumi.Input[str] vpc_id: The ID of the Amazon Virtual Private Cloud (Amazon VPC) to associate with the Studio.
        :param pulumi.Input[str] workspace_security_group_id: The ID of the Amazon EMR Studio Workspace security group. The Workspace security group allows outbound network traffic to resources in the Engine security group, and it must be in the same VPC specified by VpcId.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StudioArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::EMR::Studio

        :param str resource_name: The name of the resource.
        :param StudioArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StudioArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auth_mode: Optional[pulumi.Input['StudioAuthMode']] = None,
                 default_s3_location: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_key_arn: Optional[pulumi.Input[str]] = None,
                 engine_security_group_id: Optional[pulumi.Input[str]] = None,
                 idc_instance_arn: Optional[pulumi.Input[str]] = None,
                 idc_user_assignment: Optional[pulumi.Input['StudioIdcUserAssignment']] = None,
                 idp_auth_url: Optional[pulumi.Input[str]] = None,
                 idp_relay_state_parameter_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service_role: Optional[pulumi.Input[str]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StudioTagArgs']]]]] = None,
                 trusted_identity_propagation_enabled: Optional[pulumi.Input[bool]] = None,
                 user_role: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 workspace_security_group_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = StudioArgs.__new__(StudioArgs)

            if auth_mode is None and not opts.urn:
                raise TypeError("Missing required property 'auth_mode'")
            __props__.__dict__["auth_mode"] = auth_mode
            if default_s3_location is None and not opts.urn:
                raise TypeError("Missing required property 'default_s3_location'")
            __props__.__dict__["default_s3_location"] = default_s3_location
            __props__.__dict__["description"] = description
            __props__.__dict__["encryption_key_arn"] = encryption_key_arn
            if engine_security_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'engine_security_group_id'")
            __props__.__dict__["engine_security_group_id"] = engine_security_group_id
            __props__.__dict__["idc_instance_arn"] = idc_instance_arn
            __props__.__dict__["idc_user_assignment"] = idc_user_assignment
            __props__.__dict__["idp_auth_url"] = idp_auth_url
            __props__.__dict__["idp_relay_state_parameter_name"] = idp_relay_state_parameter_name
            __props__.__dict__["name"] = name
            if service_role is None and not opts.urn:
                raise TypeError("Missing required property 'service_role'")
            __props__.__dict__["service_role"] = service_role
            if subnet_ids is None and not opts.urn:
                raise TypeError("Missing required property 'subnet_ids'")
            __props__.__dict__["subnet_ids"] = subnet_ids
            __props__.__dict__["tags"] = tags
            __props__.__dict__["trusted_identity_propagation_enabled"] = trusted_identity_propagation_enabled
            __props__.__dict__["user_role"] = user_role
            if vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__["vpc_id"] = vpc_id
            if workspace_security_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_security_group_id'")
            __props__.__dict__["workspace_security_group_id"] = workspace_security_group_id
            __props__.__dict__["arn"] = None
            __props__.__dict__["studio_id"] = None
            __props__.__dict__["url"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["auth_mode", "encryption_key_arn", "engine_security_group_id", "idc_instance_arn", "idc_user_assignment", "service_role", "trusted_identity_propagation_enabled", "user_role", "vpc_id", "workspace_security_group_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Studio, __self__).__init__(
            'aws-native:emr:Studio',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Studio':
        """
        Get an existing Studio resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StudioArgs.__new__(StudioArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["auth_mode"] = None
        __props__.__dict__["default_s3_location"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["encryption_key_arn"] = None
        __props__.__dict__["engine_security_group_id"] = None
        __props__.__dict__["idc_instance_arn"] = None
        __props__.__dict__["idc_user_assignment"] = None
        __props__.__dict__["idp_auth_url"] = None
        __props__.__dict__["idp_relay_state_parameter_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["service_role"] = None
        __props__.__dict__["studio_id"] = None
        __props__.__dict__["subnet_ids"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["trusted_identity_propagation_enabled"] = None
        __props__.__dict__["url"] = None
        __props__.__dict__["user_role"] = None
        __props__.__dict__["vpc_id"] = None
        __props__.__dict__["workspace_security_group_id"] = None
        return Studio(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the EMR Studio.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="authMode")
    def auth_mode(self) -> pulumi.Output['StudioAuthMode']:
        """
        Specifies whether the Studio authenticates users using single sign-on (SSO) or IAM. Amazon EMR Studio currently only supports SSO authentication.
        """
        return pulumi.get(self, "auth_mode")

    @property
    @pulumi.getter(name="defaultS3Location")
    def default_s3_location(self) -> pulumi.Output[str]:
        """
        The default Amazon S3 location to back up EMR Studio Workspaces and notebook files. A Studio user can select an alternative Amazon S3 location when creating a Workspace.
        """
        return pulumi.get(self, "default_s3_location")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A detailed description of the Studio.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="encryptionKeyArn")
    def encryption_key_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The AWS KMS key identifier (ARN) used to encrypt AWS EMR Studio workspace and notebook files when backed up to AWS S3.
        """
        return pulumi.get(self, "encryption_key_arn")

    @property
    @pulumi.getter(name="engineSecurityGroupId")
    def engine_security_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the Amazon EMR Studio Engine security group. The Engine security group allows inbound network traffic from the Workspace security group, and it must be in the same VPC specified by VpcId.
        """
        return pulumi.get(self, "engine_security_group_id")

    @property
    @pulumi.getter(name="idcInstanceArn")
    def idc_instance_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The ARN of the IAM Identity Center instance to create the Studio application.
        """
        return pulumi.get(self, "idc_instance_arn")

    @property
    @pulumi.getter(name="idcUserAssignment")
    def idc_user_assignment(self) -> pulumi.Output[Optional['StudioIdcUserAssignment']]:
        """
        Specifies whether IAM Identity Center user assignment is REQUIRED or OPTIONAL. If the value is set to REQUIRED, users must be explicitly assigned to the Studio application to access the Studio.
        """
        return pulumi.get(self, "idc_user_assignment")

    @property
    @pulumi.getter(name="idpAuthUrl")
    def idp_auth_url(self) -> pulumi.Output[Optional[str]]:
        """
        Your identity provider's authentication endpoint. Amazon EMR Studio redirects federated users to this endpoint for authentication when logging in to a Studio with the Studio URL.
        """
        return pulumi.get(self, "idp_auth_url")

    @property
    @pulumi.getter(name="idpRelayStateParameterName")
    def idp_relay_state_parameter_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of relay state parameter for external Identity Provider.
        """
        return pulumi.get(self, "idp_relay_state_parameter_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A descriptive name for the Amazon EMR Studio.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serviceRole")
    def service_role(self) -> pulumi.Output[str]:
        """
        The IAM role that will be assumed by the Amazon EMR Studio. The service role provides a way for Amazon EMR Studio to interoperate with other AWS services.
        """
        return pulumi.get(self, "service_role")

    @property
    @pulumi.getter(name="studioId")
    def studio_id(self) -> pulumi.Output[str]:
        """
        The ID of the EMR Studio.
        """
        return pulumi.get(self, "studio_id")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of up to 5 subnet IDs to associate with the Studio. The subnets must belong to the VPC specified by VpcId. Studio users can create a Workspace in any of the specified subnets.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.StudioTag']]]:
        """
        A list of tags to associate with the Studio. Tags are user-defined key-value pairs that consist of a required key string with a maximum of 128 characters, and an optional value string with a maximum of 256 characters.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="trustedIdentityPropagationEnabled")
    def trusted_identity_propagation_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        A Boolean indicating whether to enable Trusted identity propagation for the Studio. The default value is false.
        """
        return pulumi.get(self, "trusted_identity_propagation_enabled")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        The unique Studio access URL.
        """
        return pulumi.get(self, "url")

    @property
    @pulumi.getter(name="userRole")
    def user_role(self) -> pulumi.Output[Optional[str]]:
        """
        The IAM user role that will be assumed by users and groups logged in to a Studio. The permissions attached to this IAM role can be scoped down for each user or group using session policies.
        """
        return pulumi.get(self, "user_role")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The ID of the Amazon Virtual Private Cloud (Amazon VPC) to associate with the Studio.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="workspaceSecurityGroupId")
    def workspace_security_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the Amazon EMR Studio Workspace security group. The Workspace security group allows outbound network traffic to resources in the Engine security group, and it must be in the same VPC specified by VpcId.
        """
        return pulumi.get(self, "workspace_security_group_id")

