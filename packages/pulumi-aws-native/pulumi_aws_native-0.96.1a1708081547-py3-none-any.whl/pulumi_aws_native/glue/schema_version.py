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

__all__ = ['SchemaVersionInitArgs', 'SchemaVersion']

@pulumi.input_type
class SchemaVersionInitArgs:
    def __init__(__self__, *,
                 schema: pulumi.Input['SchemaVersionSchemaArgs'],
                 schema_definition: pulumi.Input[str]):
        """
        The set of arguments for constructing a SchemaVersion resource.
        :param pulumi.Input[str] schema_definition: Complete definition of the schema in plain-text.
        """
        pulumi.set(__self__, "schema", schema)
        pulumi.set(__self__, "schema_definition", schema_definition)

    @property
    @pulumi.getter
    def schema(self) -> pulumi.Input['SchemaVersionSchemaArgs']:
        return pulumi.get(self, "schema")

    @schema.setter
    def schema(self, value: pulumi.Input['SchemaVersionSchemaArgs']):
        pulumi.set(self, "schema", value)

    @property
    @pulumi.getter(name="schemaDefinition")
    def schema_definition(self) -> pulumi.Input[str]:
        """
        Complete definition of the schema in plain-text.
        """
        return pulumi.get(self, "schema_definition")

    @schema_definition.setter
    def schema_definition(self, value: pulumi.Input[str]):
        pulumi.set(self, "schema_definition", value)


class SchemaVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 schema: Optional[pulumi.Input[pulumi.InputType['SchemaVersionSchemaArgs']]] = None,
                 schema_definition: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource represents an individual schema version of a schema defined in Glue Schema Registry.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] schema_definition: Complete definition of the schema in plain-text.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SchemaVersionInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource represents an individual schema version of a schema defined in Glue Schema Registry.

        :param str resource_name: The name of the resource.
        :param SchemaVersionInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SchemaVersionInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 schema: Optional[pulumi.Input[pulumi.InputType['SchemaVersionSchemaArgs']]] = None,
                 schema_definition: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SchemaVersionInitArgs.__new__(SchemaVersionInitArgs)

            if schema is None and not opts.urn:
                raise TypeError("Missing required property 'schema'")
            __props__.__dict__["schema"] = schema
            if schema_definition is None and not opts.urn:
                raise TypeError("Missing required property 'schema_definition'")
            __props__.__dict__["schema_definition"] = schema_definition
            __props__.__dict__["version_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["schema", "schema_definition"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(SchemaVersion, __self__).__init__(
            'aws-native:glue:SchemaVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SchemaVersion':
        """
        Get an existing SchemaVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SchemaVersionInitArgs.__new__(SchemaVersionInitArgs)

        __props__.__dict__["schema"] = None
        __props__.__dict__["schema_definition"] = None
        __props__.__dict__["version_id"] = None
        return SchemaVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def schema(self) -> pulumi.Output['outputs.SchemaVersionSchema']:
        return pulumi.get(self, "schema")

    @property
    @pulumi.getter(name="schemaDefinition")
    def schema_definition(self) -> pulumi.Output[str]:
        """
        Complete definition of the schema in plain-text.
        """
        return pulumi.get(self, "schema_definition")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> pulumi.Output[str]:
        """
        Represents the version ID associated with the schema version.
        """
        return pulumi.get(self, "version_id")

