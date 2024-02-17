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

__all__ = ['EndpointConfigArgs', 'EndpointConfig']

@pulumi.input_type
class EndpointConfigArgs:
    def __init__(__self__, *,
                 production_variants: pulumi.Input[Sequence[pulumi.Input['EndpointConfigProductionVariantArgs']]],
                 async_inference_config: Optional[pulumi.Input['EndpointConfigAsyncInferenceConfigArgs']] = None,
                 data_capture_config: Optional[pulumi.Input['EndpointConfigDataCaptureConfigArgs']] = None,
                 enable_network_isolation: Optional[pulumi.Input[bool]] = None,
                 endpoint_config_name: Optional[pulumi.Input[str]] = None,
                 execution_role_arn: Optional[pulumi.Input[str]] = None,
                 explainer_config: Optional[pulumi.Input['EndpointConfigExplainerConfigArgs']] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 shadow_production_variants: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigProductionVariantArgs']]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigTagArgs']]]] = None,
                 vpc_config: Optional[pulumi.Input['EndpointConfigVpcConfigArgs']] = None):
        """
        The set of arguments for constructing a EndpointConfig resource.
        """
        pulumi.set(__self__, "production_variants", production_variants)
        if async_inference_config is not None:
            pulumi.set(__self__, "async_inference_config", async_inference_config)
        if data_capture_config is not None:
            pulumi.set(__self__, "data_capture_config", data_capture_config)
        if enable_network_isolation is not None:
            pulumi.set(__self__, "enable_network_isolation", enable_network_isolation)
        if endpoint_config_name is not None:
            pulumi.set(__self__, "endpoint_config_name", endpoint_config_name)
        if execution_role_arn is not None:
            pulumi.set(__self__, "execution_role_arn", execution_role_arn)
        if explainer_config is not None:
            pulumi.set(__self__, "explainer_config", explainer_config)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if shadow_production_variants is not None:
            pulumi.set(__self__, "shadow_production_variants", shadow_production_variants)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vpc_config is not None:
            pulumi.set(__self__, "vpc_config", vpc_config)

    @property
    @pulumi.getter(name="productionVariants")
    def production_variants(self) -> pulumi.Input[Sequence[pulumi.Input['EndpointConfigProductionVariantArgs']]]:
        return pulumi.get(self, "production_variants")

    @production_variants.setter
    def production_variants(self, value: pulumi.Input[Sequence[pulumi.Input['EndpointConfigProductionVariantArgs']]]):
        pulumi.set(self, "production_variants", value)

    @property
    @pulumi.getter(name="asyncInferenceConfig")
    def async_inference_config(self) -> Optional[pulumi.Input['EndpointConfigAsyncInferenceConfigArgs']]:
        return pulumi.get(self, "async_inference_config")

    @async_inference_config.setter
    def async_inference_config(self, value: Optional[pulumi.Input['EndpointConfigAsyncInferenceConfigArgs']]):
        pulumi.set(self, "async_inference_config", value)

    @property
    @pulumi.getter(name="dataCaptureConfig")
    def data_capture_config(self) -> Optional[pulumi.Input['EndpointConfigDataCaptureConfigArgs']]:
        return pulumi.get(self, "data_capture_config")

    @data_capture_config.setter
    def data_capture_config(self, value: Optional[pulumi.Input['EndpointConfigDataCaptureConfigArgs']]):
        pulumi.set(self, "data_capture_config", value)

    @property
    @pulumi.getter(name="enableNetworkIsolation")
    def enable_network_isolation(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enable_network_isolation")

    @enable_network_isolation.setter
    def enable_network_isolation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_network_isolation", value)

    @property
    @pulumi.getter(name="endpointConfigName")
    def endpoint_config_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "endpoint_config_name")

    @endpoint_config_name.setter
    def endpoint_config_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_config_name", value)

    @property
    @pulumi.getter(name="executionRoleArn")
    def execution_role_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "execution_role_arn")

    @execution_role_arn.setter
    def execution_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "execution_role_arn", value)

    @property
    @pulumi.getter(name="explainerConfig")
    def explainer_config(self) -> Optional[pulumi.Input['EndpointConfigExplainerConfigArgs']]:
        return pulumi.get(self, "explainer_config")

    @explainer_config.setter
    def explainer_config(self, value: Optional[pulumi.Input['EndpointConfigExplainerConfigArgs']]):
        pulumi.set(self, "explainer_config", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter(name="shadowProductionVariants")
    def shadow_production_variants(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigProductionVariantArgs']]]]:
        return pulumi.get(self, "shadow_production_variants")

    @shadow_production_variants.setter
    def shadow_production_variants(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigProductionVariantArgs']]]]):
        pulumi.set(self, "shadow_production_variants", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> Optional[pulumi.Input['EndpointConfigVpcConfigArgs']]:
        return pulumi.get(self, "vpc_config")

    @vpc_config.setter
    def vpc_config(self, value: Optional[pulumi.Input['EndpointConfigVpcConfigArgs']]):
        pulumi.set(self, "vpc_config", value)


warnings.warn("""EndpointConfig is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class EndpointConfig(pulumi.CustomResource):
    warnings.warn("""EndpointConfig is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 async_inference_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigAsyncInferenceConfigArgs']]] = None,
                 data_capture_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigDataCaptureConfigArgs']]] = None,
                 enable_network_isolation: Optional[pulumi.Input[bool]] = None,
                 endpoint_config_name: Optional[pulumi.Input[str]] = None,
                 execution_role_arn: Optional[pulumi.Input[str]] = None,
                 explainer_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigExplainerConfigArgs']]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 production_variants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigProductionVariantArgs']]]]] = None,
                 shadow_production_variants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigProductionVariantArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigTagArgs']]]]] = None,
                 vpc_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigVpcConfigArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::SageMaker::EndpointConfig

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EndpointConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::SageMaker::EndpointConfig

        :param str resource_name: The name of the resource.
        :param EndpointConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EndpointConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 async_inference_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigAsyncInferenceConfigArgs']]] = None,
                 data_capture_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigDataCaptureConfigArgs']]] = None,
                 enable_network_isolation: Optional[pulumi.Input[bool]] = None,
                 endpoint_config_name: Optional[pulumi.Input[str]] = None,
                 execution_role_arn: Optional[pulumi.Input[str]] = None,
                 explainer_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigExplainerConfigArgs']]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 production_variants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigProductionVariantArgs']]]]] = None,
                 shadow_production_variants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigProductionVariantArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigTagArgs']]]]] = None,
                 vpc_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigVpcConfigArgs']]] = None,
                 __props__=None):
        pulumi.log.warn("""EndpointConfig is deprecated: EndpointConfig is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EndpointConfigArgs.__new__(EndpointConfigArgs)

            __props__.__dict__["async_inference_config"] = async_inference_config
            __props__.__dict__["data_capture_config"] = data_capture_config
            __props__.__dict__["enable_network_isolation"] = enable_network_isolation
            __props__.__dict__["endpoint_config_name"] = endpoint_config_name
            __props__.__dict__["execution_role_arn"] = execution_role_arn
            __props__.__dict__["explainer_config"] = explainer_config
            __props__.__dict__["kms_key_id"] = kms_key_id
            if production_variants is None and not opts.urn:
                raise TypeError("Missing required property 'production_variants'")
            __props__.__dict__["production_variants"] = production_variants
            __props__.__dict__["shadow_production_variants"] = shadow_production_variants
            __props__.__dict__["tags"] = tags
            __props__.__dict__["vpc_config"] = vpc_config
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["async_inference_config", "data_capture_config", "enable_network_isolation", "endpoint_config_name", "execution_role_arn", "explainer_config", "kms_key_id", "production_variants[*]", "shadow_production_variants[*]", "vpc_config"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(EndpointConfig, __self__).__init__(
            'aws-native:sagemaker:EndpointConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'EndpointConfig':
        """
        Get an existing EndpointConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EndpointConfigArgs.__new__(EndpointConfigArgs)

        __props__.__dict__["async_inference_config"] = None
        __props__.__dict__["data_capture_config"] = None
        __props__.__dict__["enable_network_isolation"] = None
        __props__.__dict__["endpoint_config_name"] = None
        __props__.__dict__["execution_role_arn"] = None
        __props__.__dict__["explainer_config"] = None
        __props__.__dict__["kms_key_id"] = None
        __props__.__dict__["production_variants"] = None
        __props__.__dict__["shadow_production_variants"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["vpc_config"] = None
        return EndpointConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="asyncInferenceConfig")
    def async_inference_config(self) -> pulumi.Output[Optional['outputs.EndpointConfigAsyncInferenceConfig']]:
        return pulumi.get(self, "async_inference_config")

    @property
    @pulumi.getter(name="dataCaptureConfig")
    def data_capture_config(self) -> pulumi.Output[Optional['outputs.EndpointConfigDataCaptureConfig']]:
        return pulumi.get(self, "data_capture_config")

    @property
    @pulumi.getter(name="enableNetworkIsolation")
    def enable_network_isolation(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "enable_network_isolation")

    @property
    @pulumi.getter(name="endpointConfigName")
    def endpoint_config_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "endpoint_config_name")

    @property
    @pulumi.getter(name="executionRoleArn")
    def execution_role_arn(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "execution_role_arn")

    @property
    @pulumi.getter(name="explainerConfig")
    def explainer_config(self) -> pulumi.Output[Optional['outputs.EndpointConfigExplainerConfig']]:
        return pulumi.get(self, "explainer_config")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="productionVariants")
    def production_variants(self) -> pulumi.Output[Sequence['outputs.EndpointConfigProductionVariant']]:
        return pulumi.get(self, "production_variants")

    @property
    @pulumi.getter(name="shadowProductionVariants")
    def shadow_production_variants(self) -> pulumi.Output[Optional[Sequence['outputs.EndpointConfigProductionVariant']]]:
        return pulumi.get(self, "shadow_production_variants")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.EndpointConfigTag']]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> pulumi.Output[Optional['outputs.EndpointConfigVpcConfig']]:
        return pulumi.get(self, "vpc_config")

