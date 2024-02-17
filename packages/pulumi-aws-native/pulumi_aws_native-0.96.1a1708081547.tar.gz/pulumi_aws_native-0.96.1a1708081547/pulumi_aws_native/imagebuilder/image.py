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

__all__ = ['ImageArgs', 'Image']

@pulumi.input_type
class ImageArgs:
    def __init__(__self__, *,
                 container_recipe_arn: Optional[pulumi.Input[str]] = None,
                 distribution_configuration_arn: Optional[pulumi.Input[str]] = None,
                 enhanced_image_metadata_enabled: Optional[pulumi.Input[bool]] = None,
                 execution_role: Optional[pulumi.Input[str]] = None,
                 image_recipe_arn: Optional[pulumi.Input[str]] = None,
                 image_scanning_configuration: Optional[pulumi.Input['ImageScanningConfigurationArgs']] = None,
                 image_tests_configuration: Optional[pulumi.Input['ImageTestsConfigurationArgs']] = None,
                 infrastructure_configuration_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workflows: Optional[pulumi.Input[Sequence[pulumi.Input['ImageWorkflowConfigurationArgs']]]] = None):
        """
        The set of arguments for constructing a Image resource.
        :param pulumi.Input[str] container_recipe_arn: The Amazon Resource Name (ARN) of the container recipe that defines how images are configured and tested.
        :param pulumi.Input[str] distribution_configuration_arn: The Amazon Resource Name (ARN) of the distribution configuration.
        :param pulumi.Input[bool] enhanced_image_metadata_enabled: Collects additional information about the image being created, including the operating system (OS) version and package list.
        :param pulumi.Input[str] execution_role: The execution role name/ARN for the image build, if provided
        :param pulumi.Input[str] image_recipe_arn: The Amazon Resource Name (ARN) of the image recipe that defines how images are configured, tested, and assessed.
        :param pulumi.Input['ImageScanningConfigurationArgs'] image_scanning_configuration: Contains settings for vulnerability scans.
        :param pulumi.Input['ImageTestsConfigurationArgs'] image_tests_configuration: The image tests configuration used when creating this image.
        :param pulumi.Input[str] infrastructure_configuration_arn: The Amazon Resource Name (ARN) of the infrastructure configuration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags associated with the image.
        :param pulumi.Input[Sequence[pulumi.Input['ImageWorkflowConfigurationArgs']]] workflows: Workflows to define the image build process
        """
        if container_recipe_arn is not None:
            pulumi.set(__self__, "container_recipe_arn", container_recipe_arn)
        if distribution_configuration_arn is not None:
            pulumi.set(__self__, "distribution_configuration_arn", distribution_configuration_arn)
        if enhanced_image_metadata_enabled is not None:
            pulumi.set(__self__, "enhanced_image_metadata_enabled", enhanced_image_metadata_enabled)
        if execution_role is not None:
            pulumi.set(__self__, "execution_role", execution_role)
        if image_recipe_arn is not None:
            pulumi.set(__self__, "image_recipe_arn", image_recipe_arn)
        if image_scanning_configuration is not None:
            pulumi.set(__self__, "image_scanning_configuration", image_scanning_configuration)
        if image_tests_configuration is not None:
            pulumi.set(__self__, "image_tests_configuration", image_tests_configuration)
        if infrastructure_configuration_arn is not None:
            pulumi.set(__self__, "infrastructure_configuration_arn", infrastructure_configuration_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if workflows is not None:
            pulumi.set(__self__, "workflows", workflows)

    @property
    @pulumi.getter(name="containerRecipeArn")
    def container_recipe_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the container recipe that defines how images are configured and tested.
        """
        return pulumi.get(self, "container_recipe_arn")

    @container_recipe_arn.setter
    def container_recipe_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "container_recipe_arn", value)

    @property
    @pulumi.getter(name="distributionConfigurationArn")
    def distribution_configuration_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the distribution configuration.
        """
        return pulumi.get(self, "distribution_configuration_arn")

    @distribution_configuration_arn.setter
    def distribution_configuration_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "distribution_configuration_arn", value)

    @property
    @pulumi.getter(name="enhancedImageMetadataEnabled")
    def enhanced_image_metadata_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Collects additional information about the image being created, including the operating system (OS) version and package list.
        """
        return pulumi.get(self, "enhanced_image_metadata_enabled")

    @enhanced_image_metadata_enabled.setter
    def enhanced_image_metadata_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enhanced_image_metadata_enabled", value)

    @property
    @pulumi.getter(name="executionRole")
    def execution_role(self) -> Optional[pulumi.Input[str]]:
        """
        The execution role name/ARN for the image build, if provided
        """
        return pulumi.get(self, "execution_role")

    @execution_role.setter
    def execution_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "execution_role", value)

    @property
    @pulumi.getter(name="imageRecipeArn")
    def image_recipe_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the image recipe that defines how images are configured, tested, and assessed.
        """
        return pulumi.get(self, "image_recipe_arn")

    @image_recipe_arn.setter
    def image_recipe_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "image_recipe_arn", value)

    @property
    @pulumi.getter(name="imageScanningConfiguration")
    def image_scanning_configuration(self) -> Optional[pulumi.Input['ImageScanningConfigurationArgs']]:
        """
        Contains settings for vulnerability scans.
        """
        return pulumi.get(self, "image_scanning_configuration")

    @image_scanning_configuration.setter
    def image_scanning_configuration(self, value: Optional[pulumi.Input['ImageScanningConfigurationArgs']]):
        pulumi.set(self, "image_scanning_configuration", value)

    @property
    @pulumi.getter(name="imageTestsConfiguration")
    def image_tests_configuration(self) -> Optional[pulumi.Input['ImageTestsConfigurationArgs']]:
        """
        The image tests configuration used when creating this image.
        """
        return pulumi.get(self, "image_tests_configuration")

    @image_tests_configuration.setter
    def image_tests_configuration(self, value: Optional[pulumi.Input['ImageTestsConfigurationArgs']]):
        pulumi.set(self, "image_tests_configuration", value)

    @property
    @pulumi.getter(name="infrastructureConfigurationArn")
    def infrastructure_configuration_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the infrastructure configuration.
        """
        return pulumi.get(self, "infrastructure_configuration_arn")

    @infrastructure_configuration_arn.setter
    def infrastructure_configuration_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "infrastructure_configuration_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags associated with the image.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def workflows(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ImageWorkflowConfigurationArgs']]]]:
        """
        Workflows to define the image build process
        """
        return pulumi.get(self, "workflows")

    @workflows.setter
    def workflows(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ImageWorkflowConfigurationArgs']]]]):
        pulumi.set(self, "workflows", value)


class Image(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_recipe_arn: Optional[pulumi.Input[str]] = None,
                 distribution_configuration_arn: Optional[pulumi.Input[str]] = None,
                 enhanced_image_metadata_enabled: Optional[pulumi.Input[bool]] = None,
                 execution_role: Optional[pulumi.Input[str]] = None,
                 image_recipe_arn: Optional[pulumi.Input[str]] = None,
                 image_scanning_configuration: Optional[pulumi.Input[pulumi.InputType['ImageScanningConfigurationArgs']]] = None,
                 image_tests_configuration: Optional[pulumi.Input[pulumi.InputType['ImageTestsConfigurationArgs']]] = None,
                 infrastructure_configuration_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workflows: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageWorkflowConfigurationArgs']]]]] = None,
                 __props__=None):
        """
        Resource schema for AWS::ImageBuilder::Image

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] container_recipe_arn: The Amazon Resource Name (ARN) of the container recipe that defines how images are configured and tested.
        :param pulumi.Input[str] distribution_configuration_arn: The Amazon Resource Name (ARN) of the distribution configuration.
        :param pulumi.Input[bool] enhanced_image_metadata_enabled: Collects additional information about the image being created, including the operating system (OS) version and package list.
        :param pulumi.Input[str] execution_role: The execution role name/ARN for the image build, if provided
        :param pulumi.Input[str] image_recipe_arn: The Amazon Resource Name (ARN) of the image recipe that defines how images are configured, tested, and assessed.
        :param pulumi.Input[pulumi.InputType['ImageScanningConfigurationArgs']] image_scanning_configuration: Contains settings for vulnerability scans.
        :param pulumi.Input[pulumi.InputType['ImageTestsConfigurationArgs']] image_tests_configuration: The image tests configuration used when creating this image.
        :param pulumi.Input[str] infrastructure_configuration_arn: The Amazon Resource Name (ARN) of the infrastructure configuration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags associated with the image.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageWorkflowConfigurationArgs']]]] workflows: Workflows to define the image build process
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ImageArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::ImageBuilder::Image

        :param str resource_name: The name of the resource.
        :param ImageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ImageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_recipe_arn: Optional[pulumi.Input[str]] = None,
                 distribution_configuration_arn: Optional[pulumi.Input[str]] = None,
                 enhanced_image_metadata_enabled: Optional[pulumi.Input[bool]] = None,
                 execution_role: Optional[pulumi.Input[str]] = None,
                 image_recipe_arn: Optional[pulumi.Input[str]] = None,
                 image_scanning_configuration: Optional[pulumi.Input[pulumi.InputType['ImageScanningConfigurationArgs']]] = None,
                 image_tests_configuration: Optional[pulumi.Input[pulumi.InputType['ImageTestsConfigurationArgs']]] = None,
                 infrastructure_configuration_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workflows: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageWorkflowConfigurationArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ImageArgs.__new__(ImageArgs)

            __props__.__dict__["container_recipe_arn"] = container_recipe_arn
            __props__.__dict__["distribution_configuration_arn"] = distribution_configuration_arn
            __props__.__dict__["enhanced_image_metadata_enabled"] = enhanced_image_metadata_enabled
            __props__.__dict__["execution_role"] = execution_role
            __props__.__dict__["image_recipe_arn"] = image_recipe_arn
            __props__.__dict__["image_scanning_configuration"] = image_scanning_configuration
            __props__.__dict__["image_tests_configuration"] = image_tests_configuration
            __props__.__dict__["infrastructure_configuration_arn"] = infrastructure_configuration_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["workflows"] = workflows
            __props__.__dict__["arn"] = None
            __props__.__dict__["image_id"] = None
            __props__.__dict__["image_uri"] = None
            __props__.__dict__["name"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["container_recipe_arn", "distribution_configuration_arn", "enhanced_image_metadata_enabled", "image_recipe_arn", "image_scanning_configuration", "image_tests_configuration", "infrastructure_configuration_arn", "tags.*", "workflows[*]"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Image, __self__).__init__(
            'aws-native:imagebuilder:Image',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Image':
        """
        Get an existing Image resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ImageArgs.__new__(ImageArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["container_recipe_arn"] = None
        __props__.__dict__["distribution_configuration_arn"] = None
        __props__.__dict__["enhanced_image_metadata_enabled"] = None
        __props__.__dict__["execution_role"] = None
        __props__.__dict__["image_id"] = None
        __props__.__dict__["image_recipe_arn"] = None
        __props__.__dict__["image_scanning_configuration"] = None
        __props__.__dict__["image_tests_configuration"] = None
        __props__.__dict__["image_uri"] = None
        __props__.__dict__["infrastructure_configuration_arn"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["workflows"] = None
        return Image(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the image.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="containerRecipeArn")
    def container_recipe_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the container recipe that defines how images are configured and tested.
        """
        return pulumi.get(self, "container_recipe_arn")

    @property
    @pulumi.getter(name="distributionConfigurationArn")
    def distribution_configuration_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the distribution configuration.
        """
        return pulumi.get(self, "distribution_configuration_arn")

    @property
    @pulumi.getter(name="enhancedImageMetadataEnabled")
    def enhanced_image_metadata_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Collects additional information about the image being created, including the operating system (OS) version and package list.
        """
        return pulumi.get(self, "enhanced_image_metadata_enabled")

    @property
    @pulumi.getter(name="executionRole")
    def execution_role(self) -> pulumi.Output[Optional[str]]:
        """
        The execution role name/ARN for the image build, if provided
        """
        return pulumi.get(self, "execution_role")

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> pulumi.Output[str]:
        """
        The AMI ID of the EC2 AMI in current region.
        """
        return pulumi.get(self, "image_id")

    @property
    @pulumi.getter(name="imageRecipeArn")
    def image_recipe_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the image recipe that defines how images are configured, tested, and assessed.
        """
        return pulumi.get(self, "image_recipe_arn")

    @property
    @pulumi.getter(name="imageScanningConfiguration")
    def image_scanning_configuration(self) -> pulumi.Output[Optional['outputs.ImageScanningConfiguration']]:
        """
        Contains settings for vulnerability scans.
        """
        return pulumi.get(self, "image_scanning_configuration")

    @property
    @pulumi.getter(name="imageTestsConfiguration")
    def image_tests_configuration(self) -> pulumi.Output[Optional['outputs.ImageTestsConfiguration']]:
        """
        The image tests configuration used when creating this image.
        """
        return pulumi.get(self, "image_tests_configuration")

    @property
    @pulumi.getter(name="imageUri")
    def image_uri(self) -> pulumi.Output[str]:
        """
        URI for containers created in current Region with default ECR image tag
        """
        return pulumi.get(self, "image_uri")

    @property
    @pulumi.getter(name="infrastructureConfigurationArn")
    def infrastructure_configuration_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the infrastructure configuration.
        """
        return pulumi.get(self, "infrastructure_configuration_arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the image.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags associated with the image.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def workflows(self) -> pulumi.Output[Optional[Sequence['outputs.ImageWorkflowConfiguration']]]:
        """
        Workflows to define the image build process
        """
        return pulumi.get(self, "workflows")

