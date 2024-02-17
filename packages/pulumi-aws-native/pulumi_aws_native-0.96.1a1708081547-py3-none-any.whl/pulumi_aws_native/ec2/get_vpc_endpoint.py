# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetVpcEndpointResult',
    'AwaitableGetVpcEndpointResult',
    'get_vpc_endpoint',
    'get_vpc_endpoint_output',
]

@pulumi.output_type
class GetVpcEndpointResult:
    def __init__(__self__, creation_timestamp=None, dns_entries=None, id=None, network_interface_ids=None, policy_document=None, private_dns_enabled=None, route_table_ids=None, security_group_ids=None, subnet_ids=None):
        if creation_timestamp and not isinstance(creation_timestamp, str):
            raise TypeError("Expected argument 'creation_timestamp' to be a str")
        pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if dns_entries and not isinstance(dns_entries, list):
            raise TypeError("Expected argument 'dns_entries' to be a list")
        pulumi.set(__self__, "dns_entries", dns_entries)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if network_interface_ids and not isinstance(network_interface_ids, list):
            raise TypeError("Expected argument 'network_interface_ids' to be a list")
        pulumi.set(__self__, "network_interface_ids", network_interface_ids)
        if policy_document and not isinstance(policy_document, str):
            raise TypeError("Expected argument 'policy_document' to be a str")
        pulumi.set(__self__, "policy_document", policy_document)
        if private_dns_enabled and not isinstance(private_dns_enabled, bool):
            raise TypeError("Expected argument 'private_dns_enabled' to be a bool")
        pulumi.set(__self__, "private_dns_enabled", private_dns_enabled)
        if route_table_ids and not isinstance(route_table_ids, list):
            raise TypeError("Expected argument 'route_table_ids' to be a list")
        pulumi.set(__self__, "route_table_ids", route_table_ids)
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError("Expected argument 'security_group_ids' to be a list")
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        if subnet_ids and not isinstance(subnet_ids, list):
            raise TypeError("Expected argument 'subnet_ids' to be a list")
        pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> Optional[str]:
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter(name="dnsEntries")
    def dns_entries(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "dns_entries")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="networkInterfaceIds")
    def network_interface_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "network_interface_ids")

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Optional[str]:
        """
        A policy to attach to the endpoint that controls access to the service.
        """
        return pulumi.get(self, "policy_document")

    @property
    @pulumi.getter(name="privateDnsEnabled")
    def private_dns_enabled(self) -> Optional[bool]:
        """
        Indicate whether to associate a private hosted zone with the specified VPC.
        """
        return pulumi.get(self, "private_dns_enabled")

    @property
    @pulumi.getter(name="routeTableIds")
    def route_table_ids(self) -> Optional[Sequence[str]]:
        """
        One or more route table IDs.
        """
        return pulumi.get(self, "route_table_ids")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[str]]:
        """
        The ID of one or more security groups to associate with the endpoint network interface.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[Sequence[str]]:
        """
        The ID of one or more subnets in which to create an endpoint network interface.
        """
        return pulumi.get(self, "subnet_ids")


class AwaitableGetVpcEndpointResult(GetVpcEndpointResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcEndpointResult(
            creation_timestamp=self.creation_timestamp,
            dns_entries=self.dns_entries,
            id=self.id,
            network_interface_ids=self.network_interface_ids,
            policy_document=self.policy_document,
            private_dns_enabled=self.private_dns_enabled,
            route_table_ids=self.route_table_ids,
            security_group_ids=self.security_group_ids,
            subnet_ids=self.subnet_ids)


def get_vpc_endpoint(id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcEndpointResult:
    """
    Resource Type definition for AWS::EC2::VPCEndpoint
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getVpcEndpoint', __args__, opts=opts, typ=GetVpcEndpointResult).value

    return AwaitableGetVpcEndpointResult(
        creation_timestamp=pulumi.get(__ret__, 'creation_timestamp'),
        dns_entries=pulumi.get(__ret__, 'dns_entries'),
        id=pulumi.get(__ret__, 'id'),
        network_interface_ids=pulumi.get(__ret__, 'network_interface_ids'),
        policy_document=pulumi.get(__ret__, 'policy_document'),
        private_dns_enabled=pulumi.get(__ret__, 'private_dns_enabled'),
        route_table_ids=pulumi.get(__ret__, 'route_table_ids'),
        security_group_ids=pulumi.get(__ret__, 'security_group_ids'),
        subnet_ids=pulumi.get(__ret__, 'subnet_ids'))


@_utilities.lift_output_func(get_vpc_endpoint)
def get_vpc_endpoint_output(id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVpcEndpointResult]:
    """
    Resource Type definition for AWS::EC2::VPCEndpoint
    """
    ...
