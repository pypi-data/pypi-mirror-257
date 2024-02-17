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
    'GetDefaultViewAssociationResult',
    'AwaitableGetDefaultViewAssociationResult',
    'get_default_view_association',
    'get_default_view_association_output',
]

@pulumi.output_type
class GetDefaultViewAssociationResult:
    def __init__(__self__, associated_aws_principal=None, view_arn=None):
        if associated_aws_principal and not isinstance(associated_aws_principal, str):
            raise TypeError("Expected argument 'associated_aws_principal' to be a str")
        pulumi.set(__self__, "associated_aws_principal", associated_aws_principal)
        if view_arn and not isinstance(view_arn, str):
            raise TypeError("Expected argument 'view_arn' to be a str")
        pulumi.set(__self__, "view_arn", view_arn)

    @property
    @pulumi.getter(name="associatedAwsPrincipal")
    def associated_aws_principal(self) -> Optional[str]:
        """
        The AWS principal that the default view is associated with, used as the unique identifier for this resource.
        """
        return pulumi.get(self, "associated_aws_principal")

    @property
    @pulumi.getter(name="viewArn")
    def view_arn(self) -> Optional[str]:
        return pulumi.get(self, "view_arn")


class AwaitableGetDefaultViewAssociationResult(GetDefaultViewAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDefaultViewAssociationResult(
            associated_aws_principal=self.associated_aws_principal,
            view_arn=self.view_arn)


def get_default_view_association(associated_aws_principal: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDefaultViewAssociationResult:
    """
    Definition of AWS::ResourceExplorer2::DefaultViewAssociation Resource Type


    :param str associated_aws_principal: The AWS principal that the default view is associated with, used as the unique identifier for this resource.
    """
    __args__ = dict()
    __args__['associatedAwsPrincipal'] = associated_aws_principal
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:resourceexplorer2:getDefaultViewAssociation', __args__, opts=opts, typ=GetDefaultViewAssociationResult).value

    return AwaitableGetDefaultViewAssociationResult(
        associated_aws_principal=pulumi.get(__ret__, 'associated_aws_principal'),
        view_arn=pulumi.get(__ret__, 'view_arn'))


@_utilities.lift_output_func(get_default_view_association)
def get_default_view_association_output(associated_aws_principal: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDefaultViewAssociationResult]:
    """
    Definition of AWS::ResourceExplorer2::DefaultViewAssociation Resource Type


    :param str associated_aws_principal: The AWS principal that the default view is associated with, used as the unique identifier for this resource.
    """
    ...
