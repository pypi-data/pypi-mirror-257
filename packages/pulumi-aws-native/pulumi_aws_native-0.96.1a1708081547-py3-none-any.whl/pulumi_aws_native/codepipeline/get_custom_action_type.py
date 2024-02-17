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
    'GetCustomActionTypeResult',
    'AwaitableGetCustomActionTypeResult',
    'get_custom_action_type',
    'get_custom_action_type_output',
]

@pulumi.output_type
class GetCustomActionTypeResult:
    def __init__(__self__, id=None, tags=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.CustomActionTypeTag']]:
        """
        Any tags assigned to the custom action.
        """
        return pulumi.get(self, "tags")


class AwaitableGetCustomActionTypeResult(GetCustomActionTypeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCustomActionTypeResult(
            id=self.id,
            tags=self.tags)


def get_custom_action_type(category: Optional[str] = None,
                           provider: Optional[str] = None,
                           version: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCustomActionTypeResult:
    """
    The AWS::CodePipeline::CustomActionType resource creates a custom action for activities that aren't included in the CodePipeline default actions, such as running an internally developed build process or a test suite. You can use these custom actions in the stage of a pipeline.


    :param str category: The category of the custom action, such as a build action or a test action.
    :param str provider: The provider of the service used in the custom action, such as AWS CodeDeploy.
    :param str version: The version identifier of the custom action.
    """
    __args__ = dict()
    __args__['category'] = category
    __args__['provider'] = provider
    __args__['version'] = version
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:codepipeline:getCustomActionType', __args__, opts=opts, typ=GetCustomActionTypeResult).value

    return AwaitableGetCustomActionTypeResult(
        id=pulumi.get(__ret__, 'id'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_custom_action_type)
def get_custom_action_type_output(category: Optional[pulumi.Input[str]] = None,
                                  provider: Optional[pulumi.Input[str]] = None,
                                  version: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCustomActionTypeResult]:
    """
    The AWS::CodePipeline::CustomActionType resource creates a custom action for activities that aren't included in the CodePipeline default actions, such as running an internally developed build process or a test suite. You can use these custom actions in the stage of a pipeline.


    :param str category: The category of the custom action, such as a build action or a test action.
    :param str provider: The provider of the service used in the custom action, such as AWS CodeDeploy.
    :param str version: The version identifier of the custom action.
    """
    ...
