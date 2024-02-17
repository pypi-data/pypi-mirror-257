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
from ._enums import *

__all__ = [
    'GetRecordingConfigurationResult',
    'AwaitableGetRecordingConfigurationResult',
    'get_recording_configuration',
    'get_recording_configuration_output',
]

@pulumi.output_type
class GetRecordingConfigurationResult:
    def __init__(__self__, arn=None, state=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Recording Configuration ARN is automatically generated on creation and assigned as the unique identifier.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def state(self) -> Optional['RecordingConfigurationState']:
        """
        Recording Configuration State.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.RecordingConfigurationTag']]:
        """
        A list of key-value pairs that contain metadata for the asset model.
        """
        return pulumi.get(self, "tags")


class AwaitableGetRecordingConfigurationResult(GetRecordingConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRecordingConfigurationResult(
            arn=self.arn,
            state=self.state,
            tags=self.tags)


def get_recording_configuration(arn: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRecordingConfigurationResult:
    """
    Resource Type definition for AWS::IVS::RecordingConfiguration


    :param str arn: Recording Configuration ARN is automatically generated on creation and assigned as the unique identifier.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ivs:getRecordingConfiguration', __args__, opts=opts, typ=GetRecordingConfigurationResult).value

    return AwaitableGetRecordingConfigurationResult(
        arn=pulumi.get(__ret__, 'arn'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_recording_configuration)
def get_recording_configuration_output(arn: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRecordingConfigurationResult]:
    """
    Resource Type definition for AWS::IVS::RecordingConfiguration


    :param str arn: Recording Configuration ARN is automatically generated on creation and assigned as the unique identifier.
    """
    ...
