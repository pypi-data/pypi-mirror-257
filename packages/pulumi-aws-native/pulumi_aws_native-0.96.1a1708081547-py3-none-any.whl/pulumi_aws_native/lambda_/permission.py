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

__all__ = ['PermissionArgs', 'Permission']

@pulumi.input_type
class PermissionArgs:
    def __init__(__self__, *,
                 action: pulumi.Input[str],
                 function_name: pulumi.Input[str],
                 principal: pulumi.Input[str],
                 event_source_token: Optional[pulumi.Input[str]] = None,
                 function_url_auth_type: Optional[pulumi.Input['PermissionFunctionUrlAuthType']] = None,
                 principal_org_id: Optional[pulumi.Input[str]] = None,
                 source_account: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Permission resource.
        :param pulumi.Input[str] action: The action that the principal can use on the function.
        :param pulumi.Input[str] function_name: The name of the Lambda function, version, or alias.
        :param pulumi.Input[str] principal: The AWS service or account that invokes the function. If you specify a service, use SourceArn or SourceAccount to limit who can invoke the function through that service.
        :param pulumi.Input[str] event_source_token: For Alexa Smart Home functions, a token that must be supplied by the invoker.
        :param pulumi.Input['PermissionFunctionUrlAuthType'] function_url_auth_type: The type of authentication that your function URL uses. Set to AWS_IAM if you want to restrict access to authenticated users only. Set to NONE if you want to bypass IAM authentication to create a public endpoint.
        :param pulumi.Input[str] principal_org_id: The identifier for your organization in AWS Organizations. Use this to grant permissions to all the AWS accounts under this organization.
        :param pulumi.Input[str] source_account: For Amazon S3, the ID of the account that owns the resource. Use this together with SourceArn to ensure that the resource is owned by the specified account. It is possible for an Amazon S3 bucket to be deleted by its owner and recreated by another account.
        :param pulumi.Input[str] source_arn: For AWS services, the ARN of the AWS resource that invokes the function. For example, an Amazon S3 bucket or Amazon SNS topic.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "function_name", function_name)
        pulumi.set(__self__, "principal", principal)
        if event_source_token is not None:
            pulumi.set(__self__, "event_source_token", event_source_token)
        if function_url_auth_type is not None:
            pulumi.set(__self__, "function_url_auth_type", function_url_auth_type)
        if principal_org_id is not None:
            pulumi.set(__self__, "principal_org_id", principal_org_id)
        if source_account is not None:
            pulumi.set(__self__, "source_account", source_account)
        if source_arn is not None:
            pulumi.set(__self__, "source_arn", source_arn)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input[str]:
        """
        The action that the principal can use on the function.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input[str]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> pulumi.Input[str]:
        """
        The name of the Lambda function, version, or alias.
        """
        return pulumi.get(self, "function_name")

    @function_name.setter
    def function_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "function_name", value)

    @property
    @pulumi.getter
    def principal(self) -> pulumi.Input[str]:
        """
        The AWS service or account that invokes the function. If you specify a service, use SourceArn or SourceAccount to limit who can invoke the function through that service.
        """
        return pulumi.get(self, "principal")

    @principal.setter
    def principal(self, value: pulumi.Input[str]):
        pulumi.set(self, "principal", value)

    @property
    @pulumi.getter(name="eventSourceToken")
    def event_source_token(self) -> Optional[pulumi.Input[str]]:
        """
        For Alexa Smart Home functions, a token that must be supplied by the invoker.
        """
        return pulumi.get(self, "event_source_token")

    @event_source_token.setter
    def event_source_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_source_token", value)

    @property
    @pulumi.getter(name="functionUrlAuthType")
    def function_url_auth_type(self) -> Optional[pulumi.Input['PermissionFunctionUrlAuthType']]:
        """
        The type of authentication that your function URL uses. Set to AWS_IAM if you want to restrict access to authenticated users only. Set to NONE if you want to bypass IAM authentication to create a public endpoint.
        """
        return pulumi.get(self, "function_url_auth_type")

    @function_url_auth_type.setter
    def function_url_auth_type(self, value: Optional[pulumi.Input['PermissionFunctionUrlAuthType']]):
        pulumi.set(self, "function_url_auth_type", value)

    @property
    @pulumi.getter(name="principalOrgId")
    def principal_org_id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier for your organization in AWS Organizations. Use this to grant permissions to all the AWS accounts under this organization.
        """
        return pulumi.get(self, "principal_org_id")

    @principal_org_id.setter
    def principal_org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_org_id", value)

    @property
    @pulumi.getter(name="sourceAccount")
    def source_account(self) -> Optional[pulumi.Input[str]]:
        """
        For Amazon S3, the ID of the account that owns the resource. Use this together with SourceArn to ensure that the resource is owned by the specified account. It is possible for an Amazon S3 bucket to be deleted by its owner and recreated by another account.
        """
        return pulumi.get(self, "source_account")

    @source_account.setter
    def source_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_account", value)

    @property
    @pulumi.getter(name="sourceArn")
    def source_arn(self) -> Optional[pulumi.Input[str]]:
        """
        For AWS services, the ARN of the AWS resource that invokes the function. For example, an Amazon S3 bucket or Amazon SNS topic.
        """
        return pulumi.get(self, "source_arn")

    @source_arn.setter
    def source_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_arn", value)


