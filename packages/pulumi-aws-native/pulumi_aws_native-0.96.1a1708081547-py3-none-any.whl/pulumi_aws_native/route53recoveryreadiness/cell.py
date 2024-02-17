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
from ._inputs import *

__all__ = ['CellArgs', 'Cell']

@pulumi.input_type
class CellArgs:
    def __init__(__self__, *,
                 cell_name: Optional[pulumi.Input[str]] = None,
                 cells: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['CellTagArgs']]]] = None):
        """
        The set of arguments for constructing a Cell resource.
        :param pulumi.Input[str] cell_name: The name of the cell to create.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] cells: A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells. For example, Availability Zones within specific Regions.
        :param pulumi.Input[Sequence[pulumi.Input['CellTagArgs']]] tags: A collection of tags associated with a resource
        """
        if cell_name is not None:
            pulumi.set(__self__, "cell_name", cell_name)
        if cells is not None:
            pulumi.set(__self__, "cells", cells)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="cellName")
    def cell_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the cell to create.
        """
        return pulumi.get(self, "cell_name")

    @cell_name.setter
    def cell_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cell_name", value)

    @property
    @pulumi.getter
    def cells(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells. For example, Availability Zones within specific Regions.
        """
        return pulumi.get(self, "cells")

    @cells.setter
    def cells(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "cells", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CellTagArgs']]]]:
        """
        A collection of tags associated with a resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CellTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Cell(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cell_name: Optional[pulumi.Input[str]] = None,
                 cells: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CellTagArgs']]]]] = None,
                 __props__=None):
        """
        The API Schema for AWS Route53 Recovery Readiness Cells.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cell_name: The name of the cell to create.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] cells: A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells. For example, Availability Zones within specific Regions.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CellTagArgs']]]] tags: A collection of tags associated with a resource
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[CellArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The API Schema for AWS Route53 Recovery Readiness Cells.

        :param str resource_name: The name of the resource.
        :param CellArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CellArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cell_name: Optional[pulumi.Input[str]] = None,
                 cells: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CellTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CellArgs.__new__(CellArgs)

            __props__.__dict__["cell_name"] = cell_name
            __props__.__dict__["cells"] = cells
            __props__.__dict__["tags"] = tags
            __props__.__dict__["cell_arn"] = None
            __props__.__dict__["parent_readiness_scopes"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["cell_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Cell, __self__).__init__(
            'aws-native:route53recoveryreadiness:Cell',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Cell':
        """
        Get an existing Cell resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CellArgs.__new__(CellArgs)

        __props__.__dict__["cell_arn"] = None
        __props__.__dict__["cell_name"] = None
        __props__.__dict__["cells"] = None
        __props__.__dict__["parent_readiness_scopes"] = None
        __props__.__dict__["tags"] = None
        return Cell(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cellArn")
    def cell_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the cell.
        """
        return pulumi.get(self, "cell_arn")

    @property
    @pulumi.getter(name="cellName")
    def cell_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the cell to create.
        """
        return pulumi.get(self, "cell_name")

    @property
    @pulumi.getter
    def cells(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells. For example, Availability Zones within specific Regions.
        """
        return pulumi.get(self, "cells")

    @property
    @pulumi.getter(name="parentReadinessScopes")
    def parent_readiness_scopes(self) -> pulumi.Output[Sequence[str]]:
        """
        The readiness scope for the cell, which can be a cell Amazon Resource Name (ARN) or a recovery group ARN. This is a list but currently can have only one element.
        """
        return pulumi.get(self, "parent_readiness_scopes")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.CellTag']]]:
        """
        A collection of tags associated with a resource
        """
        return pulumi.get(self, "tags")

