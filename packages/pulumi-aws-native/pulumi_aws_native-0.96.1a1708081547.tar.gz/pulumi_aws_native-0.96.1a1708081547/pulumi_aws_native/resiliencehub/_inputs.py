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

__all__ = [
    'AppEventSubscriptionArgs',
    'AppPermissionModelArgs',
    'AppPhysicalResourceIdArgs',
    'AppResourceMappingArgs',
    'AppTagMapArgs',
    'ResiliencyPolicyPolicyMapArgs',
    'ResiliencyPolicyTagMapArgs',
]

@pulumi.input_type
class AppEventSubscriptionArgs:
    def __init__(__self__, *,
                 event_type: pulumi.Input['AppEventSubscriptionEventType'],
                 name: pulumi.Input[str],
                 sns_topic_arn: Optional[pulumi.Input[str]] = None):
        """
        Indicates an event you would like to subscribe and get notification for.
        :param pulumi.Input['AppEventSubscriptionEventType'] event_type: The type of event you would like to subscribe and get notification for.
        :param pulumi.Input[str] name: Unique name to identify an event subscription.
        :param pulumi.Input[str] sns_topic_arn: Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic.
        """
        pulumi.set(__self__, "event_type", event_type)
        pulumi.set(__self__, "name", name)
        if sns_topic_arn is not None:
            pulumi.set(__self__, "sns_topic_arn", sns_topic_arn)

    @property
    @pulumi.getter(name="eventType")
    def event_type(self) -> pulumi.Input['AppEventSubscriptionEventType']:
        """
        The type of event you would like to subscribe and get notification for.
        """
        return pulumi.get(self, "event_type")

    @event_type.setter
    def event_type(self, value: pulumi.Input['AppEventSubscriptionEventType']):
        pulumi.set(self, "event_type", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Unique name to identify an event subscription.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic.
        """
        return pulumi.get(self, "sns_topic_arn")

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sns_topic_arn", value)


@pulumi.input_type
class AppPermissionModelArgs:
    def __init__(__self__, *,
                 type: pulumi.Input['AppPermissionModelType'],
                 cross_account_role_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 invoker_role_name: Optional[pulumi.Input[str]] = None):
        """
        Defines the roles and credentials that AWS Resilience Hub would use while creating the application, importing its resources, and running an assessment.
        :param pulumi.Input['AppPermissionModelType'] type: Defines how AWS Resilience Hub scans your resources. It can scan for the resources by using a pre-existing role in your AWS account, or by using the credentials of the current IAM user.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] cross_account_role_arns: Defines a list of role Amazon Resource Names (ARNs) to be used in other accounts. These ARNs are used for querying purposes while importing resources and assessing your application.
        :param pulumi.Input[str] invoker_role_name: Existing AWS IAM role name in the primary AWS account that will be assumed by AWS Resilience Hub Service Principle to obtain a read-only access to your application resources while running an assessment.
        """
        pulumi.set(__self__, "type", type)
        if cross_account_role_arns is not None:
            pulumi.set(__self__, "cross_account_role_arns", cross_account_role_arns)
        if invoker_role_name is not None:
            pulumi.set(__self__, "invoker_role_name", invoker_role_name)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['AppPermissionModelType']:
        """
        Defines how AWS Resilience Hub scans your resources. It can scan for the resources by using a pre-existing role in your AWS account, or by using the credentials of the current IAM user.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['AppPermissionModelType']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="crossAccountRoleArns")
    def cross_account_role_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Defines a list of role Amazon Resource Names (ARNs) to be used in other accounts. These ARNs are used for querying purposes while importing resources and assessing your application.
        """
        return pulumi.get(self, "cross_account_role_arns")

    @cross_account_role_arns.setter
    def cross_account_role_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "cross_account_role_arns", value)

    @property
    @pulumi.getter(name="invokerRoleName")
    def invoker_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        Existing AWS IAM role name in the primary AWS account that will be assumed by AWS Resilience Hub Service Principle to obtain a read-only access to your application resources while running an assessment.
        """
        return pulumi.get(self, "invoker_role_name")

    @invoker_role_name.setter
    def invoker_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "invoker_role_name", value)


@pulumi.input_type
class AppPhysicalResourceIdArgs:
    def __init__(__self__, *,
                 identifier: pulumi.Input[str],
                 type: pulumi.Input[str],
                 aws_account_id: Optional[pulumi.Input[str]] = None,
                 aws_region: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "type", type)
        if aws_account_id is not None:
            pulumi.set(__self__, "aws_account_id", aws_account_id)
        if aws_region is not None:
            pulumi.set(__self__, "aws_region", aws_region)

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Input[str]:
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "aws_account_id")

    @aws_account_id.setter
    def aws_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_account_id", value)

    @property
    @pulumi.getter(name="awsRegion")
    def aws_region(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "aws_region")

    @aws_region.setter
    def aws_region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_region", value)


@pulumi.input_type
class AppResourceMappingArgs:
    def __init__(__self__, *,
                 mapping_type: pulumi.Input[str],
                 physical_resource_id: pulumi.Input['AppPhysicalResourceIdArgs'],
                 eks_source_name: Optional[pulumi.Input[str]] = None,
                 logical_stack_name: Optional[pulumi.Input[str]] = None,
                 resource_name: Optional[pulumi.Input[str]] = None,
                 terraform_source_name: Optional[pulumi.Input[str]] = None):
        """
        Resource mapping is used to map logical resources from template to physical resource
        """
        pulumi.set(__self__, "mapping_type", mapping_type)
        pulumi.set(__self__, "physical_resource_id", physical_resource_id)
        if eks_source_name is not None:
            pulumi.set(__self__, "eks_source_name", eks_source_name)
        if logical_stack_name is not None:
            pulumi.set(__self__, "logical_stack_name", logical_stack_name)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if terraform_source_name is not None:
            pulumi.set(__self__, "terraform_source_name", terraform_source_name)

    @property
    @pulumi.getter(name="mappingType")
    def mapping_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "mapping_type")

    @mapping_type.setter
    def mapping_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "mapping_type", value)

    @property
    @pulumi.getter(name="physicalResourceId")
    def physical_resource_id(self) -> pulumi.Input['AppPhysicalResourceIdArgs']:
        return pulumi.get(self, "physical_resource_id")

    @physical_resource_id.setter
    def physical_resource_id(self, value: pulumi.Input['AppPhysicalResourceIdArgs']):
        pulumi.set(self, "physical_resource_id", value)

    @property
    @pulumi.getter(name="eksSourceName")
    def eks_source_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "eks_source_name")

    @eks_source_name.setter
    def eks_source_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "eks_source_name", value)

    @property
    @pulumi.getter(name="logicalStackName")
    def logical_stack_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "logical_stack_name")

    @logical_stack_name.setter
    def logical_stack_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "logical_stack_name", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="terraformSourceName")
    def terraform_source_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "terraform_source_name")

    @terraform_source_name.setter
    def terraform_source_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "terraform_source_name", value)


@pulumi.input_type
class AppTagMapArgs:
    def __init__(__self__):
        pass


@pulumi.input_type
class ResiliencyPolicyPolicyMapArgs:
    def __init__(__self__):
        pass


@pulumi.input_type
class ResiliencyPolicyTagMapArgs:
    def __init__(__self__):
        pass


