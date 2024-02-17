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
    'GetVolumeResult',
    'AwaitableGetVolumeResult',
    'get_volume',
    'get_volume_output',
]

@pulumi.output_type
class GetVolumeResult:
    def __init__(__self__, name=None, ontap_configuration=None, open_zfs_configuration=None, resource_arn=None, tags=None, uuid=None, volume_id=None):
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if ontap_configuration and not isinstance(ontap_configuration, dict):
            raise TypeError("Expected argument 'ontap_configuration' to be a dict")
        pulumi.set(__self__, "ontap_configuration", ontap_configuration)
        if open_zfs_configuration and not isinstance(open_zfs_configuration, dict):
            raise TypeError("Expected argument 'open_zfs_configuration' to be a dict")
        pulumi.set(__self__, "open_zfs_configuration", open_zfs_configuration)
        if resource_arn and not isinstance(resource_arn, str):
            raise TypeError("Expected argument 'resource_arn' to be a str")
        pulumi.set(__self__, "resource_arn", resource_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if uuid and not isinstance(uuid, str):
            raise TypeError("Expected argument 'uuid' to be a str")
        pulumi.set(__self__, "uuid", uuid)
        if volume_id and not isinstance(volume_id, str):
            raise TypeError("Expected argument 'volume_id' to be a str")
        pulumi.set(__self__, "volume_id", volume_id)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ontapConfiguration")
    def ontap_configuration(self) -> Optional['outputs.VolumeOntapConfiguration']:
        return pulumi.get(self, "ontap_configuration")

    @property
    @pulumi.getter(name="openZfsConfiguration")
    def open_zfs_configuration(self) -> Optional['outputs.VolumeOpenZfsConfiguration']:
        return pulumi.get(self, "open_zfs_configuration")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> Optional[str]:
        return pulumi.get(self, "resource_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.VolumeTag']]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def uuid(self) -> Optional[str]:
        return pulumi.get(self, "uuid")

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> Optional[str]:
        return pulumi.get(self, "volume_id")


class AwaitableGetVolumeResult(GetVolumeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVolumeResult(
            name=self.name,
            ontap_configuration=self.ontap_configuration,
            open_zfs_configuration=self.open_zfs_configuration,
            resource_arn=self.resource_arn,
            tags=self.tags,
            uuid=self.uuid,
            volume_id=self.volume_id)


def get_volume(volume_id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVolumeResult:
    """
    Resource Type definition for AWS::FSx::Volume
    """
    __args__ = dict()
    __args__['volumeId'] = volume_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:fsx:getVolume', __args__, opts=opts, typ=GetVolumeResult).value

    return AwaitableGetVolumeResult(
        name=pulumi.get(__ret__, 'name'),
        ontap_configuration=pulumi.get(__ret__, 'ontap_configuration'),
        open_zfs_configuration=pulumi.get(__ret__, 'open_zfs_configuration'),
        resource_arn=pulumi.get(__ret__, 'resource_arn'),
        tags=pulumi.get(__ret__, 'tags'),
        uuid=pulumi.get(__ret__, 'uuid'),
        volume_id=pulumi.get(__ret__, 'volume_id'))


@_utilities.lift_output_func(get_volume)
def get_volume_output(volume_id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVolumeResult]:
    """
    Resource Type definition for AWS::FSx::Volume
    """
    ...
