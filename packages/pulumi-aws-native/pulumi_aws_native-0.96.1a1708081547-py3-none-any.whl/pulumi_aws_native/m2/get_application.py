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
    'GetApplicationResult',
    'AwaitableGetApplicationResult',
    'get_application',
    'get_application_output',
]

@pulumi.output_type
class GetApplicationResult:
    def __init__(__self__, application_arn=None, application_id=None, description=None, tags=None):
        if application_arn and not isinstance(application_arn, str):
            raise TypeError("Expected argument 'application_arn' to be a str")
        pulumi.set(__self__, "application_arn", application_arn)
        if application_id and not isinstance(application_id, str):
            raise TypeError("Expected argument 'application_id' to be a str")
        pulumi.set(__self__, "application_id", application_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="applicationArn")
    def application_arn(self) -> Optional[str]:
        return pulumi.get(self, "application_arn")

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[str]:
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def tags(self) -> Optional['outputs.ApplicationTagMap']:
        return pulumi.get(self, "tags")


class AwaitableGetApplicationResult(GetApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(
            application_arn=self.application_arn,
            application_id=self.application_id,
            description=self.description,
            tags=self.tags)


def get_application(application_arn: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationResult:
    """
    Represents an application that runs on an AWS Mainframe Modernization Environment
    """
    __args__ = dict()
    __args__['applicationArn'] = application_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:m2:getApplication', __args__, opts=opts, typ=GetApplicationResult).value

    return AwaitableGetApplicationResult(
        application_arn=pulumi.get(__ret__, 'application_arn'),
        application_id=pulumi.get(__ret__, 'application_id'),
        description=pulumi.get(__ret__, 'description'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_application)
def get_application_output(application_arn: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApplicationResult]:
    """
    Represents an application that runs on an AWS Mainframe Modernization Environment
    """
    ...
