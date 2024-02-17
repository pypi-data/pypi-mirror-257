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

__all__ = [
    'GetTransitGatewayPeeringResult',
    'AwaitableGetTransitGatewayPeeringResult',
    'get_transit_gateway_peering',
    'get_transit_gateway_peering_output',
]

@pulumi.output_type
class GetTransitGatewayPeeringResult:
    def __init__(__self__, core_network_arn=None, created_at=None, edge_location=None, owner_account_id=None, peering_id=None, peering_type=None, resource_arn=None, state=None, tags=None, transit_gateway_peering_attachment_id=None):
        if core_network_arn and not isinstance(core_network_arn, str):
            raise TypeError("Expected argument 'core_network_arn' to be a str")
        pulumi.set(__self__, "core_network_arn", core_network_arn)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if edge_location and not isinstance(edge_location, str):
            raise TypeError("Expected argument 'edge_location' to be a str")
        pulumi.set(__self__, "edge_location", edge_location)
        if owner_account_id and not isinstance(owner_account_id, str):
            raise TypeError("Expected argument 'owner_account_id' to be a str")
        pulumi.set(__self__, "owner_account_id", owner_account_id)
        if peering_id and not isinstance(peering_id, str):
            raise TypeError("Expected argument 'peering_id' to be a str")
        pulumi.set(__self__, "peering_id", peering_id)
        if peering_type and not isinstance(peering_type, str):
            raise TypeError("Expected argument 'peering_type' to be a str")
        pulumi.set(__self__, "peering_type", peering_type)
        if resource_arn and not isinstance(resource_arn, str):
            raise TypeError("Expected argument 'resource_arn' to be a str")
        pulumi.set(__self__, "resource_arn", resource_arn)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if transit_gateway_peering_attachment_id and not isinstance(transit_gateway_peering_attachment_id, str):
            raise TypeError("Expected argument 'transit_gateway_peering_attachment_id' to be a str")
        pulumi.set(__self__, "transit_gateway_peering_attachment_id", transit_gateway_peering_attachment_id)

    @property
    @pulumi.getter(name="coreNetworkArn")
    def core_network_arn(self) -> Optional[str]:
        """
        The ARN (Amazon Resource Name) of the core network that you want to peer a transit gateway to.
        """
        return pulumi.get(self, "core_network_arn")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The creation time of the transit gateway peering
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="edgeLocation")
    def edge_location(self) -> Optional[str]:
        """
        The location of the transit gateway peering
        """
        return pulumi.get(self, "edge_location")

    @property
    @pulumi.getter(name="ownerAccountId")
    def owner_account_id(self) -> Optional[str]:
        """
        Peering owner account Id
        """
        return pulumi.get(self, "owner_account_id")

    @property
    @pulumi.getter(name="peeringId")
    def peering_id(self) -> Optional[str]:
        """
        The Id of the transit gateway peering
        """
        return pulumi.get(self, "peering_id")

    @property
    @pulumi.getter(name="peeringType")
    def peering_type(self) -> Optional[str]:
        """
        Peering type (TransitGatewayPeering)
        """
        return pulumi.get(self, "peering_type")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> Optional[str]:
        """
        The ARN (Amazon Resource Name) of the resource that you will peer to a core network
        """
        return pulumi.get(self, "resource_arn")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of the transit gateway peering
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.TransitGatewayPeeringTag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transitGatewayPeeringAttachmentId")
    def transit_gateway_peering_attachment_id(self) -> Optional[str]:
        """
        The ID of the TransitGatewayPeeringAttachment
        """
        return pulumi.get(self, "transit_gateway_peering_attachment_id")


class AwaitableGetTransitGatewayPeeringResult(GetTransitGatewayPeeringResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTransitGatewayPeeringResult(
            core_network_arn=self.core_network_arn,
            created_at=self.created_at,
            edge_location=self.edge_location,
            owner_account_id=self.owner_account_id,
            peering_id=self.peering_id,
            peering_type=self.peering_type,
            resource_arn=self.resource_arn,
            state=self.state,
            tags=self.tags,
            transit_gateway_peering_attachment_id=self.transit_gateway_peering_attachment_id)


def get_transit_gateway_peering(peering_id: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTransitGatewayPeeringResult:
    """
    AWS::NetworkManager::TransitGatewayPeering Resoruce Type.


    :param str peering_id: The Id of the transit gateway peering
    """
    __args__ = dict()
    __args__['peeringId'] = peering_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:networkmanager:getTransitGatewayPeering', __args__, opts=opts, typ=GetTransitGatewayPeeringResult).value

    return AwaitableGetTransitGatewayPeeringResult(
        core_network_arn=pulumi.get(__ret__, 'core_network_arn'),
        created_at=pulumi.get(__ret__, 'created_at'),
        edge_location=pulumi.get(__ret__, 'edge_location'),
        owner_account_id=pulumi.get(__ret__, 'owner_account_id'),
        peering_id=pulumi.get(__ret__, 'peering_id'),
        peering_type=pulumi.get(__ret__, 'peering_type'),
        resource_arn=pulumi.get(__ret__, 'resource_arn'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'),
        transit_gateway_peering_attachment_id=pulumi.get(__ret__, 'transit_gateway_peering_attachment_id'))


@_utilities.lift_output_func(get_transit_gateway_peering)
def get_transit_gateway_peering_output(peering_id: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTransitGatewayPeeringResult]:
    """
    AWS::NetworkManager::TransitGatewayPeering Resoruce Type.


    :param str peering_id: The Id of the transit gateway peering
    """
    ...
