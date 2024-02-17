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
from ._inputs import *

__all__ = ['ComponentTypeArgs', 'ComponentType']

@pulumi.input_type
class ComponentTypeArgs:
    def __init__(__self__, *,
                 component_type_id: pulumi.Input[str],
                 workspace_id: pulumi.Input[str],
                 composite_component_types: Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypeCompositeComponentTypeArgs']]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 extends_from: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 functions: Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypeFunctionArgs']]]] = None,
                 is_singleton: Optional[pulumi.Input[bool]] = None,
                 property_definitions: Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypePropertyDefinitionArgs']]]] = None,
                 property_groups: Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypePropertyGroupArgs']]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ComponentType resource.
        :param pulumi.Input[str] component_type_id: The ID of the component type.
        :param pulumi.Input[str] workspace_id: The ID of the workspace that contains the component type.
        :param pulumi.Input[Mapping[str, pulumi.Input['ComponentTypeCompositeComponentTypeArgs']]] composite_component_types: An map of the composite component types in the component type. Each composite component type's key must be unique to this map.
        :param pulumi.Input[str] description: The description of the component type.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] extends_from: Specifies the parent component type to extend.
        :param pulumi.Input[Mapping[str, pulumi.Input['ComponentTypeFunctionArgs']]] functions: a Map of functions in the component type. Each function's key must be unique to this map.
        :param pulumi.Input[bool] is_singleton: A Boolean value that specifies whether an entity can have more than one component of this type.
        :param pulumi.Input[Mapping[str, pulumi.Input['ComponentTypePropertyDefinitionArgs']]] property_definitions: An map of the property definitions in the component type. Each property definition's key must be unique to this map.
        :param pulumi.Input[Mapping[str, pulumi.Input['ComponentTypePropertyGroupArgs']]] property_groups: An map of the property groups in the component type. Each property group's key must be unique to this map.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of key-value pairs to associate with a resource.
        """
        pulumi.set(__self__, "component_type_id", component_type_id)
        pulumi.set(__self__, "workspace_id", workspace_id)
        if composite_component_types is not None:
            pulumi.set(__self__, "composite_component_types", composite_component_types)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if extends_from is not None:
            pulumi.set(__self__, "extends_from", extends_from)
        if functions is not None:
            pulumi.set(__self__, "functions", functions)
        if is_singleton is not None:
            pulumi.set(__self__, "is_singleton", is_singleton)
        if property_definitions is not None:
            pulumi.set(__self__, "property_definitions", property_definitions)
        if property_groups is not None:
            pulumi.set(__self__, "property_groups", property_groups)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="componentTypeId")
    def component_type_id(self) -> pulumi.Input[str]:
        """
        The ID of the component type.
        """
        return pulumi.get(self, "component_type_id")

    @component_type_id.setter
    def component_type_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "component_type_id", value)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Input[str]:
        """
        The ID of the workspace that contains the component type.
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_id", value)

    @property
    @pulumi.getter(name="compositeComponentTypes")
    def composite_component_types(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypeCompositeComponentTypeArgs']]]]:
        """
        An map of the composite component types in the component type. Each composite component type's key must be unique to this map.
        """
        return pulumi.get(self, "composite_component_types")

    @composite_component_types.setter
    def composite_component_types(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypeCompositeComponentTypeArgs']]]]):
        pulumi.set(self, "composite_component_types", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the component type.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="extendsFrom")
    def extends_from(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the parent component type to extend.
        """
        return pulumi.get(self, "extends_from")

    @extends_from.setter
    def extends_from(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "extends_from", value)

    @property
    @pulumi.getter
    def functions(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypeFunctionArgs']]]]:
        """
        a Map of functions in the component type. Each function's key must be unique to this map.
        """
        return pulumi.get(self, "functions")

    @functions.setter
    def functions(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypeFunctionArgs']]]]):
        pulumi.set(self, "functions", value)

    @property
    @pulumi.getter(name="isSingleton")
    def is_singleton(self) -> Optional[pulumi.Input[bool]]:
        """
        A Boolean value that specifies whether an entity can have more than one component of this type.
        """
        return pulumi.get(self, "is_singleton")

    @is_singleton.setter
    def is_singleton(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_singleton", value)

    @property
    @pulumi.getter(name="propertyDefinitions")
    def property_definitions(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypePropertyDefinitionArgs']]]]:
        """
        An map of the property definitions in the component type. Each property definition's key must be unique to this map.
        """
        return pulumi.get(self, "property_definitions")

    @property_definitions.setter
    def property_definitions(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypePropertyDefinitionArgs']]]]):
        pulumi.set(self, "property_definitions", value)

    @property
    @pulumi.getter(name="propertyGroups")
    def property_groups(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypePropertyGroupArgs']]]]:
        """
        An map of the property groups in the component type. Each property group's key must be unique to this map.
        """
        return pulumi.get(self, "property_groups")

    @property_groups.setter
    def property_groups(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['ComponentTypePropertyGroupArgs']]]]):
        pulumi.set(self, "property_groups", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of key-value pairs to associate with a resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class ComponentType(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 component_type_id: Optional[pulumi.Input[str]] = None,
                 composite_component_types: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypeCompositeComponentTypeArgs']]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 extends_from: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 functions: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypeFunctionArgs']]]]] = None,
                 is_singleton: Optional[pulumi.Input[bool]] = None,
                 property_definitions: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypePropertyDefinitionArgs']]]]] = None,
                 property_groups: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypePropertyGroupArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource schema for AWS::IoTTwinMaker::ComponentType

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] component_type_id: The ID of the component type.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypeCompositeComponentTypeArgs']]]] composite_component_types: An map of the composite component types in the component type. Each composite component type's key must be unique to this map.
        :param pulumi.Input[str] description: The description of the component type.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] extends_from: Specifies the parent component type to extend.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypeFunctionArgs']]]] functions: a Map of functions in the component type. Each function's key must be unique to this map.
        :param pulumi.Input[bool] is_singleton: A Boolean value that specifies whether an entity can have more than one component of this type.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypePropertyDefinitionArgs']]]] property_definitions: An map of the property definitions in the component type. Each property definition's key must be unique to this map.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypePropertyGroupArgs']]]] property_groups: An map of the property groups in the component type. Each property group's key must be unique to this map.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of key-value pairs to associate with a resource.
        :param pulumi.Input[str] workspace_id: The ID of the workspace that contains the component type.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ComponentTypeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::IoTTwinMaker::ComponentType

        :param str resource_name: The name of the resource.
        :param ComponentTypeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ComponentTypeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 component_type_id: Optional[pulumi.Input[str]] = None,
                 composite_component_types: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypeCompositeComponentTypeArgs']]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 extends_from: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 functions: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypeFunctionArgs']]]]] = None,
                 is_singleton: Optional[pulumi.Input[bool]] = None,
                 property_definitions: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypePropertyDefinitionArgs']]]]] = None,
                 property_groups: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ComponentTypePropertyGroupArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ComponentTypeArgs.__new__(ComponentTypeArgs)

            if component_type_id is None and not opts.urn:
                raise TypeError("Missing required property 'component_type_id'")
            __props__.__dict__["component_type_id"] = component_type_id
            __props__.__dict__["composite_component_types"] = composite_component_types
            __props__.__dict__["description"] = description
            __props__.__dict__["extends_from"] = extends_from
            __props__.__dict__["functions"] = functions
            __props__.__dict__["is_singleton"] = is_singleton
            __props__.__dict__["property_definitions"] = property_definitions
            __props__.__dict__["property_groups"] = property_groups
            __props__.__dict__["tags"] = tags
            if workspace_id is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_id'")
            __props__.__dict__["workspace_id"] = workspace_id
            __props__.__dict__["arn"] = None
            __props__.__dict__["creation_date_time"] = None
            __props__.__dict__["is_abstract"] = None
            __props__.__dict__["is_schema_initialized"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["update_date_time"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["component_type_id", "workspace_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ComponentType, __self__).__init__(
            'aws-native:iottwinmaker:ComponentType',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ComponentType':
        """
        Get an existing ComponentType resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ComponentTypeArgs.__new__(ComponentTypeArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["component_type_id"] = None
        __props__.__dict__["composite_component_types"] = None
        __props__.__dict__["creation_date_time"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["extends_from"] = None
        __props__.__dict__["functions"] = None
        __props__.__dict__["is_abstract"] = None
        __props__.__dict__["is_schema_initialized"] = None
        __props__.__dict__["is_singleton"] = None
        __props__.__dict__["property_definitions"] = None
        __props__.__dict__["property_groups"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["update_date_time"] = None
        __props__.__dict__["workspace_id"] = None
        return ComponentType(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the component type.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="componentTypeId")
    def component_type_id(self) -> pulumi.Output[str]:
        """
        The ID of the component type.
        """
        return pulumi.get(self, "component_type_id")

    @property
    @pulumi.getter(name="compositeComponentTypes")
    def composite_component_types(self) -> pulumi.Output[Optional[Mapping[str, 'outputs.ComponentTypeCompositeComponentType']]]:
        """
        An map of the composite component types in the component type. Each composite component type's key must be unique to this map.
        """
        return pulumi.get(self, "composite_component_types")

    @property
    @pulumi.getter(name="creationDateTime")
    def creation_date_time(self) -> pulumi.Output[str]:
        """
        The date and time when the component type was created.
        """
        return pulumi.get(self, "creation_date_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the component type.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="extendsFrom")
    def extends_from(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specifies the parent component type to extend.
        """
        return pulumi.get(self, "extends_from")

    @property
    @pulumi.getter
    def functions(self) -> pulumi.Output[Optional[Mapping[str, 'outputs.ComponentTypeFunction']]]:
        """
        a Map of functions in the component type. Each function's key must be unique to this map.
        """
        return pulumi.get(self, "functions")

    @property
    @pulumi.getter(name="isAbstract")
    def is_abstract(self) -> pulumi.Output[bool]:
        """
        A Boolean value that specifies whether the component type is abstract.
        """
        return pulumi.get(self, "is_abstract")

    @property
    @pulumi.getter(name="isSchemaInitialized")
    def is_schema_initialized(self) -> pulumi.Output[bool]:
        """
        A Boolean value that specifies whether the component type has a schema initializer and that the schema initializer has run.
        """
        return pulumi.get(self, "is_schema_initialized")

    @property
    @pulumi.getter(name="isSingleton")
    def is_singleton(self) -> pulumi.Output[Optional[bool]]:
        """
        A Boolean value that specifies whether an entity can have more than one component of this type.
        """
        return pulumi.get(self, "is_singleton")

    @property
    @pulumi.getter(name="propertyDefinitions")
    def property_definitions(self) -> pulumi.Output[Optional[Mapping[str, 'outputs.ComponentTypePropertyDefinition']]]:
        """
        An map of the property definitions in the component type. Each property definition's key must be unique to this map.
        """
        return pulumi.get(self, "property_definitions")

    @property
    @pulumi.getter(name="propertyGroups")
    def property_groups(self) -> pulumi.Output[Optional[Mapping[str, 'outputs.ComponentTypePropertyGroup']]]:
        """
        An map of the property groups in the component type. Each property group's key must be unique to this map.
        """
        return pulumi.get(self, "property_groups")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.ComponentTypeStatus']:
        """
        The current status of the component type.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of key-value pairs to associate with a resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updateDateTime")
    def update_date_time(self) -> pulumi.Output[str]:
        """
        The last date and time when the component type was updated.
        """
        return pulumi.get(self, "update_date_time")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Output[str]:
        """
        The ID of the workspace that contains the component type.
        """
        return pulumi.get(self, "workspace_id")

