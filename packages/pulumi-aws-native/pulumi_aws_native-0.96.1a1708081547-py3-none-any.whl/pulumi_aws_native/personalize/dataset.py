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

__all__ = ['DatasetArgs', 'Dataset']

@pulumi.input_type
class DatasetArgs:
    def __init__(__self__, *,
                 dataset_group_arn: pulumi.Input[str],
                 dataset_type: pulumi.Input['DatasetType'],
                 schema_arn: pulumi.Input[str],
                 dataset_import_job: Optional[pulumi.Input['DatasetImportJobArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Dataset resource.
        :param pulumi.Input[str] dataset_group_arn: The Amazon Resource Name (ARN) of the dataset group to add the dataset to
        :param pulumi.Input['DatasetType'] dataset_type: The type of dataset
        :param pulumi.Input[str] schema_arn: The ARN of the schema to associate with the dataset. The schema defines the dataset fields.
        :param pulumi.Input[str] name: The name for the dataset
        """
        pulumi.set(__self__, "dataset_group_arn", dataset_group_arn)
        pulumi.set(__self__, "dataset_type", dataset_type)
        pulumi.set(__self__, "schema_arn", schema_arn)
        if dataset_import_job is not None:
            pulumi.set(__self__, "dataset_import_job", dataset_import_job)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="datasetGroupArn")
    def dataset_group_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the dataset group to add the dataset to
        """
        return pulumi.get(self, "dataset_group_arn")

    @dataset_group_arn.setter
    def dataset_group_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "dataset_group_arn", value)

    @property
    @pulumi.getter(name="datasetType")
    def dataset_type(self) -> pulumi.Input['DatasetType']:
        """
        The type of dataset
        """
        return pulumi.get(self, "dataset_type")

    @dataset_type.setter
    def dataset_type(self, value: pulumi.Input['DatasetType']):
        pulumi.set(self, "dataset_type", value)

    @property
    @pulumi.getter(name="schemaArn")
    def schema_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the schema to associate with the dataset. The schema defines the dataset fields.
        """
        return pulumi.get(self, "schema_arn")

    @schema_arn.setter
    def schema_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "schema_arn", value)

    @property
    @pulumi.getter(name="datasetImportJob")
    def dataset_import_job(self) -> Optional[pulumi.Input['DatasetImportJobArgs']]:
        return pulumi.get(self, "dataset_import_job")

    @dataset_import_job.setter
    def dataset_import_job(self, value: Optional[pulumi.Input['DatasetImportJobArgs']]):
        pulumi.set(self, "dataset_import_job", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the dataset
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class Dataset(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dataset_group_arn: Optional[pulumi.Input[str]] = None,
                 dataset_import_job: Optional[pulumi.Input[pulumi.InputType['DatasetImportJobArgs']]] = None,
                 dataset_type: Optional[pulumi.Input['DatasetType']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 schema_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource schema for AWS::Personalize::Dataset.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dataset_group_arn: The Amazon Resource Name (ARN) of the dataset group to add the dataset to
        :param pulumi.Input['DatasetType'] dataset_type: The type of dataset
        :param pulumi.Input[str] name: The name for the dataset
        :param pulumi.Input[str] schema_arn: The ARN of the schema to associate with the dataset. The schema defines the dataset fields.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DatasetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::Personalize::Dataset.

        :param str resource_name: The name of the resource.
        :param DatasetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DatasetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dataset_group_arn: Optional[pulumi.Input[str]] = None,
                 dataset_import_job: Optional[pulumi.Input[pulumi.InputType['DatasetImportJobArgs']]] = None,
                 dataset_type: Optional[pulumi.Input['DatasetType']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 schema_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DatasetArgs.__new__(DatasetArgs)

            if dataset_group_arn is None and not opts.urn:
                raise TypeError("Missing required property 'dataset_group_arn'")
            __props__.__dict__["dataset_group_arn"] = dataset_group_arn
            __props__.__dict__["dataset_import_job"] = dataset_import_job
            if dataset_type is None and not opts.urn:
                raise TypeError("Missing required property 'dataset_type'")
            __props__.__dict__["dataset_type"] = dataset_type
            __props__.__dict__["name"] = name
            if schema_arn is None and not opts.urn:
                raise TypeError("Missing required property 'schema_arn'")
            __props__.__dict__["schema_arn"] = schema_arn
            __props__.__dict__["dataset_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["dataset_group_arn", "dataset_type", "name", "schema_arn"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Dataset, __self__).__init__(
            'aws-native:personalize:Dataset',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Dataset':
        """
        Get an existing Dataset resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DatasetArgs.__new__(DatasetArgs)

        __props__.__dict__["dataset_arn"] = None
        __props__.__dict__["dataset_group_arn"] = None
        __props__.__dict__["dataset_import_job"] = None
        __props__.__dict__["dataset_type"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["schema_arn"] = None
        return Dataset(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="datasetArn")
    def dataset_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the dataset
        """
        return pulumi.get(self, "dataset_arn")

    @property
    @pulumi.getter(name="datasetGroupArn")
    def dataset_group_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the dataset group to add the dataset to
        """
        return pulumi.get(self, "dataset_group_arn")

    @property
    @pulumi.getter(name="datasetImportJob")
    def dataset_import_job(self) -> pulumi.Output[Optional['outputs.DatasetImportJob']]:
        return pulumi.get(self, "dataset_import_job")

    @property
    @pulumi.getter(name="datasetType")
    def dataset_type(self) -> pulumi.Output['DatasetType']:
        """
        The type of dataset
        """
        return pulumi.get(self, "dataset_type")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name for the dataset
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="schemaArn")
    def schema_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the schema to associate with the dataset. The schema defines the dataset fields.
        """
        return pulumi.get(self, "schema_arn")

