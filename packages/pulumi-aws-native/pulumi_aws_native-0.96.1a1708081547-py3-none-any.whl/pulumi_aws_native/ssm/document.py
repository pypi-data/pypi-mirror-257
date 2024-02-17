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

__all__ = ['DocumentArgs', 'Document']

@pulumi.input_type
class DocumentArgs:
    def __init__(__self__, *,
                 content: Any,
                 attachments: Optional[pulumi.Input[Sequence[pulumi.Input['DocumentAttachmentsSourceArgs']]]] = None,
                 document_format: Optional[pulumi.Input['DocumentFormat']] = None,
                 document_type: Optional[pulumi.Input['DocumentType']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 requires: Optional[pulumi.Input[Sequence[pulumi.Input['DocumentRequiresArgs']]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['DocumentTagArgs']]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 update_method: Optional[pulumi.Input['DocumentUpdateMethod']] = None,
                 version_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Document resource.
        :param Any content: The content for the Systems Manager document in JSON, YAML or String format.
        :param pulumi.Input[Sequence[pulumi.Input['DocumentAttachmentsSourceArgs']]] attachments: A list of key and value pairs that describe attachments to a version of a document.
        :param pulumi.Input['DocumentFormat'] document_format: Specify the document format for the request. The document format can be either JSON or YAML. JSON is the default format.
        :param pulumi.Input['DocumentType'] document_type: The type of document to create.
        :param pulumi.Input[str] name: A name for the Systems Manager document.
        :param pulumi.Input[Sequence[pulumi.Input['DocumentRequiresArgs']]] requires: A list of SSM documents required by a document. For example, an ApplicationConfiguration document requires an ApplicationConfigurationSchema document.
        :param pulumi.Input[Sequence[pulumi.Input['DocumentTagArgs']]] tags: Optional metadata that you assign to a resource. Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment.
        :param pulumi.Input[str] target_type: Specify a target type to define the kinds of resources the document can run on.
        :param pulumi.Input['DocumentUpdateMethod'] update_method: Update method - when set to 'Replace', the update will replace the existing document; when set to 'NewVersion', the update will create a new version.
        :param pulumi.Input[str] version_name: An optional field specifying the version of the artifact you are creating with the document. This value is unique across all versions of a document, and cannot be changed.
        """
        pulumi.set(__self__, "content", content)
        if attachments is not None:
            pulumi.set(__self__, "attachments", attachments)
        if document_format is not None:
            pulumi.set(__self__, "document_format", document_format)
        if document_type is not None:
            pulumi.set(__self__, "document_type", document_type)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if requires is not None:
            pulumi.set(__self__, "requires", requires)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if target_type is not None:
            pulumi.set(__self__, "target_type", target_type)
        if update_method is not None:
            pulumi.set(__self__, "update_method", update_method)
        if version_name is not None:
            pulumi.set(__self__, "version_name", version_name)

    @property
    @pulumi.getter
    def content(self) -> Any:
        """
        The content for the Systems Manager document in JSON, YAML or String format.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Any):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter
    def attachments(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DocumentAttachmentsSourceArgs']]]]:
        """
        A list of key and value pairs that describe attachments to a version of a document.
        """
        return pulumi.get(self, "attachments")

    @attachments.setter
    def attachments(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DocumentAttachmentsSourceArgs']]]]):
        pulumi.set(self, "attachments", value)

    @property
    @pulumi.getter(name="documentFormat")
    def document_format(self) -> Optional[pulumi.Input['DocumentFormat']]:
        """
        Specify the document format for the request. The document format can be either JSON or YAML. JSON is the default format.
        """
        return pulumi.get(self, "document_format")

    @document_format.setter
    def document_format(self, value: Optional[pulumi.Input['DocumentFormat']]):
        pulumi.set(self, "document_format", value)

    @property
    @pulumi.getter(name="documentType")
    def document_type(self) -> Optional[pulumi.Input['DocumentType']]:
        """
        The type of document to create.
        """
        return pulumi.get(self, "document_type")

    @document_type.setter
    def document_type(self, value: Optional[pulumi.Input['DocumentType']]):
        pulumi.set(self, "document_type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the Systems Manager document.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def requires(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DocumentRequiresArgs']]]]:
        """
        A list of SSM documents required by a document. For example, an ApplicationConfiguration document requires an ApplicationConfigurationSchema document.
        """
        return pulumi.get(self, "requires")

    @requires.setter
    def requires(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DocumentRequiresArgs']]]]):
        pulumi.set(self, "requires", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DocumentTagArgs']]]]:
        """
        Optional metadata that you assign to a resource. Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DocumentTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> Optional[pulumi.Input[str]]:
        """
        Specify a target type to define the kinds of resources the document can run on.
        """
        return pulumi.get(self, "target_type")

    @target_type.setter
    def target_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_type", value)

    @property
    @pulumi.getter(name="updateMethod")
    def update_method(self) -> Optional[pulumi.Input['DocumentUpdateMethod']]:
        """
        Update method - when set to 'Replace', the update will replace the existing document; when set to 'NewVersion', the update will create a new version.
        """
        return pulumi.get(self, "update_method")

    @update_method.setter
    def update_method(self, value: Optional[pulumi.Input['DocumentUpdateMethod']]):
        pulumi.set(self, "update_method", value)

    @property
    @pulumi.getter(name="versionName")
    def version_name(self) -> Optional[pulumi.Input[str]]:
        """
        An optional field specifying the version of the artifact you are creating with the document. This value is unique across all versions of a document, and cannot be changed.
        """
        return pulumi.get(self, "version_name")

    @version_name.setter
    def version_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version_name", value)


class Document(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attachments: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DocumentAttachmentsSourceArgs']]]]] = None,
                 content: Optional[Any] = None,
                 document_format: Optional[pulumi.Input['DocumentFormat']] = None,
                 document_type: Optional[pulumi.Input['DocumentType']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 requires: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DocumentRequiresArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DocumentTagArgs']]]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 update_method: Optional[pulumi.Input['DocumentUpdateMethod']] = None,
                 version_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The AWS::SSM::Document resource is an SSM document in AWS Systems Manager that defines the actions that Systems Manager performs, which can be used to set up and run commands on your instances.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DocumentAttachmentsSourceArgs']]]] attachments: A list of key and value pairs that describe attachments to a version of a document.
        :param Any content: The content for the Systems Manager document in JSON, YAML or String format.
        :param pulumi.Input['DocumentFormat'] document_format: Specify the document format for the request. The document format can be either JSON or YAML. JSON is the default format.
        :param pulumi.Input['DocumentType'] document_type: The type of document to create.
        :param pulumi.Input[str] name: A name for the Systems Manager document.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DocumentRequiresArgs']]]] requires: A list of SSM documents required by a document. For example, an ApplicationConfiguration document requires an ApplicationConfigurationSchema document.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DocumentTagArgs']]]] tags: Optional metadata that you assign to a resource. Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment.
        :param pulumi.Input[str] target_type: Specify a target type to define the kinds of resources the document can run on.
        :param pulumi.Input['DocumentUpdateMethod'] update_method: Update method - when set to 'Replace', the update will replace the existing document; when set to 'NewVersion', the update will create a new version.
        :param pulumi.Input[str] version_name: An optional field specifying the version of the artifact you are creating with the document. This value is unique across all versions of a document, and cannot be changed.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DocumentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The AWS::SSM::Document resource is an SSM document in AWS Systems Manager that defines the actions that Systems Manager performs, which can be used to set up and run commands on your instances.

        :param str resource_name: The name of the resource.
        :param DocumentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DocumentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attachments: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DocumentAttachmentsSourceArgs']]]]] = None,
                 content: Optional[Any] = None,
                 document_format: Optional[pulumi.Input['DocumentFormat']] = None,
                 document_type: Optional[pulumi.Input['DocumentType']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 requires: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DocumentRequiresArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DocumentTagArgs']]]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 update_method: Optional[pulumi.Input['DocumentUpdateMethod']] = None,
                 version_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DocumentArgs.__new__(DocumentArgs)

            __props__.__dict__["attachments"] = attachments
            if content is None and not opts.urn:
                raise TypeError("Missing required property 'content'")
            __props__.__dict__["content"] = content
            __props__.__dict__["document_format"] = document_format
            __props__.__dict__["document_type"] = document_type
            __props__.__dict__["name"] = name
            __props__.__dict__["requires"] = requires
            __props__.__dict__["tags"] = tags
            __props__.__dict__["target_type"] = target_type
            __props__.__dict__["update_method"] = update_method
            __props__.__dict__["version_name"] = version_name
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["document_type", "name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Document, __self__).__init__(
            'aws-native:ssm:Document',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Document':
        """
        Get an existing Document resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DocumentArgs.__new__(DocumentArgs)

        __props__.__dict__["attachments"] = None
        __props__.__dict__["content"] = None
        __props__.__dict__["document_format"] = None
        __props__.__dict__["document_type"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["requires"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["target_type"] = None
        __props__.__dict__["update_method"] = None
        __props__.__dict__["version_name"] = None
        return Document(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def attachments(self) -> pulumi.Output[Optional[Sequence['outputs.DocumentAttachmentsSource']]]:
        """
        A list of key and value pairs that describe attachments to a version of a document.
        """
        return pulumi.get(self, "attachments")

    @property
    @pulumi.getter
    def content(self) -> pulumi.Output[Any]:
        """
        The content for the Systems Manager document in JSON, YAML or String format.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="documentFormat")
    def document_format(self) -> pulumi.Output[Optional['DocumentFormat']]:
        """
        Specify the document format for the request. The document format can be either JSON or YAML. JSON is the default format.
        """
        return pulumi.get(self, "document_format")

    @property
    @pulumi.getter(name="documentType")
    def document_type(self) -> pulumi.Output[Optional['DocumentType']]:
        """
        The type of document to create.
        """
        return pulumi.get(self, "document_type")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        A name for the Systems Manager document.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def requires(self) -> pulumi.Output[Optional[Sequence['outputs.DocumentRequires']]]:
        """
        A list of SSM documents required by a document. For example, an ApplicationConfiguration document requires an ApplicationConfigurationSchema document.
        """
        return pulumi.get(self, "requires")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.DocumentTag']]]:
        """
        Optional metadata that you assign to a resource. Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Output[Optional[str]]:
        """
        Specify a target type to define the kinds of resources the document can run on.
        """
        return pulumi.get(self, "target_type")

    @property
    @pulumi.getter(name="updateMethod")
    def update_method(self) -> pulumi.Output[Optional['DocumentUpdateMethod']]:
        """
        Update method - when set to 'Replace', the update will replace the existing document; when set to 'NewVersion', the update will create a new version.
        """
        return pulumi.get(self, "update_method")

    @property
    @pulumi.getter(name="versionName")
    def version_name(self) -> pulumi.Output[Optional[str]]:
        """
        An optional field specifying the version of the artifact you are creating with the document. This value is unique across all versions of a document, and cannot be changed.
        """
        return pulumi.get(self, "version_name")

