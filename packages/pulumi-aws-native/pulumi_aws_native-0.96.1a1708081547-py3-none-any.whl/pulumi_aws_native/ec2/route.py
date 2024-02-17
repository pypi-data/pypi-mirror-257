# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RouteArgs', 'Route']

@pulumi.input_type
class RouteArgs:
    def __init__(__self__, *,
                 route_table_id: pulumi.Input[str],
                 carrier_gateway_id: Optional[pulumi.Input[str]] = None,
                 core_network_arn: Optional[pulumi.Input[str]] = None,
                 destination_cidr_block: Optional[pulumi.Input[str]] = None,
                 destination_ipv6_cidr_block: Optional[pulumi.Input[str]] = None,
                 destination_prefix_list_id: Optional[pulumi.Input[str]] = None,
                 egress_only_internet_gateway_id: Optional[pulumi.Input[str]] = None,
                 gateway_id: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 local_gateway_id: Optional[pulumi.Input[str]] = None,
                 nat_gateway_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_id: Optional[pulumi.Input[str]] = None,
                 vpc_endpoint_id: Optional[pulumi.Input[str]] = None,
                 vpc_peering_connection_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Route resource.
        :param pulumi.Input[str] route_table_id: The ID of the route table. The routing table must be associated with the same VPC that the virtual private gateway is attached to.
        :param pulumi.Input[str] carrier_gateway_id: The ID of the carrier gateway.
        :param pulumi.Input[str] core_network_arn: The Amazon Resource Name (ARN) of the core network.
        :param pulumi.Input[str] destination_cidr_block: The IPv4 CIDR block used for the destination match.
        :param pulumi.Input[str] destination_ipv6_cidr_block: The IPv6 CIDR block used for the destination match.
        :param pulumi.Input[str] destination_prefix_list_id: The ID of managed prefix list, it's a set of one or more CIDR blocks.
        :param pulumi.Input[str] egress_only_internet_gateway_id: The ID of the egress-only internet gateway.
        :param pulumi.Input[str] gateway_id: The ID of an internet gateway or virtual private gateway attached to your VPC.
        :param pulumi.Input[str] instance_id: The ID of a NAT instance in your VPC.
        :param pulumi.Input[str] local_gateway_id: The ID of the local gateway.
        :param pulumi.Input[str] nat_gateway_id: The ID of a NAT gateway.
        :param pulumi.Input[str] network_interface_id: The ID of the network interface.
        :param pulumi.Input[str] transit_gateway_id: The ID of a transit gateway.
        :param pulumi.Input[str] vpc_endpoint_id: The ID of a VPC endpoint. Supported for Gateway Load Balancer endpoints only.
        :param pulumi.Input[str] vpc_peering_connection_id: The ID of a VPC peering connection.
        """
        pulumi.set(__self__, "route_table_id", route_table_id)
        if carrier_gateway_id is not None:
            pulumi.set(__self__, "carrier_gateway_id", carrier_gateway_id)
        if core_network_arn is not None:
            pulumi.set(__self__, "core_network_arn", core_network_arn)
        if destination_cidr_block is not None:
            pulumi.set(__self__, "destination_cidr_block", destination_cidr_block)
        if destination_ipv6_cidr_block is not None:
            pulumi.set(__self__, "destination_ipv6_cidr_block", destination_ipv6_cidr_block)
        if destination_prefix_list_id is not None:
            pulumi.set(__self__, "destination_prefix_list_id", destination_prefix_list_id)
        if egress_only_internet_gateway_id is not None:
            pulumi.set(__self__, "egress_only_internet_gateway_id", egress_only_internet_gateway_id)
        if gateway_id is not None:
            pulumi.set(__self__, "gateway_id", gateway_id)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if local_gateway_id is not None:
            pulumi.set(__self__, "local_gateway_id", local_gateway_id)
        if nat_gateway_id is not None:
            pulumi.set(__self__, "nat_gateway_id", nat_gateway_id)
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)
        if transit_gateway_id is not None:
            pulumi.set(__self__, "transit_gateway_id", transit_gateway_id)
        if vpc_endpoint_id is not None:
            pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)
        if vpc_peering_connection_id is not None:
            pulumi.set(__self__, "vpc_peering_connection_id", vpc_peering_connection_id)

    @property
    @pulumi.getter(name="routeTableId")
    def route_table_id(self) -> pulumi.Input[str]:
        """
        The ID of the route table. The routing table must be associated with the same VPC that the virtual private gateway is attached to.
        """
        return pulumi.get(self, "route_table_id")

    @route_table_id.setter
    def route_table_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "route_table_id", value)

    @property
    @pulumi.getter(name="carrierGatewayId")
    def carrier_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the carrier gateway.
        """
        return pulumi.get(self, "carrier_gateway_id")

    @carrier_gateway_id.setter
    def carrier_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "carrier_gateway_id", value)

    @property
    @pulumi.getter(name="coreNetworkArn")
    def core_network_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the core network.
        """
        return pulumi.get(self, "core_network_arn")

    @core_network_arn.setter
    def core_network_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "core_network_arn", value)

    @property
    @pulumi.getter(name="destinationCidrBlock")
    def destination_cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv4 CIDR block used for the destination match.
        """
        return pulumi.get(self, "destination_cidr_block")

    @destination_cidr_block.setter
    def destination_cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "destination_cidr_block", value)

    @property
    @pulumi.getter(name="destinationIpv6CidrBlock")
    def destination_ipv6_cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv6 CIDR block used for the destination match.
        """
        return pulumi.get(self, "destination_ipv6_cidr_block")

    @destination_ipv6_cidr_block.setter
    def destination_ipv6_cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "destination_ipv6_cidr_block", value)

    @property
    @pulumi.getter(name="destinationPrefixListId")
    def destination_prefix_list_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of managed prefix list, it's a set of one or more CIDR blocks.
        """
        return pulumi.get(self, "destination_prefix_list_id")

    @destination_prefix_list_id.setter
    def destination_prefix_list_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "destination_prefix_list_id", value)

    @property
    @pulumi.getter(name="egressOnlyInternetGatewayId")
    def egress_only_internet_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the egress-only internet gateway.
        """
        return pulumi.get(self, "egress_only_internet_gateway_id")

    @egress_only_internet_gateway_id.setter
    def egress_only_internet_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "egress_only_internet_gateway_id", value)

    @property
    @pulumi.getter(name="gatewayId")
    def gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of an internet gateway or virtual private gateway attached to your VPC.
        """
        return pulumi.get(self, "gateway_id")

    @gateway_id.setter
    def gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gateway_id", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of a NAT instance in your VPC.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="localGatewayId")
    def local_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the local gateway.
        """
        return pulumi.get(self, "local_gateway_id")

    @local_gateway_id.setter
    def local_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "local_gateway_id", value)

    @property
    @pulumi.getter(name="natGatewayId")
    def nat_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of a NAT gateway.
        """
        return pulumi.get(self, "nat_gateway_id")

    @nat_gateway_id.setter
    def nat_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "nat_gateway_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the network interface.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_interface_id", value)

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of a transit gateway.
        """
        return pulumi.get(self, "transit_gateway_id")

    @transit_gateway_id.setter
    def transit_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "transit_gateway_id", value)

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of a VPC endpoint. Supported for Gateway Load Balancer endpoints only.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @vpc_endpoint_id.setter
    def vpc_endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_endpoint_id", value)

    @property
    @pulumi.getter(name="vpcPeeringConnectionId")
    def vpc_peering_connection_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of a VPC peering connection.
        """
        return pulumi.get(self, "vpc_peering_connection_id")

    @vpc_peering_connection_id.setter
    def vpc_peering_connection_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_peering_connection_id", value)


