# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'BillingGroupStatus',
    'CustomLineItemCurrencyCode',
    'CustomLineItemLineItemFilterAttribute',
    'CustomLineItemLineItemFilterMatchOption',
    'CustomLineItemLineItemFilterValue',
    'CustomLineItemType',
    'PricingRuleBillingEntity',
    'PricingRuleScope',
    'PricingRuleType',
]


class BillingGroupStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PRIMARY_ACCOUNT_MISSING = "PRIMARY_ACCOUNT_MISSING"


class CustomLineItemCurrencyCode(str, Enum):
    USD = "USD"
    CNY = "CNY"


class CustomLineItemLineItemFilterAttribute(str, Enum):
    LINE_ITEM_TYPE = "LINE_ITEM_TYPE"


class CustomLineItemLineItemFilterMatchOption(str, Enum):
    NOT_EQUAL = "NOT_EQUAL"


class CustomLineItemLineItemFilterValue(str, Enum):
    SAVINGS_PLAN_NEGATION = "SAVINGS_PLAN_NEGATION"


class CustomLineItemType(str, Enum):
    FEE = "FEE"
    CREDIT = "CREDIT"


class PricingRuleBillingEntity(str, Enum):
    """
    The seller of services provided by AWS, their affiliates, or third-party providers selling services via AWS Marketplaces. Supported billing entities are AWS, AWS Marketplace, and AISPL.
    """
    AWS = "AWS"
    AWS_MARKETPLACE = "AWS Marketplace"
    AISPL = "AISPL"


class PricingRuleScope(str, Enum):
    """
    A term used to categorize the granularity of a Pricing Rule.
    """
    GLOBAL_ = "GLOBAL"
    SERVICE = "SERVICE"
    BILLING_ENTITY = "BILLING_ENTITY"
    SKU = "SKU"


class PricingRuleType(str, Enum):
    """
    One of MARKUP, DISCOUNT or TIERING that describes the behaviour of the pricing rule.
    """
    MARKUP = "MARKUP"
    DISCOUNT = "DISCOUNT"
    TIERING = "TIERING"
