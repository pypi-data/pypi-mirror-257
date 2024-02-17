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

__all__ = ['DbProxyTargetGroupArgs', 'DbProxyTargetGroup']

@pulumi.input_type
class DbProxyTargetGroupArgs:
    def __init__(__self__, *,
                 db_proxy_name: pulumi.Input[str],
                 target_group_name: pulumi.Input['DbProxyTargetGroupTargetGroupName'],
                 connection_pool_configuration_info: Optional[pulumi.Input['DbProxyTargetGroupConnectionPoolConfigurationInfoFormatArgs']] = None,
                 db_cluster_identifiers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 db_instance_identifiers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a DbProxyTargetGroup resource.
        :param pulumi.Input[str] db_proxy_name: The identifier for the proxy.
        :param pulumi.Input['DbProxyTargetGroupTargetGroupName'] target_group_name: The identifier for the DBProxyTargetGroup
        """
        pulumi.set(__self__, "db_proxy_name", db_proxy_name)
        pulumi.set(__self__, "target_group_name", target_group_name)
        if connection_pool_configuration_info is not None:
            pulumi.set(__self__, "connection_pool_configuration_info", connection_pool_configuration_info)
        if db_cluster_identifiers is not None:
            pulumi.set(__self__, "db_cluster_identifiers", db_cluster_identifiers)
        if db_instance_identifiers is not None:
            pulumi.set(__self__, "db_instance_identifiers", db_instance_identifiers)

    @property
    @pulumi.getter(name="dbProxyName")
    def db_proxy_name(self) -> pulumi.Input[str]:
        """
        The identifier for the proxy.
        """
        return pulumi.get(self, "db_proxy_name")

    @db_proxy_name.setter
    def db_proxy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_proxy_name", value)

    @property
    @pulumi.getter(name="targetGroupName")
    def target_group_name(self) -> pulumi.Input['DbProxyTargetGroupTargetGroupName']:
        """
        The identifier for the DBProxyTargetGroup
        """
        return pulumi.get(self, "target_group_name")

    @target_group_name.setter
    def target_group_name(self, value: pulumi.Input['DbProxyTargetGroupTargetGroupName']):
        pulumi.set(self, "target_group_name", value)

    @property
    @pulumi.getter(name="connectionPoolConfigurationInfo")
    def connection_pool_configuration_info(self) -> Optional[pulumi.Input['DbProxyTargetGroupConnectionPoolConfigurationInfoFormatArgs']]:
        return pulumi.get(self, "connection_pool_configuration_info")

    @connection_pool_configuration_info.setter
    def connection_pool_configuration_info(self, value: Optional[pulumi.Input['DbProxyTargetGroupConnectionPoolConfigurationInfoFormatArgs']]):
        pulumi.set(self, "connection_pool_configuration_info", value)

    @property
    @pulumi.getter(name="dbClusterIdentifiers")
    def db_cluster_identifiers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "db_cluster_identifiers")

    @db_cluster_identifiers.setter
    def db_cluster_identifiers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "db_cluster_identifiers", value)

    @property
    @pulumi.getter(name="dbInstanceIdentifiers")
    def db_instance_identifiers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "db_instance_identifiers")

    @db_instance_identifiers.setter
    def db_instance_identifiers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "db_instance_identifiers", value)


class DbProxyTargetGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_pool_configuration_info: Optional[pulumi.Input[pulumi.InputType['DbProxyTargetGroupConnectionPoolConfigurationInfoFormatArgs']]] = None,
                 db_cluster_identifiers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 db_instance_identifiers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 db_proxy_name: Optional[pulumi.Input[str]] = None,
                 target_group_name: Optional[pulumi.Input['DbProxyTargetGroupTargetGroupName']] = None,
                 __props__=None):
        """
        Resource schema for AWS::RDS::DBProxyTargetGroup

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_proxy_name: The identifier for the proxy.
        :param pulumi.Input['DbProxyTargetGroupTargetGroupName'] target_group_name: The identifier for the DBProxyTargetGroup
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DbProxyTargetGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::RDS::DBProxyTargetGroup

        :param str resource_name: The name of the resource.
        :param DbProxyTargetGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DbProxyTargetGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_pool_configuration_info: Optional[pulumi.Input[pulumi.InputType['DbProxyTargetGroupConnectionPoolConfigurationInfoFormatArgs']]] = None,
                 db_cluster_identifiers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 db_instance_identifiers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 db_proxy_name: Optional[pulumi.Input[str]] = None,
                 target_group_name: Optional[pulumi.Input['DbProxyTargetGroupTargetGroupName']] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DbProxyTargetGroupArgs.__new__(DbProxyTargetGroupArgs)

            __props__.__dict__["connection_pool_configuration_info"] = connection_pool_configuration_info
            __props__.__dict__["db_cluster_identifiers"] = db_cluster_identifiers
            __props__.__dict__["db_instance_identifiers"] = db_instance_identifiers
            if db_proxy_name is None and not opts.urn:
                raise TypeError("Missing required property 'db_proxy_name'")
            __props__.__dict__["db_proxy_name"] = db_proxy_name
            if target_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'target_group_name'")
            __props__.__dict__["target_group_name"] = target_group_name
            __props__.__dict__["target_group_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["db_proxy_name", "target_group_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(DbProxyTargetGroup, __self__).__init__(
            'aws-native:rds:DbProxyTargetGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DbProxyTargetGroup':
        """
        Get an existing DbProxyTargetGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DbProxyTargetGroupArgs.__new__(DbProxyTargetGroupArgs)

        __props__.__dict__["connection_pool_configuration_info"] = None
        __props__.__dict__["db_cluster_identifiers"] = None
        __props__.__dict__["db_instance_identifiers"] = None
        __props__.__dict__["db_proxy_name"] = None
        __props__.__dict__["target_group_arn"] = None
        __props__.__dict__["target_group_name"] = None
        return DbProxyTargetGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionPoolConfigurationInfo")
    def connection_pool_configuration_info(self) -> pulumi.Output[Optional['outputs.DbProxyTargetGroupConnectionPoolConfigurationInfoFormat']]:
        return pulumi.get(self, "connection_pool_configuration_info")

    @property
    @pulumi.getter(name="dbClusterIdentifiers")
    def db_cluster_identifiers(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "db_cluster_identifiers")

    @property
    @pulumi.getter(name="dbInstanceIdentifiers")
    def db_instance_identifiers(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "db_instance_identifiers")

    @property
    @pulumi.getter(name="dbProxyName")
    def db_proxy_name(self) -> pulumi.Output[str]:
        """
        The identifier for the proxy.
        """
        return pulumi.get(self, "db_proxy_name")

    @property
    @pulumi.getter(name="targetGroupArn")
    def target_group_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) representing the target group.
        """
        return pulumi.get(self, "target_group_arn")

    @property
    @pulumi.getter(name="targetGroupName")
    def target_group_name(self) -> pulumi.Output['DbProxyTargetGroupTargetGroupName']:
        """
        The identifier for the DBProxyTargetGroup
        """
        return pulumi.get(self, "target_group_name")

