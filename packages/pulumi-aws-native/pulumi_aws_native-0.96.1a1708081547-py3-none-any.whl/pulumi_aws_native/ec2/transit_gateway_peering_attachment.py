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

__all__ = ['TransitGatewayPeeringAttachmentArgs', 'TransitGatewayPeeringAttachment']

@pulumi.input_type
class TransitGatewayPeeringAttachmentArgs:
    def __init__(__self__, *,
                 peer_account_id: pulumi.Input[str],
                 peer_region: pulumi.Input[str],
                 peer_transit_gateway_id: pulumi.Input[str],
                 transit_gateway_id: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['TransitGatewayPeeringAttachmentTagArgs']]]] = None):
        """
        The set of arguments for constructing a TransitGatewayPeeringAttachment resource.
        :param pulumi.Input[str] peer_account_id: The ID of the peer account
        :param pulumi.Input[str] peer_region: Peer Region
        :param pulumi.Input[str] peer_transit_gateway_id: The ID of the peer transit gateway.
        :param pulumi.Input[str] transit_gateway_id: The ID of the transit gateway.
        :param pulumi.Input[Sequence[pulumi.Input['TransitGatewayPeeringAttachmentTagArgs']]] tags: The tags for the transit gateway peering attachment.
        """
        pulumi.set(__self__, "peer_account_id", peer_account_id)
        pulumi.set(__self__, "peer_region", peer_region)
        pulumi.set(__self__, "peer_transit_gateway_id", peer_transit_gateway_id)
        pulumi.set(__self__, "transit_gateway_id", transit_gateway_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="peerAccountId")
    def peer_account_id(self) -> pulumi.Input[str]:
        """
        The ID of the peer account
        """
        return pulumi.get(self, "peer_account_id")

    @peer_account_id.setter
    def peer_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "peer_account_id", value)

    @property
    @pulumi.getter(name="peerRegion")
    def peer_region(self) -> pulumi.Input[str]:
        """
        Peer Region
        """
        return pulumi.get(self, "peer_region")

    @peer_region.setter
    def peer_region(self, value: pulumi.Input[str]):
        pulumi.set(self, "peer_region", value)

    @property
    @pulumi.getter(name="peerTransitGatewayId")
    def peer_transit_gateway_id(self) -> pulumi.Input[str]:
        """
        The ID of the peer transit gateway.
        """
        return pulumi.get(self, "peer_transit_gateway_id")

    @peer_transit_gateway_id.setter
    def peer_transit_gateway_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "peer_transit_gateway_id", value)

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> pulumi.Input[str]:
        """
        The ID of the transit gateway.
        """
        return pulumi.get(self, "transit_gateway_id")

    @transit_gateway_id.setter
    def transit_gateway_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "transit_gateway_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TransitGatewayPeeringAttachmentTagArgs']]]]:
        """
        The tags for the transit gateway peering attachment.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TransitGatewayPeeringAttachmentTagArgs']]]]):
        pulumi.set(self, "tags", value)


class TransitGatewayPeeringAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 peer_account_id: Optional[pulumi.Input[str]] = None,
                 peer_region: Optional[pulumi.Input[str]] = None,
                 peer_transit_gateway_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TransitGatewayPeeringAttachmentTagArgs']]]]] = None,
                 transit_gateway_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The AWS::EC2::TransitGatewayPeeringAttachment type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] peer_account_id: The ID of the peer account
        :param pulumi.Input[str] peer_region: Peer Region
        :param pulumi.Input[str] peer_transit_gateway_id: The ID of the peer transit gateway.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TransitGatewayPeeringAttachmentTagArgs']]]] tags: The tags for the transit gateway peering attachment.
        :param pulumi.Input[str] transit_gateway_id: The ID of the transit gateway.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TransitGatewayPeeringAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The AWS::EC2::TransitGatewayPeeringAttachment type

        :param str resource_name: The name of the resource.
        :param TransitGatewayPeeringAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TransitGatewayPeeringAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 peer_account_id: Optional[pulumi.Input[str]] = None,
                 peer_region: Optional[pulumi.Input[str]] = None,
                 peer_transit_gateway_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TransitGatewayPeeringAttachmentTagArgs']]]]] = None,
                 transit_gateway_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TransitGatewayPeeringAttachmentArgs.__new__(TransitGatewayPeeringAttachmentArgs)

            if peer_account_id is None and not opts.urn:
                raise TypeError("Missing required property 'peer_account_id'")
            __props__.__dict__["peer_account_id"] = peer_account_id
            if peer_region is None and not opts.urn:
                raise TypeError("Missing required property 'peer_region'")
            __props__.__dict__["peer_region"] = peer_region
            if peer_transit_gateway_id is None and not opts.urn:
                raise TypeError("Missing required property 'peer_transit_gateway_id'")
            __props__.__dict__["peer_transit_gateway_id"] = peer_transit_gateway_id
            __props__.__dict__["tags"] = tags
            if transit_gateway_id is None and not opts.urn:
                raise TypeError("Missing required property 'transit_gateway_id'")
            __props__.__dict__["transit_gateway_id"] = transit_gateway_id
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["transit_gateway_attachment_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["peer_account_id", "peer_region", "peer_transit_gateway_id", "transit_gateway_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(TransitGatewayPeeringAttachment, __self__).__init__(
            'aws-native:ec2:TransitGatewayPeeringAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TransitGatewayPeeringAttachment':
        """
        Get an existing TransitGatewayPeeringAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TransitGatewayPeeringAttachmentArgs.__new__(TransitGatewayPeeringAttachmentArgs)

        __props__.__dict__["creation_time"] = None
        __props__.__dict__["peer_account_id"] = None
        __props__.__dict__["peer_region"] = None
        __props__.__dict__["peer_transit_gateway_id"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["transit_gateway_attachment_id"] = None
        __props__.__dict__["transit_gateway_id"] = None
        return TransitGatewayPeeringAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        The time the transit gateway peering attachment was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="peerAccountId")
    def peer_account_id(self) -> pulumi.Output[str]:
        """
        The ID of the peer account
        """
        return pulumi.get(self, "peer_account_id")

    @property
    @pulumi.getter(name="peerRegion")
    def peer_region(self) -> pulumi.Output[str]:
        """
        Peer Region
        """
        return pulumi.get(self, "peer_region")

    @property
    @pulumi.getter(name="peerTransitGatewayId")
    def peer_transit_gateway_id(self) -> pulumi.Output[str]:
        """
        The ID of the peer transit gateway.
        """
        return pulumi.get(self, "peer_transit_gateway_id")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the transit gateway peering attachment. Note that the initiating state has been deprecated.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.TransitGatewayPeeringAttachmentPeeringAttachmentStatus']:
        """
        The status of the transit gateway peering attachment.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.TransitGatewayPeeringAttachmentTag']]]:
        """
        The tags for the transit gateway peering attachment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> pulumi.Output[str]:
        """
        The ID of the transit gateway peering attachment.
        """
        return pulumi.get(self, "transit_gateway_attachment_id")

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> pulumi.Output[str]:
        """
        The ID of the transit gateway.
        """
        return pulumi.get(self, "transit_gateway_id")

