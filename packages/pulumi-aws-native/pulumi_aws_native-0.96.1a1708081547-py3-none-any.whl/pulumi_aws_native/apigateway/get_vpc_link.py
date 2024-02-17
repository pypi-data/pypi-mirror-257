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
    'GetVpcLinkResult',
    'AwaitableGetVpcLinkResult',
    'get_vpc_link',
    'get_vpc_link_output',
]

@pulumi.output_type
class GetVpcLinkResult:
    def __init__(__self__, description=None, name=None, tags=None, vpc_link_id=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if vpc_link_id and not isinstance(vpc_link_id, str):
            raise TypeError("Expected argument 'vpc_link_id' to be a str")
        pulumi.set(__self__, "vpc_link_id", vpc_link_id)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of the VPC link.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A name for the VPC link.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.VpcLinkTag']]:
        """
        An array of arbitrary tags (key-value pairs) to associate with the stage.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcLinkId")
    def vpc_link_id(self) -> Optional[str]:
        """
        The ID of the instance that backs VPC link.
        """
        return pulumi.get(self, "vpc_link_id")


class AwaitableGetVpcLinkResult(GetVpcLinkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcLinkResult(
            description=self.description,
            name=self.name,
            tags=self.tags,
            vpc_link_id=self.vpc_link_id)


def get_vpc_link(vpc_link_id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcLinkResult:
    """
    Schema for AWS ApiGateway VpcLink


    :param str vpc_link_id: The ID of the instance that backs VPC link.
    """
    __args__ = dict()
    __args__['vpcLinkId'] = vpc_link_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:apigateway:getVpcLink', __args__, opts=opts, typ=GetVpcLinkResult).value

    return AwaitableGetVpcLinkResult(
        description=pulumi.get(__ret__, 'description'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'),
        vpc_link_id=pulumi.get(__ret__, 'vpc_link_id'))


@_utilities.lift_output_func(get_vpc_link)
def get_vpc_link_output(vpc_link_id: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVpcLinkResult]:
    """
    Schema for AWS ApiGateway VpcLink


    :param str vpc_link_id: The ID of the instance that backs VPC link.
    """
    ...
