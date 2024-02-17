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
    'GetRepositoryAssociationResult',
    'AwaitableGetRepositoryAssociationResult',
    'get_repository_association',
    'get_repository_association_output',
]

@pulumi.output_type
class GetRepositoryAssociationResult:
    def __init__(__self__, association_arn=None):
        if association_arn and not isinstance(association_arn, str):
            raise TypeError("Expected argument 'association_arn' to be a str")
        pulumi.set(__self__, "association_arn", association_arn)

    @property
    @pulumi.getter(name="associationArn")
    def association_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the repository association.
        """
        return pulumi.get(self, "association_arn")


class AwaitableGetRepositoryAssociationResult(GetRepositoryAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRepositoryAssociationResult(
            association_arn=self.association_arn)


def get_repository_association(association_arn: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRepositoryAssociationResult:
    """
    This resource schema represents the RepositoryAssociation resource in the Amazon CodeGuru Reviewer service.


    :param str association_arn: The Amazon Resource Name (ARN) of the repository association.
    """
    __args__ = dict()
    __args__['associationArn'] = association_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:codegurureviewer:getRepositoryAssociation', __args__, opts=opts, typ=GetRepositoryAssociationResult).value

    return AwaitableGetRepositoryAssociationResult(
        association_arn=pulumi.get(__ret__, 'association_arn'))


@_utilities.lift_output_func(get_repository_association)
def get_repository_association_output(association_arn: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRepositoryAssociationResult]:
    """
    This resource schema represents the RepositoryAssociation resource in the Amazon CodeGuru Reviewer service.


    :param str association_arn: The Amazon Resource Name (ARN) of the repository association.
    """
    ...