class Route(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 carrier_gateway_id: Optional[pulumi.Input[str]] = None,
                 core_network_arn: Optional[pulumi.Input[str]] = None,
                 destination_cidr_block: Optional[pulumi.Input[str]] = None,
                 destination_ipv6_cidr_block: Optional[pulumi.Input[str]] = None,
                 destination_prefix_list_id: Optional[pulumi.Input[str]] = None,
                 egress_only_internet_gateway_id: Optional[pulumi.Input[str]] = None,
                 gateway_id: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 local_gateway_id: Optional[pulumi.Input[str]] = None,
                 nat_gateway_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 route_table_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_id: Optional[pulumi.Input[str]] = None,
                 vpc_endpoint_id: Optional[pulumi.Input[str]] = None,
                 vpc_peering_connection_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::EC2::Route

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] carrier_gateway_id: The ID of the carrier gateway.
        :param pulumi.Input[str] core_network_arn: The Amazon Resource Name (ARN) of the core network.
        :param pulumi.Input[str] destination_cidr_block: The IPv4 CIDR block used for the destination match.
        :param pulumi.Input[str] destination_ipv6_cidr_block: The IPv6 CIDR block used for the destination match.
        :param pulumi.Input[str] destination_prefix_list_id: The ID of managed prefix list, it's a set of one or more CIDR blocks.
        :param pulumi.Input[str] egress_only_internet_gateway_id: The ID of the egress-only internet gateway.
        :param pulumi.Input[str] gateway_id: The ID of an internet gateway or virtual private gateway attached to your VPC.
        :param pulumi.Input[str] instance_id: The ID of a NAT instance in your VPC.
        :param pulumi.Input[str] local_gateway_id: The ID of the local gateway.
        :param pulumi.Input[str] nat_gateway_id: The ID of a NAT gateway.
        :param pulumi.Input[str] network_interface_id: The ID of the network interface.
        :param pulumi.Input[str] route_table_id: The ID of the route table. The routing table must be associated with the same VPC that the virtual private gateway is attached to.
        :param pulumi.Input[str] transit_gateway_id: The ID of a transit gateway.
        :param pulumi.Input[str] vpc_endpoint_id: The ID of a VPC endpoint. Supported for Gateway Load Balancer endpoints only.
        :param pulumi.Input[str] vpc_peering_connection_id: The ID of a VPC peering connection.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RouteArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::EC2::Route

        :param str resource_name: The name of the resource.
        :param RouteArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RouteArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 carrier_gateway_id: Optional[pulumi.Input[str]] = None,
                 core_network_arn: Optional[pulumi.Input[str]] = None,
                 destination_cidr_block: Optional[pulumi.Input[str]] = None,
                 destination_ipv6_cidr_block: Optional[pulumi.Input[str]] = None,
                 destination_prefix_list_id: Optional[pulumi.Input[str]] = None,
                 egress_only_internet_gateway_id: Optional[pulumi.Input[str]] = None,
                 gateway_id: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 local_gateway_id: Optional[pulumi.Input[str]] = None,
                 nat_gateway_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 route_table_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_id: Optional[pulumi.Input[str]] = None,
                 vpc_endpoint_id: Optional[pulumi.Input[str]] = None,
                 vpc_peering_connection_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RouteArgs.__new__(RouteArgs)

            __props__.__dict__["carrier_gateway_id"] = carrier_gateway_id
            __props__.__dict__["core_network_arn"] = core_network_arn
            __props__.__dict__["destination_cidr_block"] = destination_cidr_block
            __props__.__dict__["destination_ipv6_cidr_block"] = destination_ipv6_cidr_block
            __props__.__dict__["destination_prefix_list_id"] = destination_prefix_list_id
            __props__.__dict__["egress_only_internet_gateway_id"] = egress_only_internet_gateway_id
            __props__.__dict__["gateway_id"] = gateway_id
            __props__.__dict__["instance_id"] = instance_id
            __props__.__dict__["local_gateway_id"] = local_gateway_id
            __props__.__dict__["nat_gateway_id"] = nat_gateway_id
            __props__.__dict__["network_interface_id"] = network_interface_id
            if route_table_id is None and not opts.urn:
                raise TypeError("Missing required property 'route_table_id'")
            __props__.__dict__["route_table_id"] = route_table_id
            __props__.__dict__["transit_gateway_id"] = transit_gateway_id
            __props__.__dict__["vpc_endpoint_id"] = vpc_endpoint_id
            __props__.__dict__["vpc_peering_connection_id"] = vpc_peering_connection_id
            __props__.__dict__["cidr_block"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["destination_cidr_block", "destination_ipv6_cidr_block", "destination_prefix_list_id", "route_table_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Route, __self__).__init__(
            'aws-native:ec2:Route',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Route':
        """
        Get an existing Route resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RouteArgs.__new__(RouteArgs)

        __props__.__dict__["carrier_gateway_id"] = None
        __props__.__dict__["cidr_block"] = None
        __props__.__dict__["core_network_arn"] = None
        __props__.__dict__["destination_cidr_block"] = None
        __props__.__dict__["destination_ipv6_cidr_block"] = None
        __props__.__dict__["destination_prefix_list_id"] = None
        __props__.__dict__["egress_only_internet_gateway_id"] = None
        __props__.__dict__["gateway_id"] = None
        __props__.__dict__["instance_id"] = None
        __props__.__dict__["local_gateway_id"] = None
        __props__.__dict__["nat_gateway_id"] = None
        __props__.__dict__["network_interface_id"] = None
        __props__.__dict__["route_table_id"] = None
        __props__.__dict__["transit_gateway_id"] = None
        __props__.__dict__["vpc_endpoint_id"] = None
        __props__.__dict__["vpc_peering_connection_id"] = None
        return Route(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="carrierGatewayId")
    def carrier_gateway_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the carrier gateway.
        """
        return pulumi.get(self, "carrier_gateway_id")

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> pulumi.Output[str]:
        """
        The primary identifier of the resource generated by the service.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter(name="coreNetworkArn")
    def core_network_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the core network.
        """
        return pulumi.get(self, "core_network_arn")

    @property
    @pulumi.getter(name="destinationCidrBlock")
    def destination_cidr_block(self) -> pulumi.Output[Optional[str]]:
        """
        The IPv4 CIDR block used for the destination match.
        """
        return pulumi.get(self, "destination_cidr_block")

    @property
    @pulumi.getter(name="destinationIpv6CidrBlock")
    def destination_ipv6_cidr_block(self) -> pulumi.Output[Optional[str]]:
        """
        The IPv6 CIDR block used for the destination match.
        """
        return pulumi.get(self, "destination_ipv6_cidr_block")

    @property
    @pulumi.getter(name="destinationPrefixListId")
    def destination_prefix_list_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of managed prefix list, it's a set of one or more CIDR blocks.
        """
        return pulumi.get(self, "destination_prefix_list_id")

    @property
    @pulumi.getter(name="egressOnlyInternetGatewayId")
    def egress_only_internet_gateway_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the egress-only internet gateway.
        """
        return pulumi.get(self, "egress_only_internet_gateway_id")

    @property
    @pulumi.getter(name="gatewayId")
    def gateway_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of an internet gateway or virtual private gateway attached to your VPC.
        """
        return pulumi.get(self, "gateway_id")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of a NAT instance in your VPC.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="localGatewayId")
    def local_gateway_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the local gateway.
        """
        return pulumi.get(self, "local_gateway_id")

    @property
    @pulumi.getter(name="natGatewayId")
    def nat_gateway_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of a NAT gateway.
        """
        return pulumi.get(self, "nat_gateway_id")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the network interface.
        """
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter(name="routeTableId")
    def route_table_id(self) -> pulumi.Output[str]:
        """
        The ID of the route table. The routing table must be associated with the same VPC that the virtual private gateway is attached to.
        """
        return pulumi.get(self, "route_table_id")

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of a transit gateway.
        """
        return pulumi.get(self, "transit_gateway_id")

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of a VPC endpoint. Supported for Gateway Load Balancer endpoints only.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @property
    @pulumi.getter(name="vpcPeeringConnectionId")
    def vpc_peering_connection_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of a VPC peering connection.
        """
        return pulumi.get(self, "vpc_peering_connection_id")

