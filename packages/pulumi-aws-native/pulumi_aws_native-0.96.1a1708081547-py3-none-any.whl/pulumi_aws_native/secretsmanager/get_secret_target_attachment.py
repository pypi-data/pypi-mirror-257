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
    'GetSecretTargetAttachmentResult',
    'AwaitableGetSecretTargetAttachmentResult',
    'get_secret_target_attachment',
    'get_secret_target_attachment_output',
]

@pulumi.output_type
class GetSecretTargetAttachmentResult:
    def __init__(__self__, id=None, secret_id=None, target_id=None, target_type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if secret_id and not isinstance(secret_id, str):
            raise TypeError("Expected argument 'secret_id' to be a str")
        pulumi.set(__self__, "secret_id", secret_id)
        if target_id and not isinstance(target_id, str):
            raise TypeError("Expected argument 'target_id' to be a str")
        pulumi.set(__self__, "target_id", target_id)
        if target_type and not isinstance(target_type, str):
            raise TypeError("Expected argument 'target_type' to be a str")
        pulumi.set(__self__, "target_type", target_type)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="secretId")
    def secret_id(self) -> Optional[str]:
        return pulumi.get(self, "secret_id")

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> Optional[str]:
        return pulumi.get(self, "target_id")

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> Optional[str]:
        return pulumi.get(self, "target_type")


class AwaitableGetSecretTargetAttachmentResult(GetSecretTargetAttachmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecretTargetAttachmentResult(
            id=self.id,
            secret_id=self.secret_id,
            target_id=self.target_id,
            target_type=self.target_type)


def get_secret_target_attachment(id: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecretTargetAttachmentResult:
    """
    Resource Type definition for AWS::SecretsManager::SecretTargetAttachment
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:secretsmanager:getSecretTargetAttachment', __args__, opts=opts, typ=GetSecretTargetAttachmentResult).value

    return AwaitableGetSecretTargetAttachmentResult(
        id=pulumi.get(__ret__, 'id'),
        secret_id=pulumi.get(__ret__, 'secret_id'),
        target_id=pulumi.get(__ret__, 'target_id'),
        target_type=pulumi.get(__ret__, 'target_type'))


@_utilities.lift_output_func(get_secret_target_attachment)
def get_secret_target_attachment_output(id: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSecretTargetAttachmentResult]:
    """
    Resource Type definition for AWS::SecretsManager::SecretTargetAttachment
    """
    ...
