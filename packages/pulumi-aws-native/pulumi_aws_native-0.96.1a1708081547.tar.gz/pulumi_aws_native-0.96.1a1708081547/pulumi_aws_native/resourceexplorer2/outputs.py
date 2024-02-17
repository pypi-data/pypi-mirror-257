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
    'IndexTagMap',
    'ViewIncludedProperty',
    'ViewSearchFilter',
    'ViewTagMap',
]

@pulumi.output_type
class IndexTagMap(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ViewIncludedProperty(dict):
    def __init__(__self__, *,
                 name: str):
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")


@pulumi.output_type
class ViewSearchFilter(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "filterString":
            suggest = "filter_string"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ViewSearchFilter. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ViewSearchFilter.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ViewSearchFilter.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 filter_string: str):
        pulumi.set(__self__, "filter_string", filter_string)

    @property
    @pulumi.getter(name="filterString")
    def filter_string(self) -> str:
        return pulumi.get(self, "filter_string")


@pulumi.output_type
class ViewTagMap(dict):
    def __init__(__self__):
        pass


