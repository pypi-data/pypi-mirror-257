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
from ._inputs import *

__all__ = ['ClusterArgs', 'Cluster']

@pulumi.input_type
class ClusterArgs:
    def __init__(__self__, *,
                 iam_role_arn: pulumi.Input[str],
                 node_type: pulumi.Input[str],
                 replication_factor: pulumi.Input[int],
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 cluster_endpoint_encryption_type: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 notification_topic_arn: Optional[pulumi.Input[str]] = None,
                 parameter_group_name: Optional[pulumi.Input[str]] = None,
                 preferred_maintenance_window: Optional[pulumi.Input[str]] = None,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sse_specification: Optional[pulumi.Input['ClusterSseSpecificationArgs']] = None,
                 subnet_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None):
        """
        The set of arguments for constructing a Cluster resource.
        """
        pulumi.set(__self__, "iam_role_arn", iam_role_arn)
        pulumi.set(__self__, "node_type", node_type)
        pulumi.set(__self__, "replication_factor", replication_factor)
        if availability_zones is not None:
            pulumi.set(__self__, "availability_zones", availability_zones)
        if cluster_endpoint_encryption_type is not None:
            pulumi.set(__self__, "cluster_endpoint_encryption_type", cluster_endpoint_encryption_type)
        if cluster_name is not None:
            pulumi.set(__self__, "cluster_name", cluster_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if notification_topic_arn is not None:
            pulumi.set(__self__, "notification_topic_arn", notification_topic_arn)
        if parameter_group_name is not None:
            pulumi.set(__self__, "parameter_group_name", parameter_group_name)
        if preferred_maintenance_window is not None:
            pulumi.set(__self__, "preferred_maintenance_window", preferred_maintenance_window)
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)
        if sse_specification is not None:
            pulumi.set(__self__, "sse_specification", sse_specification)
        if subnet_group_name is not None:
            pulumi.set(__self__, "subnet_group_name", subnet_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> pulumi.Input[str]:
        return pulumi.get(self, "iam_role_arn")

    @iam_role_arn.setter
    def iam_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "iam_role_arn", value)

    @property
    @pulumi.getter(name="nodeType")
    def node_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "node_type")

    @node_type.setter
    def node_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "node_type", value)

    @property
    @pulumi.getter(name="replicationFactor")
    def replication_factor(self) -> pulumi.Input[int]:
        return pulumi.get(self, "replication_factor")

    @replication_factor.setter
    def replication_factor(self, value: pulumi.Input[int]):
        pulumi.set(self, "replication_factor", value)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "availability_zones")

    @availability_zones.setter
    def availability_zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "availability_zones", value)

    @property
    @pulumi.getter(name="clusterEndpointEncryptionType")
    def cluster_endpoint_encryption_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cluster_endpoint_encryption_type")

    @cluster_endpoint_encryption_type.setter
    def cluster_endpoint_encryption_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_endpoint_encryption_type", value)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="notificationTopicArn")
    def notification_topic_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "notification_topic_arn")

    @notification_topic_arn.setter
    def notification_topic_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notification_topic_arn", value)

    @property
    @pulumi.getter(name="parameterGroupName")
    def parameter_group_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "parameter_group_name")

    @parameter_group_name.setter
    def parameter_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parameter_group_name", value)

    @property
    @pulumi.getter(name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "preferred_maintenance_window")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "preferred_maintenance_window", value)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter(name="sseSpecification")
    def sse_specification(self) -> Optional[pulumi.Input['ClusterSseSpecificationArgs']]:
        return pulumi.get(self, "sse_specification")

    @sse_specification.setter
    def sse_specification(self, value: Optional[pulumi.Input['ClusterSseSpecificationArgs']]):
        pulumi.set(self, "sse_specification", value)

    @property
    @pulumi.getter(name="subnetGroupName")
    def subnet_group_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "subnet_group_name")

    @subnet_group_name.setter
    def subnet_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[Any]):
        pulumi.set(self, "tags", value)


