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
    'GetLedgerResult',
    'AwaitableGetLedgerResult',
    'get_ledger',
    'get_ledger_output',
]

@pulumi.output_type
class GetLedgerResult:
    def __init__(__self__, deletion_protection=None, id=None, kms_key=None, permissions_mode=None, tags=None):
        if deletion_protection and not isinstance(deletion_protection, bool):
            raise TypeError("Expected argument 'deletion_protection' to be a bool")
        pulumi.set(__self__, "deletion_protection", deletion_protection)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kms_key and not isinstance(kms_key, str):
            raise TypeError("Expected argument 'kms_key' to be a str")
        pulumi.set(__self__, "kms_key", kms_key)
        if permissions_mode and not isinstance(permissions_mode, str):
            raise TypeError("Expected argument 'permissions_mode' to be a str")
        pulumi.set(__self__, "permissions_mode", permissions_mode)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> Optional[bool]:
        return pulumi.get(self, "deletion_protection")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="kmsKey")
    def kms_key(self) -> Optional[str]:
        return pulumi.get(self, "kms_key")

    @property
    @pulumi.getter(name="permissionsMode")
    def permissions_mode(self) -> Optional[str]:
        return pulumi.get(self, "permissions_mode")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.LedgerTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetLedgerResult(GetLedgerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLedgerResult(
            deletion_protection=self.deletion_protection,
            id=self.id,
            kms_key=self.kms_key,
            permissions_mode=self.permissions_mode,
            tags=self.tags)


def get_ledger(id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLedgerResult:
    """
    Resource Type definition for AWS::QLDB::Ledger
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:qldb:getLedger', __args__, opts=opts, typ=GetLedgerResult).value

    return AwaitableGetLedgerResult(
        deletion_protection=pulumi.get(__ret__, 'deletion_protection'),
        id=pulumi.get(__ret__, 'id'),
        kms_key=pulumi.get(__ret__, 'kms_key'),
        permissions_mode=pulumi.get(__ret__, 'permissions_mode'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_ledger)
def get_ledger_output(id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLedgerResult]:
    """
    Resource Type definition for AWS::QLDB::Ledger
    """
    ...
