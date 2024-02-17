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
    'GetPresetResult',
    'AwaitableGetPresetResult',
    'get_preset',
    'get_preset_output',
]

@pulumi.output_type
class GetPresetResult:
    def __init__(__self__, arn=None, category=None, description=None, id=None, settings_json=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if category and not isinstance(category, str):
            raise TypeError("Expected argument 'category' to be a str")
        pulumi.set(__self__, "category", category)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if settings_json and not isinstance(settings_json, dict):
            raise TypeError("Expected argument 'settings_json' to be a dict")
        pulumi.set(__self__, "settings_json", settings_json)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def category(self) -> Optional[str]:
        return pulumi.get(self, "category")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="settingsJson")
    def settings_json(self) -> Optional[Any]:
        return pulumi.get(self, "settings_json")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        return pulumi.get(self, "tags")


class AwaitableGetPresetResult(GetPresetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPresetResult(
            arn=self.arn,
            category=self.category,
            description=self.description,
            id=self.id,
            settings_json=self.settings_json,
            tags=self.tags)


def get_preset(id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPresetResult:
    """
    Resource Type definition for AWS::MediaConvert::Preset
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:mediaconvert:getPreset', __args__, opts=opts, typ=GetPresetResult).value

    return AwaitableGetPresetResult(
        arn=pulumi.get(__ret__, 'arn'),
        category=pulumi.get(__ret__, 'category'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        settings_json=pulumi.get(__ret__, 'settings_json'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_preset)
def get_preset_output(id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPresetResult]:
    """
    Resource Type definition for AWS::MediaConvert::Preset
    """
    ...