warnings.warn("""Cluster is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class Cluster(pulumi.CustomResource):
    warnings.warn("""Cluster is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 cluster_endpoint_encryption_type: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 iam_role_arn: Optional[pulumi.Input[str]] = None,
                 node_type: Optional[pulumi.Input[str]] = None,
                 notification_topic_arn: Optional[pulumi.Input[str]] = None,
                 parameter_group_name: Optional[pulumi.Input[str]] = None,
                 preferred_maintenance_window: Optional[pulumi.Input[str]] = None,
                 replication_factor: Optional[pulumi.Input[int]] = None,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sse_specification: Optional[pulumi.Input[pulumi.InputType['ClusterSseSpecificationArgs']]] = None,
                 subnet_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::DAX::Cluster

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::DAX::Cluster

        :param str resource_name: The name of the resource.
        :param ClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 cluster_endpoint_encryption_type: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 iam_role_arn: Optional[pulumi.Input[str]] = None,
                 node_type: Optional[pulumi.Input[str]] = None,
                 notification_topic_arn: Optional[pulumi.Input[str]] = None,
                 parameter_group_name: Optional[pulumi.Input[str]] = None,
                 preferred_maintenance_window: Optional[pulumi.Input[str]] = None,
                 replication_factor: Optional[pulumi.Input[int]] = None,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sse_specification: Optional[pulumi.Input[pulumi.InputType['ClusterSseSpecificationArgs']]] = None,
                 subnet_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 __props__=None):
        pulumi.log.warn("""Cluster is deprecated: Cluster is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterArgs.__new__(ClusterArgs)

            __props__.__dict__["availability_zones"] = availability_zones
            __props__.__dict__["cluster_endpoint_encryption_type"] = cluster_endpoint_encryption_type
            __props__.__dict__["cluster_name"] = cluster_name
            __props__.__dict__["description"] = description
            if iam_role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'iam_role_arn'")
            __props__.__dict__["iam_role_arn"] = iam_role_arn
            if node_type is None and not opts.urn:
                raise TypeError("Missing required property 'node_type'")
            __props__.__dict__["node_type"] = node_type
            __props__.__dict__["notification_topic_arn"] = notification_topic_arn
            __props__.__dict__["parameter_group_name"] = parameter_group_name
            __props__.__dict__["preferred_maintenance_window"] = preferred_maintenance_window
            if replication_factor is None and not opts.urn:
                raise TypeError("Missing required property 'replication_factor'")
            __props__.__dict__["replication_factor"] = replication_factor
            __props__.__dict__["security_group_ids"] = security_group_ids
            __props__.__dict__["sse_specification"] = sse_specification
            __props__.__dict__["subnet_group_name"] = subnet_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["cluster_discovery_endpoint"] = None
            __props__.__dict__["cluster_discovery_endpoint_url"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["cluster_endpoint_encryption_type", "cluster_name", "iam_role_arn", "node_type", "sse_specification", "subnet_group_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Cluster, __self__).__init__(
            'aws-native:dax:Cluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Cluster':
        """
        Get an existing Cluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ClusterArgs.__new__(ClusterArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["availability_zones"] = None
        __props__.__dict__["cluster_discovery_endpoint"] = None
        __props__.__dict__["cluster_discovery_endpoint_url"] = None
        __props__.__dict__["cluster_endpoint_encryption_type"] = None
        __props__.__dict__["cluster_name"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["iam_role_arn"] = None
        __props__.__dict__["node_type"] = None
        __props__.__dict__["notification_topic_arn"] = None
        __props__.__dict__["parameter_group_name"] = None
        __props__.__dict__["preferred_maintenance_window"] = None
        __props__.__dict__["replication_factor"] = None
        __props__.__dict__["security_group_ids"] = None
        __props__.__dict__["sse_specification"] = None
        __props__.__dict__["subnet_group_name"] = None
        __props__.__dict__["tags"] = None
        return Cluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "availability_zones")

    @property
    @pulumi.getter(name="clusterDiscoveryEndpoint")
    def cluster_discovery_endpoint(self) -> pulumi.Output[str]:
        return pulumi.get(self, "cluster_discovery_endpoint")

    @property
    @pulumi.getter(name="clusterDiscoveryEndpointUrl")
    def cluster_discovery_endpoint_url(self) -> pulumi.Output[str]:
        return pulumi.get(self, "cluster_discovery_endpoint_url")

    @property
    @pulumi.getter(name="clusterEndpointEncryptionType")
    def cluster_endpoint_encryption_type(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "cluster_endpoint_encryption_type")

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "cluster_name")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "iam_role_arn")

    @property
    @pulumi.getter(name="nodeType")
    def node_type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "node_type")

    @property
    @pulumi.getter(name="notificationTopicArn")
    def notification_topic_arn(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "notification_topic_arn")

    @property
    @pulumi.getter(name="parameterGroupName")
    def parameter_group_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "parameter_group_name")

    @property
    @pulumi.getter(name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "preferred_maintenance_window")

    @property
    @pulumi.getter(name="replicationFactor")
    def replication_factor(self) -> pulumi.Output[int]:
        return pulumi.get(self, "replication_factor")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="sseSpecification")
    def sse_specification(self) -> pulumi.Output[Optional['outputs.ClusterSseSpecification']]:
        return pulumi.get(self, "sse_specification")

    @property
    @pulumi.getter(name="subnetGroupName")
    def subnet_group_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "subnet_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Any]]:
        return pulumi.get(self, "tags")

