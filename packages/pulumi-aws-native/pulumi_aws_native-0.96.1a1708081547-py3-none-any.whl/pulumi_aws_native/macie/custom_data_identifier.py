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

__all__ = ['CustomDataIdentifierArgs', 'CustomDataIdentifier']

@pulumi.input_type
class CustomDataIdentifierArgs:
    def __init__(__self__, *,
                 regex: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 ignore_words: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 keywords: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 maximum_match_distance: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['CustomDataIdentifierTagArgs']]]] = None):
        """
        The set of arguments for constructing a CustomDataIdentifier resource.
        :param pulumi.Input[str] regex: Regular expression for custom data identifier.
        :param pulumi.Input[str] description: Description of custom data identifier.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ignore_words: Words to be ignored.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] keywords: Keywords to be matched against.
        :param pulumi.Input[int] maximum_match_distance: Maximum match distance.
        :param pulumi.Input[str] name: Name of custom data identifier.
        :param pulumi.Input[Sequence[pulumi.Input['CustomDataIdentifierTagArgs']]] tags: A collection of tags associated with a resource
        """
        pulumi.set(__self__, "regex", regex)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if ignore_words is not None:
            pulumi.set(__self__, "ignore_words", ignore_words)
        if keywords is not None:
            pulumi.set(__self__, "keywords", keywords)
        if maximum_match_distance is not None:
            pulumi.set(__self__, "maximum_match_distance", maximum_match_distance)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def regex(self) -> pulumi.Input[str]:
        """
        Regular expression for custom data identifier.
        """
        return pulumi.get(self, "regex")

    @regex.setter
    def regex(self, value: pulumi.Input[str]):
        pulumi.set(self, "regex", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of custom data identifier.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="ignoreWords")
    def ignore_words(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Words to be ignored.
        """
        return pulumi.get(self, "ignore_words")

    @ignore_words.setter
    def ignore_words(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ignore_words", value)

    @property
    @pulumi.getter
    def keywords(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Keywords to be matched against.
        """
        return pulumi.get(self, "keywords")

    @keywords.setter
    def keywords(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "keywords", value)

    @property
    @pulumi.getter(name="maximumMatchDistance")
    def maximum_match_distance(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum match distance.
        """
        return pulumi.get(self, "maximum_match_distance")

    @maximum_match_distance.setter
    def maximum_match_distance(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "maximum_match_distance", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of custom data identifier.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CustomDataIdentifierTagArgs']]]]:
        """
        A collection of tags associated with a resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CustomDataIdentifierTagArgs']]]]):
        pulumi.set(self, "tags", value)


class CustomDataIdentifier(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ignore_words: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 keywords: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 maximum_match_distance: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 regex: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CustomDataIdentifierTagArgs']]]]] = None,
                 __props__=None):
        """
        Macie CustomDataIdentifier resource schema

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of custom data identifier.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ignore_words: Words to be ignored.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] keywords: Keywords to be matched against.
        :param pulumi.Input[int] maximum_match_distance: Maximum match distance.
        :param pulumi.Input[str] name: Name of custom data identifier.
        :param pulumi.Input[str] regex: Regular expression for custom data identifier.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CustomDataIdentifierTagArgs']]]] tags: A collection of tags associated with a resource
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CustomDataIdentifierArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Macie CustomDataIdentifier resource schema

        :param str resource_name: The name of the resource.
        :param CustomDataIdentifierArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CustomDataIdentifierArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ignore_words: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 keywords: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 maximum_match_distance: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 regex: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CustomDataIdentifierTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CustomDataIdentifierArgs.__new__(CustomDataIdentifierArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["ignore_words"] = ignore_words
            __props__.__dict__["keywords"] = keywords
            __props__.__dict__["maximum_match_distance"] = maximum_match_distance
            __props__.__dict__["name"] = name
            if regex is None and not opts.urn:
                raise TypeError("Missing required property 'regex'")
            __props__.__dict__["regex"] = regex
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["description", "ignore_words[*]", "keywords[*]", "maximum_match_distance", "name", "regex"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(CustomDataIdentifier, __self__).__init__(
            'aws-native:macie:CustomDataIdentifier',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'CustomDataIdentifier':
        """
        Get an existing CustomDataIdentifier resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CustomDataIdentifierArgs.__new__(CustomDataIdentifierArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["ignore_words"] = None
        __props__.__dict__["keywords"] = None
        __props__.__dict__["maximum_match_distance"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["regex"] = None
        __props__.__dict__["tags"] = None
        return CustomDataIdentifier(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Custom data identifier ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of custom data identifier.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="ignoreWords")
    def ignore_words(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Words to be ignored.
        """
        return pulumi.get(self, "ignore_words")

    @property
    @pulumi.getter
    def keywords(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Keywords to be matched against.
        """
        return pulumi.get(self, "keywords")

    @property
    @pulumi.getter(name="maximumMatchDistance")
    def maximum_match_distance(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum match distance.
        """
        return pulumi.get(self, "maximum_match_distance")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of custom data identifier.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def regex(self) -> pulumi.Output[str]:
        """
        Regular expression for custom data identifier.
        """
        return pulumi.get(self, "regex")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.CustomDataIdentifierTag']]]:
        """
        A collection of tags associated with a resource
        """
        return pulumi.get(self, "tags")

