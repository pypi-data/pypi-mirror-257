# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['MicrosoftTeamsChannelConfigurationArgs', 'MicrosoftTeamsChannelConfiguration']

@pulumi.input_type
class MicrosoftTeamsChannelConfigurationArgs:
    def __init__(__self__, *,
                 configuration_name: pulumi.Input[str],
                 iam_role_arn: pulumi.Input[str],
                 team_id: pulumi.Input[str],
                 teams_channel_id: pulumi.Input[str],
                 teams_tenant_id: pulumi.Input[str],
                 guardrail_policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 logging_level: Optional[pulumi.Input[str]] = None,
                 sns_topic_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 user_role_required: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a MicrosoftTeamsChannelConfiguration resource.
        :param pulumi.Input[str] configuration_name: The name of the configuration
        :param pulumi.Input[str] iam_role_arn: The ARN of the IAM role that defines the permissions for AWS Chatbot
        :param pulumi.Input[str] team_id: The id of the Microsoft Teams team
        :param pulumi.Input[str] teams_channel_id: The id of the Microsoft Teams channel
        :param pulumi.Input[str] teams_tenant_id: The id of the Microsoft Teams tenant
        :param pulumi.Input[Sequence[pulumi.Input[str]]] guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param pulumi.Input[str] logging_level: Specifies the logging level for this configuration:ERROR,INFO or NONE. This property affects the log entries pushed to Amazon CloudWatch logs
        :param pulumi.Input[Sequence[pulumi.Input[str]]] sns_topic_arns: ARNs of SNS topics which delivers notifications to AWS Chatbot, for example CloudWatch alarm notifications.
        :param pulumi.Input[bool] user_role_required: Enables use of a user role requirement in your chat configuration
        """
        pulumi.set(__self__, "configuration_name", configuration_name)
        pulumi.set(__self__, "iam_role_arn", iam_role_arn)
        pulumi.set(__self__, "team_id", team_id)
        pulumi.set(__self__, "teams_channel_id", teams_channel_id)
        pulumi.set(__self__, "teams_tenant_id", teams_tenant_id)
        if guardrail_policies is not None:
            pulumi.set(__self__, "guardrail_policies", guardrail_policies)
        if logging_level is not None:
            pulumi.set(__self__, "logging_level", logging_level)
        if sns_topic_arns is not None:
            pulumi.set(__self__, "sns_topic_arns", sns_topic_arns)
        if user_role_required is not None:
            pulumi.set(__self__, "user_role_required", user_role_required)

    @property
    @pulumi.getter(name="configurationName")
    def configuration_name(self) -> pulumi.Input[str]:
        """
        The name of the configuration
        """
        return pulumi.get(self, "configuration_name")

    @configuration_name.setter
    def configuration_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "configuration_name", value)

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the IAM role that defines the permissions for AWS Chatbot
        """
        return pulumi.get(self, "iam_role_arn")

    @iam_role_arn.setter
    def iam_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "iam_role_arn", value)

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> pulumi.Input[str]:
        """
        The id of the Microsoft Teams team
        """
        return pulumi.get(self, "team_id")

    @team_id.setter
    def team_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "team_id", value)

    @property
    @pulumi.getter(name="teamsChannelId")
    def teams_channel_id(self) -> pulumi.Input[str]:
        """
        The id of the Microsoft Teams channel
        """
        return pulumi.get(self, "teams_channel_id")

    @teams_channel_id.setter
    def teams_channel_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "teams_channel_id", value)

    @property
    @pulumi.getter(name="teamsTenantId")
    def teams_tenant_id(self) -> pulumi.Input[str]:
        """
        The id of the Microsoft Teams tenant
        """
        return pulumi.get(self, "teams_tenant_id")

    @teams_tenant_id.setter
    def teams_tenant_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "teams_tenant_id", value)

    @property
    @pulumi.getter(name="guardrailPolicies")
    def guardrail_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        """
        return pulumi.get(self, "guardrail_policies")

    @guardrail_policies.setter
    def guardrail_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "guardrail_policies", value)

    @property
    @pulumi.getter(name="loggingLevel")
    def logging_level(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the logging level for this configuration:ERROR,INFO or NONE. This property affects the log entries pushed to Amazon CloudWatch logs
        """
        return pulumi.get(self, "logging_level")

    @logging_level.setter
    def logging_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "logging_level", value)

    @property
    @pulumi.getter(name="snsTopicArns")
    def sns_topic_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        ARNs of SNS topics which delivers notifications to AWS Chatbot, for example CloudWatch alarm notifications.
        """
        return pulumi.get(self, "sns_topic_arns")

    @sns_topic_arns.setter
    def sns_topic_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "sns_topic_arns", value)

    @property
    @pulumi.getter(name="userRoleRequired")
    def user_role_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables use of a user role requirement in your chat configuration
        """
        return pulumi.get(self, "user_role_required")

    @user_role_required.setter
    def user_role_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "user_role_required", value)


class MicrosoftTeamsChannelConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_name: Optional[pulumi.Input[str]] = None,
                 guardrail_policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 iam_role_arn: Optional[pulumi.Input[str]] = None,
                 logging_level: Optional[pulumi.Input[str]] = None,
                 sns_topic_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 teams_channel_id: Optional[pulumi.Input[str]] = None,
                 teams_tenant_id: Optional[pulumi.Input[str]] = None,
                 user_role_required: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Resource schema for AWS::Chatbot::MicrosoftTeamsChannelConfiguration.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configuration_name: The name of the configuration
        :param pulumi.Input[Sequence[pulumi.Input[str]]] guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param pulumi.Input[str] iam_role_arn: The ARN of the IAM role that defines the permissions for AWS Chatbot
        :param pulumi.Input[str] logging_level: Specifies the logging level for this configuration:ERROR,INFO or NONE. This property affects the log entries pushed to Amazon CloudWatch logs
        :param pulumi.Input[Sequence[pulumi.Input[str]]] sns_topic_arns: ARNs of SNS topics which delivers notifications to AWS Chatbot, for example CloudWatch alarm notifications.
        :param pulumi.Input[str] team_id: The id of the Microsoft Teams team
        :param pulumi.Input[str] teams_channel_id: The id of the Microsoft Teams channel
        :param pulumi.Input[str] teams_tenant_id: The id of the Microsoft Teams tenant
        :param pulumi.Input[bool] user_role_required: Enables use of a user role requirement in your chat configuration
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MicrosoftTeamsChannelConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::Chatbot::MicrosoftTeamsChannelConfiguration.

        :param str resource_name: The name of the resource.
        :param MicrosoftTeamsChannelConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MicrosoftTeamsChannelConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_name: Optional[pulumi.Input[str]] = None,
                 guardrail_policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 iam_role_arn: Optional[pulumi.Input[str]] = None,
                 logging_level: Optional[pulumi.Input[str]] = None,
                 sns_topic_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 teams_channel_id: Optional[pulumi.Input[str]] = None,
                 teams_tenant_id: Optional[pulumi.Input[str]] = None,
                 user_role_required: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MicrosoftTeamsChannelConfigurationArgs.__new__(MicrosoftTeamsChannelConfigurationArgs)

            if configuration_name is None and not opts.urn:
                raise TypeError("Missing required property 'configuration_name'")
            __props__.__dict__["configuration_name"] = configuration_name
            __props__.__dict__["guardrail_policies"] = guardrail_policies
            if iam_role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'iam_role_arn'")
            __props__.__dict__["iam_role_arn"] = iam_role_arn
            __props__.__dict__["logging_level"] = logging_level
            __props__.__dict__["sns_topic_arns"] = sns_topic_arns
            if team_id is None and not opts.urn:
                raise TypeError("Missing required property 'team_id'")
            __props__.__dict__["team_id"] = team_id
            if teams_channel_id is None and not opts.urn:
                raise TypeError("Missing required property 'teams_channel_id'")
            __props__.__dict__["teams_channel_id"] = teams_channel_id
            if teams_tenant_id is None and not opts.urn:
                raise TypeError("Missing required property 'teams_tenant_id'")
            __props__.__dict__["teams_tenant_id"] = teams_tenant_id
            __props__.__dict__["user_role_required"] = user_role_required
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["configuration_name", "team_id", "teams_tenant_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(MicrosoftTeamsChannelConfiguration, __self__).__init__(
            'aws-native:chatbot:MicrosoftTeamsChannelConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MicrosoftTeamsChannelConfiguration':
        """
        Get an existing MicrosoftTeamsChannelConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MicrosoftTeamsChannelConfigurationArgs.__new__(MicrosoftTeamsChannelConfigurationArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["configuration_name"] = None
        __props__.__dict__["guardrail_policies"] = None
        __props__.__dict__["iam_role_arn"] = None
        __props__.__dict__["logging_level"] = None
        __props__.__dict__["sns_topic_arns"] = None
        __props__.__dict__["team_id"] = None
        __props__.__dict__["teams_channel_id"] = None
        __props__.__dict__["teams_tenant_id"] = None
        __props__.__dict__["user_role_required"] = None
        return MicrosoftTeamsChannelConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the configuration
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="configurationName")
    def configuration_name(self) -> pulumi.Output[str]:
        """
        The name of the configuration
        """
        return pulumi.get(self, "configuration_name")

    @property
    @pulumi.getter(name="guardrailPolicies")
    def guardrail_policies(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        """
        return pulumi.get(self, "guardrail_policies")

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the IAM role that defines the permissions for AWS Chatbot
        """
        return pulumi.get(self, "iam_role_arn")

    @property
    @pulumi.getter(name="loggingLevel")
    def logging_level(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the logging level for this configuration:ERROR,INFO or NONE. This property affects the log entries pushed to Amazon CloudWatch logs
        """
        return pulumi.get(self, "logging_level")

    @property
    @pulumi.getter(name="snsTopicArns")
    def sns_topic_arns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        ARNs of SNS topics which delivers notifications to AWS Chatbot, for example CloudWatch alarm notifications.
        """
        return pulumi.get(self, "sns_topic_arns")

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> pulumi.Output[str]:
        """
        The id of the Microsoft Teams team
        """
        return pulumi.get(self, "team_id")

    @property
    @pulumi.getter(name="teamsChannelId")
    def teams_channel_id(self) -> pulumi.Output[str]:
        """
        The id of the Microsoft Teams channel
        """
        return pulumi.get(self, "teams_channel_id")

    @property
    @pulumi.getter(name="teamsTenantId")
    def teams_tenant_id(self) -> pulumi.Output[str]:
        """
        The id of the Microsoft Teams tenant
        """
        return pulumi.get(self, "teams_tenant_id")

    @property
    @pulumi.getter(name="userRoleRequired")
    def user_role_required(self) -> pulumi.Output[Optional[bool]]:
        """
        Enables use of a user role requirement in your chat configuration
        """
        return pulumi.get(self, "user_role_required")

