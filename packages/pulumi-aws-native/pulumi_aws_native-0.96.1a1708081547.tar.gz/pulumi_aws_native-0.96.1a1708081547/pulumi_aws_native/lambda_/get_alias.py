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
    'GetAliasResult',
    'AwaitableGetAliasResult',
    'get_alias',
    'get_alias_output',
]

@pulumi.output_type
class GetAliasResult:
    def __init__(__self__, description=None, function_version=None, id=None, provisioned_concurrency_config=None, routing_config=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if function_version and not isinstance(function_version, str):
            raise TypeError("Expected argument 'function_version' to be a str")
        pulumi.set(__self__, "function_version", function_version)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if provisioned_concurrency_config and not isinstance(provisioned_concurrency_config, dict):
            raise TypeError("Expected argument 'provisioned_concurrency_config' to be a dict")
        pulumi.set(__self__, "provisioned_concurrency_config", provisioned_concurrency_config)
        if routing_config and not isinstance(routing_config, dict):
            raise TypeError("Expected argument 'routing_config' to be a dict")
        pulumi.set(__self__, "routing_config", routing_config)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="functionVersion")
    def function_version(self) -> Optional[str]:
        return pulumi.get(self, "function_version")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="provisionedConcurrencyConfig")
    def provisioned_concurrency_config(self) -> Optional['outputs.AliasProvisionedConcurrencyConfiguration']:
        return pulumi.get(self, "provisioned_concurrency_config")

    @property
    @pulumi.getter(name="routingConfig")
    def routing_config(self) -> Optional['outputs.AliasRoutingConfiguration']:
        return pulumi.get(self, "routing_config")


class AwaitableGetAliasResult(GetAliasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAliasResult(
            description=self.description,
            function_version=self.function_version,
            id=self.id,
            provisioned_concurrency_config=self.provisioned_concurrency_config,
            routing_config=self.routing_config)


def get_alias(id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAliasResult:
    """
    Resource Type definition for AWS::Lambda::Alias
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:lambda:getAlias', __args__, opts=opts, typ=GetAliasResult).value

    return AwaitableGetAliasResult(
        description=pulumi.get(__ret__, 'description'),
        function_version=pulumi.get(__ret__, 'function_version'),
        id=pulumi.get(__ret__, 'id'),
        provisioned_concurrency_config=pulumi.get(__ret__, 'provisioned_concurrency_config'),
        routing_config=pulumi.get(__ret__, 'routing_config'))


@_utilities.lift_output_func(get_alias)
def get_alias_output(id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAliasResult]:
    """
    Resource Type definition for AWS::Lambda::Alias
    """
    ...
