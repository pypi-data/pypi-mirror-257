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

__all__ = ['ModelArgs', 'Model']

@pulumi.input_type
class ModelArgs:
    def __init__(__self__, *,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input['ModelContainerDefinitionArgs']]]] = None,
                 enable_network_isolation: Optional[pulumi.Input[bool]] = None,
                 execution_role_arn: Optional[pulumi.Input[str]] = None,
                 inference_execution_config: Optional[pulumi.Input['ModelInferenceExecutionConfigArgs']] = None,
                 model_name: Optional[pulumi.Input[str]] = None,
                 primary_container: Optional[pulumi.Input['ModelContainerDefinitionArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['ModelTagArgs']]]] = None,
                 vpc_config: Optional[pulumi.Input['ModelVpcConfigArgs']] = None):
        """
        The set of arguments for constructing a Model resource.
        """
        if containers is not None:
            pulumi.set(__self__, "containers", containers)
        if enable_network_isolation is not None:
            pulumi.set(__self__, "enable_network_isolation", enable_network_isolation)
        if execution_role_arn is not None:
            pulumi.set(__self__, "execution_role_arn", execution_role_arn)
        if inference_execution_config is not None:
            pulumi.set(__self__, "inference_execution_config", inference_execution_config)
        if model_name is not None:
            pulumi.set(__self__, "model_name", model_name)
        if primary_container is not None:
            pulumi.set(__self__, "primary_container", primary_container)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vpc_config is not None:
            pulumi.set(__self__, "vpc_config", vpc_config)

    @property
    @pulumi.getter
    def containers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ModelContainerDefinitionArgs']]]]:
        return pulumi.get(self, "containers")

    @containers.setter
    def containers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ModelContainerDefinitionArgs']]]]):
        pulumi.set(self, "containers", value)

    @property
    @pulumi.getter(name="enableNetworkIsolation")
    def enable_network_isolation(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enable_network_isolation")

    @enable_network_isolation.setter
    def enable_network_isolation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_network_isolation", value)

    @property
    @pulumi.getter(name="executionRoleArn")
    def execution_role_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "execution_role_arn")

    @execution_role_arn.setter
    def execution_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "execution_role_arn", value)

    @property
    @pulumi.getter(name="inferenceExecutionConfig")
    def inference_execution_config(self) -> Optional[pulumi.Input['ModelInferenceExecutionConfigArgs']]:
        return pulumi.get(self, "inference_execution_config")

    @inference_execution_config.setter
    def inference_execution_config(self, value: Optional[pulumi.Input['ModelInferenceExecutionConfigArgs']]):
        pulumi.set(self, "inference_execution_config", value)

    @property
    @pulumi.getter(name="modelName")
    def model_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "model_name")

    @model_name.setter
    def model_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "model_name", value)

    @property
    @pulumi.getter(name="primaryContainer")
    def primary_container(self) -> Optional[pulumi.Input['ModelContainerDefinitionArgs']]:
        return pulumi.get(self, "primary_container")

    @primary_container.setter
    def primary_container(self, value: Optional[pulumi.Input['ModelContainerDefinitionArgs']]):
        pulumi.set(self, "primary_container", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ModelTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ModelTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> Optional[pulumi.Input['ModelVpcConfigArgs']]:
        return pulumi.get(self, "vpc_config")

    @vpc_config.setter
    def vpc_config(self, value: Optional[pulumi.Input['ModelVpcConfigArgs']]):
        pulumi.set(self, "vpc_config", value)


warnings.warn("""Model is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class Model(pulumi.CustomResource):
    warnings.warn("""Model is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ModelContainerDefinitionArgs']]]]] = None,
                 enable_network_isolation: Optional[pulumi.Input[bool]] = None,
                 execution_role_arn: Optional[pulumi.Input[str]] = None,
                 inference_execution_config: Optional[pulumi.Input[pulumi.InputType['ModelInferenceExecutionConfigArgs']]] = None,
                 model_name: Optional[pulumi.Input[str]] = None,
                 primary_container: Optional[pulumi.Input[pulumi.InputType['ModelContainerDefinitionArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ModelTagArgs']]]]] = None,
                 vpc_config: Optional[pulumi.Input[pulumi.InputType['ModelVpcConfigArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::SageMaker::Model

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ModelArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::SageMaker::Model

        :param str resource_name: The name of the resource.
        :param ModelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ModelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ModelContainerDefinitionArgs']]]]] = None,
                 enable_network_isolation: Optional[pulumi.Input[bool]] = None,
                 execution_role_arn: Optional[pulumi.Input[str]] = None,
                 inference_execution_config: Optional[pulumi.Input[pulumi.InputType['ModelInferenceExecutionConfigArgs']]] = None,
                 model_name: Optional[pulumi.Input[str]] = None,
                 primary_container: Optional[pulumi.Input[pulumi.InputType['ModelContainerDefinitionArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ModelTagArgs']]]]] = None,
                 vpc_config: Optional[pulumi.Input[pulumi.InputType['ModelVpcConfigArgs']]] = None,
                 __props__=None):
        pulumi.log.warn("""Model is deprecated: Model is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ModelArgs.__new__(ModelArgs)

            __props__.__dict__["containers"] = containers
            __props__.__dict__["enable_network_isolation"] = enable_network_isolation
            __props__.__dict__["execution_role_arn"] = execution_role_arn
            __props__.__dict__["inference_execution_config"] = inference_execution_config
            __props__.__dict__["model_name"] = model_name
            __props__.__dict__["primary_container"] = primary_container
            __props__.__dict__["tags"] = tags
            __props__.__dict__["vpc_config"] = vpc_config
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["containers[*]", "enable_network_isolation", "execution_role_arn", "inference_execution_config", "model_name", "primary_container", "vpc_config"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Model, __self__).__init__(
            'aws-native:sagemaker:Model',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Model':
        """
        Get an existing Model resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ModelArgs.__new__(ModelArgs)

        __props__.__dict__["containers"] = None
        __props__.__dict__["enable_network_isolation"] = None
        __props__.__dict__["execution_role_arn"] = None
        __props__.__dict__["inference_execution_config"] = None
        __props__.__dict__["model_name"] = None
        __props__.__dict__["primary_container"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["vpc_config"] = None
        return Model(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def containers(self) -> pulumi.Output[Optional[Sequence['outputs.ModelContainerDefinition']]]:
        return pulumi.get(self, "containers")

    @property
    @pulumi.getter(name="enableNetworkIsolation")
    def enable_network_isolation(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "enable_network_isolation")

    @property
    @pulumi.getter(name="executionRoleArn")
    def execution_role_arn(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "execution_role_arn")

    @property
    @pulumi.getter(name="inferenceExecutionConfig")
    def inference_execution_config(self) -> pulumi.Output[Optional['outputs.ModelInferenceExecutionConfig']]:
        return pulumi.get(self, "inference_execution_config")

    @property
    @pulumi.getter(name="modelName")
    def model_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "model_name")

    @property
    @pulumi.getter(name="primaryContainer")
    def primary_container(self) -> pulumi.Output[Optional['outputs.ModelContainerDefinition']]:
        return pulumi.get(self, "primary_container")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.ModelTag']]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> pulumi.Output[Optional['outputs.ModelVpcConfig']]:
        return pulumi.get(self, "vpc_config")

