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

__all__ = ['ObjectTypeArgs', 'ObjectType']

@pulumi.input_type
class ObjectTypeArgs:
    def __init__(__self__, *,
                 domain_name: pulumi.Input[str],
                 allow_profile_creation: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_key: Optional[pulumi.Input[str]] = None,
                 expiration_days: Optional[pulumi.Input[int]] = None,
                 fields: Optional[pulumi.Input[Sequence[pulumi.Input['ObjectTypeFieldMapArgs']]]] = None,
                 keys: Optional[pulumi.Input[Sequence[pulumi.Input['ObjectTypeKeyMapArgs']]]] = None,
                 object_type_name: Optional[pulumi.Input[str]] = None,
                 source_last_updated_timestamp_format: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['ObjectTypeTagArgs']]]] = None,
                 template_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ObjectType resource.
        :param pulumi.Input[str] domain_name: The unique name of the domain.
        :param pulumi.Input[bool] allow_profile_creation: Indicates whether a profile should be created when data is received.
        :param pulumi.Input[str] description: Description of the profile object type.
        :param pulumi.Input[str] encryption_key: The default encryption key
        :param pulumi.Input[int] expiration_days: The default number of days until the data within the domain expires.
        :param pulumi.Input[Sequence[pulumi.Input['ObjectTypeFieldMapArgs']]] fields: A list of the name and ObjectType field.
        :param pulumi.Input[Sequence[pulumi.Input['ObjectTypeKeyMapArgs']]] keys: A list of unique keys that can be used to map data to the profile.
        :param pulumi.Input[str] object_type_name: The name of the profile object type.
        :param pulumi.Input[str] source_last_updated_timestamp_format: The format of your sourceLastUpdatedTimestamp that was previously set up.
        :param pulumi.Input[Sequence[pulumi.Input['ObjectTypeTagArgs']]] tags: The tags (keys and values) associated with the integration.
        :param pulumi.Input[str] template_id: A unique identifier for the object template.
        """
        pulumi.set(__self__, "domain_name", domain_name)
        if allow_profile_creation is not None:
            pulumi.set(__self__, "allow_profile_creation", allow_profile_creation)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encryption_key is not None:
            pulumi.set(__self__, "encryption_key", encryption_key)
        if expiration_days is not None:
            pulumi.set(__self__, "expiration_days", expiration_days)
        if fields is not None:
            pulumi.set(__self__, "fields", fields)
        if keys is not None:
            pulumi.set(__self__, "keys", keys)
        if object_type_name is not None:
            pulumi.set(__self__, "object_type_name", object_type_name)
        if source_last_updated_timestamp_format is not None:
            pulumi.set(__self__, "source_last_updated_timestamp_format", source_last_updated_timestamp_format)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if template_id is not None:
            pulumi.set(__self__, "template_id", template_id)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Input[str]:
        """
        The unique name of the domain.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="allowProfileCreation")
    def allow_profile_creation(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether a profile should be created when data is received.
        """
        return pulumi.get(self, "allow_profile_creation")

    @allow_profile_creation.setter
    def allow_profile_creation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_profile_creation", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the profile object type.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="encryptionKey")
    def encryption_key(self) -> Optional[pulumi.Input[str]]:
        """
        The default encryption key
        """
        return pulumi.get(self, "encryption_key")

    @encryption_key.setter
    def encryption_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encryption_key", value)

    @property
    @pulumi.getter(name="expirationDays")
    def expiration_days(self) -> Optional[pulumi.Input[int]]:
        """
        The default number of days until the data within the domain expires.
        """
        return pulumi.get(self, "expiration_days")

    @expiration_days.setter
    def expiration_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expiration_days", value)

    @property
    @pulumi.getter
    def fields(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ObjectTypeFieldMapArgs']]]]:
        """
        A list of the name and ObjectType field.
        """
        return pulumi.get(self, "fields")

    @fields.setter
    def fields(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ObjectTypeFieldMapArgs']]]]):
        pulumi.set(self, "fields", value)

    @property
    @pulumi.getter
    def keys(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ObjectTypeKeyMapArgs']]]]:
        """
        A list of unique keys that can be used to map data to the profile.
        """
        return pulumi.get(self, "keys")

    @keys.setter
    def keys(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ObjectTypeKeyMapArgs']]]]):
        pulumi.set(self, "keys", value)

    @property
    @pulumi.getter(name="objectTypeName")
    def object_type_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the profile object type.
        """
        return pulumi.get(self, "object_type_name")

    @object_type_name.setter
    def object_type_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "object_type_name", value)

    @property
    @pulumi.getter(name="sourceLastUpdatedTimestampFormat")
    def source_last_updated_timestamp_format(self) -> Optional[pulumi.Input[str]]:
        """
        The format of your sourceLastUpdatedTimestamp that was previously set up.
        """
        return pulumi.get(self, "source_last_updated_timestamp_format")

    @source_last_updated_timestamp_format.setter
    def source_last_updated_timestamp_format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_last_updated_timestamp_format", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ObjectTypeTagArgs']]]]:
        """
        The tags (keys and values) associated with the integration.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ObjectTypeTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="templateId")
    def template_id(self) -> Optional[pulumi.Input[str]]:
        """
        A unique identifier for the object template.
        """
        return pulumi.get(self, "template_id")

    @template_id.setter
    def template_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_id", value)


class ObjectType(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_profile_creation: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 encryption_key: Optional[pulumi.Input[str]] = None,
                 expiration_days: Optional[pulumi.Input[int]] = None,
                 fields: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectTypeFieldMapArgs']]]]] = None,
                 keys: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectTypeKeyMapArgs']]]]] = None,
                 object_type_name: Optional[pulumi.Input[str]] = None,
                 source_last_updated_timestamp_format: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectTypeTagArgs']]]]] = None,
                 template_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An ObjectType resource of Amazon Connect Customer Profiles

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_profile_creation: Indicates whether a profile should be created when data is received.
        :param pulumi.Input[str] description: Description of the profile object type.
        :param pulumi.Input[str] domain_name: The unique name of the domain.
        :param pulumi.Input[str] encryption_key: The default encryption key
        :param pulumi.Input[int] expiration_days: The default number of days until the data within the domain expires.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectTypeFieldMapArgs']]]] fields: A list of the name and ObjectType field.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectTypeKeyMapArgs']]]] keys: A list of unique keys that can be used to map data to the profile.
        :param pulumi.Input[str] object_type_name: The name of the profile object type.
        :param pulumi.Input[str] source_last_updated_timestamp_format: The format of your sourceLastUpdatedTimestamp that was previously set up.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectTypeTagArgs']]]] tags: The tags (keys and values) associated with the integration.
        :param pulumi.Input[str] template_id: A unique identifier for the object template.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ObjectTypeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An ObjectType resource of Amazon Connect Customer Profiles

        :param str resource_name: The name of the resource.
        :param ObjectTypeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ObjectTypeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_profile_creation: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 encryption_key: Optional[pulumi.Input[str]] = None,
                 expiration_days: Optional[pulumi.Input[int]] = None,
                 fields: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectTypeFieldMapArgs']]]]] = None,
                 keys: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectTypeKeyMapArgs']]]]] = None,
                 object_type_name: Optional[pulumi.Input[str]] = None,
                 source_last_updated_timestamp_format: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectTypeTagArgs']]]]] = None,
                 template_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ObjectTypeArgs.__new__(ObjectTypeArgs)

            __props__.__dict__["allow_profile_creation"] = allow_profile_creation
            __props__.__dict__["description"] = description
            if domain_name is None and not opts.urn:
                raise TypeError("Missing required property 'domain_name'")
            __props__.__dict__["domain_name"] = domain_name
            __props__.__dict__["encryption_key"] = encryption_key
            __props__.__dict__["expiration_days"] = expiration_days
            __props__.__dict__["fields"] = fields
            __props__.__dict__["keys"] = keys
            __props__.__dict__["object_type_name"] = object_type_name
            __props__.__dict__["source_last_updated_timestamp_format"] = source_last_updated_timestamp_format
            __props__.__dict__["tags"] = tags
            __props__.__dict__["template_id"] = template_id
            __props__.__dict__["created_at"] = None
            __props__.__dict__["last_updated_at"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["domain_name", "object_type_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ObjectType, __self__).__init__(
            'aws-native:customerprofiles:ObjectType',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ObjectType':
        """
        Get an existing ObjectType resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ObjectTypeArgs.__new__(ObjectTypeArgs)

        __props__.__dict__["allow_profile_creation"] = None
        __props__.__dict__["created_at"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["domain_name"] = None
        __props__.__dict__["encryption_key"] = None
        __props__.__dict__["expiration_days"] = None
        __props__.__dict__["fields"] = None
        __props__.__dict__["keys"] = None
        __props__.__dict__["last_updated_at"] = None
        __props__.__dict__["object_type_name"] = None
        __props__.__dict__["source_last_updated_timestamp_format"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["template_id"] = None
        return ObjectType(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowProfileCreation")
    def allow_profile_creation(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether a profile should be created when data is received.
        """
        return pulumi.get(self, "allow_profile_creation")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The time of this integration got created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the profile object type.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        The unique name of the domain.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="encryptionKey")
    def encryption_key(self) -> pulumi.Output[Optional[str]]:
        """
        The default encryption key
        """
        return pulumi.get(self, "encryption_key")

    @property
    @pulumi.getter(name="expirationDays")
    def expiration_days(self) -> pulumi.Output[Optional[int]]:
        """
        The default number of days until the data within the domain expires.
        """
        return pulumi.get(self, "expiration_days")

    @property
    @pulumi.getter
    def fields(self) -> pulumi.Output[Optional[Sequence['outputs.ObjectTypeFieldMap']]]:
        """
        A list of the name and ObjectType field.
        """
        return pulumi.get(self, "fields")

    @property
    @pulumi.getter
    def keys(self) -> pulumi.Output[Optional[Sequence['outputs.ObjectTypeKeyMap']]]:
        """
        A list of unique keys that can be used to map data to the profile.
        """
        return pulumi.get(self, "keys")

    @property
    @pulumi.getter(name="lastUpdatedAt")
    def last_updated_at(self) -> pulumi.Output[str]:
        """
        The time of this integration got last updated at.
        """
        return pulumi.get(self, "last_updated_at")

    @property
    @pulumi.getter(name="objectTypeName")
    def object_type_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the profile object type.
        """
        return pulumi.get(self, "object_type_name")

    @property
    @pulumi.getter(name="sourceLastUpdatedTimestampFormat")
    def source_last_updated_timestamp_format(self) -> pulumi.Output[Optional[str]]:
        """
        The format of your sourceLastUpdatedTimestamp that was previously set up.
        """
        return pulumi.get(self, "source_last_updated_timestamp_format")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.ObjectTypeTag']]]:
        """
        The tags (keys and values) associated with the integration.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="templateId")
    def template_id(self) -> pulumi.Output[Optional[str]]:
        """
        A unique identifier for the object template.
        """
        return pulumi.get(self, "template_id")

