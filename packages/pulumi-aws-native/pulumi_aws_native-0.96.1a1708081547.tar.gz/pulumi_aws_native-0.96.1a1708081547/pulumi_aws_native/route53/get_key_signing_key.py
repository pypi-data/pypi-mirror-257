# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'GetKeySigningKeyResult',
    'AwaitableGetKeySigningKeyResult',
    'get_key_signing_key',
    'get_key_signing_key_output',
]

@pulumi.output_type
class GetKeySigningKeyResult:
    def __init__(__self__, status=None):
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def status(self) -> Optional['KeySigningKeyStatus']:
        """
        A string specifying the initial status of the key signing key (KSK). You can set the value to ACTIVE or INACTIVE.
        """
        return pulumi.get(self, "status")


class AwaitableGetKeySigningKeyResult(GetKeySigningKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKeySigningKeyResult(
            status=self.status)


def get_key_signing_key(hosted_zone_id: Optional[str] = None,
                        name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetKeySigningKeyResult:
    """
    Represents a key signing key (KSK) associated with a hosted zone. You can only have two KSKs per hosted zone.


    :param str hosted_zone_id: The unique string (ID) used to identify a hosted zone.
    :param str name: An alphanumeric string used to identify a key signing key (KSK). Name must be unique for each key signing key in the same hosted zone.
    """
    __args__ = dict()
    __args__['hostedZoneId'] = hosted_zone_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:route53:getKeySigningKey', __args__, opts=opts, typ=GetKeySigningKeyResult).value

    return AwaitableGetKeySigningKeyResult(
        status=pulumi.get(__ret__, 'status'))


@_utilities.lift_output_func(get_key_signing_key)
def get_key_signing_key_output(hosted_zone_id: Optional[pulumi.Input[str]] = None,
                               name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetKeySigningKeyResult]:
    """
    Represents a key signing key (KSK) associated with a hosted zone. You can only have two KSKs per hosted zone.


    :param str hosted_zone_id: The unique string (ID) used to identify a hosted zone.
    :param str name: An alphanumeric string used to identify a key signing key (KSK). Name must be unique for each key signing key in the same hosted zone.
    """
    ...
