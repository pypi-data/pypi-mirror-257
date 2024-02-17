# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TargetAccountConfigurationArgs', 'TargetAccountConfiguration']

@pulumi.input_type
class TargetAccountConfigurationArgs:
    def __init__(__self__, *,
                 account_id: pulumi.Input[str],
                 experiment_template_id: pulumi.Input[str],
                 role_arn: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TargetAccountConfiguration resource.
        """
        pulumi.set(__self__, "account_id", account_id)
        pulumi.set(__self__, "experiment_template_id", experiment_template_id)
        pulumi.set(__self__, "role_arn", role_arn)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="experimentTemplateId")
    def experiment_template_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "experiment_template_id")

    @experiment_template_id.setter
    def experiment_template_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "experiment_template_id", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


class TargetAccountConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 experiment_template_id: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource schema for AWS::FIS::TargetAccountConfiguration

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TargetAccountConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::FIS::TargetAccountConfiguration

        :param str resource_name: The name of the resource.
        :param TargetAccountConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TargetAccountConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 experiment_template_id: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TargetAccountConfigurationArgs.__new__(TargetAccountConfigurationArgs)

            if account_id is None and not opts.urn:
                raise TypeError("Missing required property 'account_id'")
            __props__.__dict__["account_id"] = account_id
            __props__.__dict__["description"] = description
            if experiment_template_id is None and not opts.urn:
                raise TypeError("Missing required property 'experiment_template_id'")
            __props__.__dict__["experiment_template_id"] = experiment_template_id
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["account_id", "experiment_template_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(TargetAccountConfiguration, __self__).__init__(
            'aws-native:fis:TargetAccountConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TargetAccountConfiguration':
        """
        Get an existing TargetAccountConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TargetAccountConfigurationArgs.__new__(TargetAccountConfigurationArgs)

        __props__.__dict__["account_id"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["experiment_template_id"] = None
        __props__.__dict__["role_arn"] = None
        return TargetAccountConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="experimentTemplateId")
    def experiment_template_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "experiment_template_id")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "role_arn")