class Permission(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 event_source_token: Optional[pulumi.Input[str]] = None,
                 function_name: Optional[pulumi.Input[str]] = None,
                 function_url_auth_type: Optional[pulumi.Input['PermissionFunctionUrlAuthType']] = None,
                 principal: Optional[pulumi.Input[str]] = None,
                 principal_org_id: Optional[pulumi.Input[str]] = None,
                 source_account: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Lambda::Permission

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: The action that the principal can use on the function.
        :param pulumi.Input[str] event_source_token: For Alexa Smart Home functions, a token that must be supplied by the invoker.
        :param pulumi.Input[str] function_name: The name of the Lambda function, version, or alias.
        :param pulumi.Input['PermissionFunctionUrlAuthType'] function_url_auth_type: The type of authentication that your function URL uses. Set to AWS_IAM if you want to restrict access to authenticated users only. Set to NONE if you want to bypass IAM authentication to create a public endpoint.
        :param pulumi.Input[str] principal: The AWS service or account that invokes the function. If you specify a service, use SourceArn or SourceAccount to limit who can invoke the function through that service.
        :param pulumi.Input[str] principal_org_id: The identifier for your organization in AWS Organizations. Use this to grant permissions to all the AWS accounts under this organization.
        :param pulumi.Input[str] source_account: For Amazon S3, the ID of the account that owns the resource. Use this together with SourceArn to ensure that the resource is owned by the specified account. It is possible for an Amazon S3 bucket to be deleted by its owner and recreated by another account.
        :param pulumi.Input[str] source_arn: For AWS services, the ARN of the AWS resource that invokes the function. For example, an Amazon S3 bucket or Amazon SNS topic.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PermissionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Lambda::Permission

        :param str resource_name: The name of the resource.
        :param PermissionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PermissionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 event_source_token: Optional[pulumi.Input[str]] = None,
                 function_name: Optional[pulumi.Input[str]] = None,
                 function_url_auth_type: Optional[pulumi.Input['PermissionFunctionUrlAuthType']] = None,
                 principal: Optional[pulumi.Input[str]] = None,
                 principal_org_id: Optional[pulumi.Input[str]] = None,
                 source_account: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PermissionArgs.__new__(PermissionArgs)

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__.__dict__["action"] = action
            __props__.__dict__["event_source_token"] = event_source_token
            if function_name is None and not opts.urn:
                raise TypeError("Missing required property 'function_name'")
            __props__.__dict__["function_name"] = function_name
            __props__.__dict__["function_url_auth_type"] = function_url_auth_type
            if principal is None and not opts.urn:
                raise TypeError("Missing required property 'principal'")
            __props__.__dict__["principal"] = principal
            __props__.__dict__["principal_org_id"] = principal_org_id
            __props__.__dict__["source_account"] = source_account
            __props__.__dict__["source_arn"] = source_arn
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["action", "event_source_token", "function_name", "function_url_auth_type", "principal", "principal_org_id", "source_account", "source_arn"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Permission, __self__).__init__(
            'aws-native:lambda:Permission',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Permission':
        """
        Get an existing Permission resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PermissionArgs.__new__(PermissionArgs)

        __props__.__dict__["action"] = None
        __props__.__dict__["event_source_token"] = None
        __props__.__dict__["function_name"] = None
        __props__.__dict__["function_url_auth_type"] = None
        __props__.__dict__["principal"] = None
        __props__.__dict__["principal_org_id"] = None
        __props__.__dict__["source_account"] = None
        __props__.__dict__["source_arn"] = None
        return Permission(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[str]:
        """
        The action that the principal can use on the function.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="eventSourceToken")
    def event_source_token(self) -> pulumi.Output[Optional[str]]:
        """
        For Alexa Smart Home functions, a token that must be supplied by the invoker.
        """
        return pulumi.get(self, "event_source_token")

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> pulumi.Output[str]:
        """
        The name of the Lambda function, version, or alias.
        """
        return pulumi.get(self, "function_name")

    @property
    @pulumi.getter(name="functionUrlAuthType")
    def function_url_auth_type(self) -> pulumi.Output[Optional['PermissionFunctionUrlAuthType']]:
        """
        The type of authentication that your function URL uses. Set to AWS_IAM if you want to restrict access to authenticated users only. Set to NONE if you want to bypass IAM authentication to create a public endpoint.
        """
        return pulumi.get(self, "function_url_auth_type")

    @property
    @pulumi.getter
    def principal(self) -> pulumi.Output[str]:
        """
        The AWS service or account that invokes the function. If you specify a service, use SourceArn or SourceAccount to limit who can invoke the function through that service.
        """
        return pulumi.get(self, "principal")

    @property
    @pulumi.getter(name="principalOrgId")
    def principal_org_id(self) -> pulumi.Output[Optional[str]]:
        """
        The identifier for your organization in AWS Organizations. Use this to grant permissions to all the AWS accounts under this organization.
        """
        return pulumi.get(self, "principal_org_id")

    @property
    @pulumi.getter(name="sourceAccount")
    def source_account(self) -> pulumi.Output[Optional[str]]:
        """
        For Amazon S3, the ID of the account that owns the resource. Use this together with SourceArn to ensure that the resource is owned by the specified account. It is possible for an Amazon S3 bucket to be deleted by its owner and recreated by another account.
        """
        return pulumi.get(self, "source_account")

    @property
    @pulumi.getter(name="sourceArn")
    def source_arn(self) -> pulumi.Output[Optional[str]]:
        """
        For AWS services, the ARN of the AWS resource that invokes the function. For example, an Amazon S3 bucket or Amazon SNS topic.
        """
        return pulumi.get(self, "source_arn")

