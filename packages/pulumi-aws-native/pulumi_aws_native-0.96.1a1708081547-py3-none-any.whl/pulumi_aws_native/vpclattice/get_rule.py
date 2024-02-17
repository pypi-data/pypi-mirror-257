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
    'GetRuleResult',
    'AwaitableGetRuleResult',
    'get_rule',
    'get_rule_output',
]

@pulumi.output_type
class GetRuleResult:
    def __init__(__self__, action=None, arn=None, id=None, match=None, priority=None, tags=None):
        if action and not isinstance(action, dict):
            raise TypeError("Expected argument 'action' to be a dict")
        pulumi.set(__self__, "action", action)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if match and not isinstance(match, dict):
            raise TypeError("Expected argument 'match' to be a dict")
        pulumi.set(__self__, "match", match)
        if priority and not isinstance(priority, int):
            raise TypeError("Expected argument 'priority' to be a int")
        pulumi.set(__self__, "priority", priority)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def action(self) -> Optional['outputs.RuleAction']:
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def match(self) -> Optional['outputs.RuleMatch']:
        return pulumi.get(self, "match")

    @property
    @pulumi.getter
    def priority(self) -> Optional[int]:
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.RuleTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetRuleResult(GetRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRuleResult(
            action=self.action,
            arn=self.arn,
            id=self.id,
            match=self.match,
            priority=self.priority,
            tags=self.tags)


def get_rule(arn: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRuleResult:
    """
    Creates a listener rule. Each listener has a default rule for checking connection requests, but you can define additional rules. Each rule consists of a priority, one or more actions, and one or more conditions.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:vpclattice:getRule', __args__, opts=opts, typ=GetRuleResult).value

    return AwaitableGetRuleResult(
        action=pulumi.get(__ret__, 'action'),
        arn=pulumi.get(__ret__, 'arn'),
        id=pulumi.get(__ret__, 'id'),
        match=pulumi.get(__ret__, 'match'),
        priority=pulumi.get(__ret__, 'priority'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_rule)
def get_rule_output(arn: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRuleResult]:
    """
    Creates a listener rule. Each listener has a default rule for checking connection requests, but you can define additional rules. Each rule consists of a priority, one or more actions, and one or more conditions.
    """
    ...
