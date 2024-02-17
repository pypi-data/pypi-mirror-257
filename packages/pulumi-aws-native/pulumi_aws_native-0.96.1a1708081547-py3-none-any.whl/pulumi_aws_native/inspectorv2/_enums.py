# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'CisScanConfigurationCisSecurityLevel',
    'CisScanConfigurationDay',
    'FilterAction',
    'FilterMapComparison',
    'FilterStringComparison',
]


class CisScanConfigurationCisSecurityLevel(str, Enum):
    LEVEL1 = "LEVEL_1"
    LEVEL2 = "LEVEL_2"


class CisScanConfigurationDay(str, Enum):
    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"
    SUN = "SUN"


class FilterAction(str, Enum):
    NONE = "NONE"
    SUPPRESS = "SUPPRESS"


class FilterMapComparison(str, Enum):
    EQUALS = "EQUALS"


class FilterStringComparison(str, Enum):
    EQUALS = "EQUALS"
    PREFIX = "PREFIX"
    NOT_EQUALS = "NOT_EQUALS"
