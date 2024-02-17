# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AccountAliasArgs', 'AccountAlias']

@pulumi.input_type
class AccountAliasArgs:
    def __init__(__self__, *,
                 account_alias: pulumi.Input[str]):
        """
        The set of arguments for constructing a AccountAlias resource.
        :param pulumi.Input[str] account_alias: An account alias associated with a customer's account.
        """
        pulumi.set(__self__, "account_alias", account_alias)

    @property
    @pulumi.getter(name="accountAlias")
    def account_alias(self) -> pulumi.Input[str]:
        """
        An account alias associated with a customer's account.
        """
        return pulumi.get(self, "account_alias")

    @account_alias.setter
    def account_alias(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_alias", value)


class AccountAlias(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_alias: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An AWS Support App resource that creates, updates, reads, and deletes a customer's account alias.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_alias: An account alias associated with a customer's account.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccountAliasArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An AWS Support App resource that creates, updates, reads, and deletes a customer's account alias.

        :param str resource_name: The name of the resource.
        :param AccountAliasArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountAliasArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_alias: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccountAliasArgs.__new__(AccountAliasArgs)

            if account_alias is None and not opts.urn:
                raise TypeError("Missing required property 'account_alias'")
            __props__.__dict__["account_alias"] = account_alias
            __props__.__dict__["account_alias_resource_id"] = None
        super(AccountAlias, __self__).__init__(
            'aws-native:supportapp:AccountAlias',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AccountAlias':
        """
        Get an existing AccountAlias resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AccountAliasArgs.__new__(AccountAliasArgs)

        __props__.__dict__["account_alias"] = None
        __props__.__dict__["account_alias_resource_id"] = None
        return AccountAlias(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountAlias")
    def account_alias(self) -> pulumi.Output[str]:
        """
        An account alias associated with a customer's account.
        """
        return pulumi.get(self, "account_alias")

    @property
    @pulumi.getter(name="accountAliasResourceId")
    def account_alias_resource_id(self) -> pulumi.Output[str]:
        """
        Unique identifier representing an alias tied to an account
        """
        return pulumi.get(self, "account_alias_resource_id")

