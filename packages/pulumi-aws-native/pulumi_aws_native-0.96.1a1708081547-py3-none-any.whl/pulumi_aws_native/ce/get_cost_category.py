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
    'GetCostCategoryResult',
    'AwaitableGetCostCategoryResult',
    'get_cost_category',
    'get_cost_category_output',
]

@pulumi.output_type
class GetCostCategoryResult:
    def __init__(__self__, arn=None, default_value=None, effective_start=None, rule_version=None, rules=None, split_charge_rules=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if default_value and not isinstance(default_value, str):
            raise TypeError("Expected argument 'default_value' to be a str")
        pulumi.set(__self__, "default_value", default_value)
        if effective_start and not isinstance(effective_start, str):
            raise TypeError("Expected argument 'effective_start' to be a str")
        pulumi.set(__self__, "effective_start", effective_start)
        if rule_version and not isinstance(rule_version, str):
            raise TypeError("Expected argument 'rule_version' to be a str")
        pulumi.set(__self__, "rule_version", rule_version)
        if rules and not isinstance(rules, str):
            raise TypeError("Expected argument 'rules' to be a str")
        pulumi.set(__self__, "rules", rules)
        if split_charge_rules and not isinstance(split_charge_rules, str):
            raise TypeError("Expected argument 'split_charge_rules' to be a str")
        pulumi.set(__self__, "split_charge_rules", split_charge_rules)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Cost category ARN
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="defaultValue")
    def default_value(self) -> Optional[str]:
        """
        The default value for the cost category
        """
        return pulumi.get(self, "default_value")

    @property
    @pulumi.getter(name="effectiveStart")
    def effective_start(self) -> Optional[str]:
        return pulumi.get(self, "effective_start")

    @property
    @pulumi.getter(name="ruleVersion")
    def rule_version(self) -> Optional['CostCategoryRuleVersion']:
        return pulumi.get(self, "rule_version")

    @property
    @pulumi.getter
    def rules(self) -> Optional[str]:
        """
        JSON array format of Expression in Billing and Cost Management API
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="splitChargeRules")
    def split_charge_rules(self) -> Optional[str]:
        """
        Json array format of CostCategorySplitChargeRule in Billing and Cost Management API
        """
        return pulumi.get(self, "split_charge_rules")


class AwaitableGetCostCategoryResult(GetCostCategoryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCostCategoryResult(
            arn=self.arn,
            default_value=self.default_value,
            effective_start=self.effective_start,
            rule_version=self.rule_version,
            rules=self.rules,
            split_charge_rules=self.split_charge_rules)


def get_cost_category(arn: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCostCategoryResult:
    """
    Cost Category enables you to map your cost and usage into meaningful categories. You can use Cost Category to organize your costs using a rule-based engine.


    :param str arn: Cost category ARN
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ce:getCostCategory', __args__, opts=opts, typ=GetCostCategoryResult).value

    return AwaitableGetCostCategoryResult(
        arn=pulumi.get(__ret__, 'arn'),
        default_value=pulumi.get(__ret__, 'default_value'),
        effective_start=pulumi.get(__ret__, 'effective_start'),
        rule_version=pulumi.get(__ret__, 'rule_version'),
        rules=pulumi.get(__ret__, 'rules'),
        split_charge_rules=pulumi.get(__ret__, 'split_charge_rules'))


@_utilities.lift_output_func(get_cost_category)
def get_cost_category_output(arn: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCostCategoryResult]:
    """
    Cost Category enables you to map your cost and usage into meaningful categories. You can use Cost Category to organize your costs using a rule-based engine.


    :param str arn: Cost category ARN
    """
    ...
