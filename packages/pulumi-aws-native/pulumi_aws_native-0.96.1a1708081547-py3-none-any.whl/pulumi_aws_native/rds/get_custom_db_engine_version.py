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
    'GetCustomDbEngineVersionResult',
    'AwaitableGetCustomDbEngineVersionResult',
    'get_custom_db_engine_version',
    'get_custom_db_engine_version_output',
]

@pulumi.output_type
class GetCustomDbEngineVersionResult:
    def __init__(__self__, db_engine_version_arn=None, description=None, status=None, tags=None):
        if db_engine_version_arn and not isinstance(db_engine_version_arn, str):
            raise TypeError("Expected argument 'db_engine_version_arn' to be a str")
        pulumi.set(__self__, "db_engine_version_arn", db_engine_version_arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="dbEngineVersionArn")
    def db_engine_version_arn(self) -> Optional[str]:
        """
        The ARN of the custom engine version.
        """
        return pulumi.get(self, "db_engine_version_arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of your CEV.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def status(self) -> Optional['CustomDbEngineVersionStatus']:
        """
        The availability status to be assigned to the CEV.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.CustomDbEngineVersionTag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetCustomDbEngineVersionResult(GetCustomDbEngineVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCustomDbEngineVersionResult(
            db_engine_version_arn=self.db_engine_version_arn,
            description=self.description,
            status=self.status,
            tags=self.tags)


def get_custom_db_engine_version(engine: Optional[str] = None,
                                 engine_version: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCustomDbEngineVersionResult:
    """
    The AWS::RDS::CustomDBEngineVersion resource creates an Amazon RDS custom DB engine version.


    :param str engine: The database engine to use for your custom engine version (CEV). The only supported value is `custom-oracle-ee`.
    :param str engine_version: The name of your CEV. The name format is 19.customized_string . For example, a valid name is 19.my_cev1. This setting is required for RDS Custom for Oracle, but optional for Amazon RDS. The combination of Engine and EngineVersion is unique per customer per Region.
    """
    __args__ = dict()
    __args__['engine'] = engine
    __args__['engineVersion'] = engine_version
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:rds:getCustomDbEngineVersion', __args__, opts=opts, typ=GetCustomDbEngineVersionResult).value

    return AwaitableGetCustomDbEngineVersionResult(
        db_engine_version_arn=pulumi.get(__ret__, 'db_engine_version_arn'),
        description=pulumi.get(__ret__, 'description'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_custom_db_engine_version)
def get_custom_db_engine_version_output(engine: Optional[pulumi.Input[str]] = None,
                                        engine_version: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCustomDbEngineVersionResult]:
    """
    The AWS::RDS::CustomDBEngineVersion resource creates an Amazon RDS custom DB engine version.


    :param str engine: The database engine to use for your custom engine version (CEV). The only supported value is `custom-oracle-ee`.
    :param str engine_version: The name of your CEV. The name format is 19.customized_string . For example, a valid name is 19.my_cev1. This setting is required for RDS Custom for Oracle, but optional for Amazon RDS. The combination of Engine and EngineVersion is unique per customer per Region.
    """
    ...
