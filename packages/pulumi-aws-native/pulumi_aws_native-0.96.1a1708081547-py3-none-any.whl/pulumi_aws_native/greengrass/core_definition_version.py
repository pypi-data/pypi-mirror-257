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

__all__ = ['CoreDefinitionVersionInitArgs', 'CoreDefinitionVersion']

@pulumi.input_type
class CoreDefinitionVersionInitArgs:
    def __init__(__self__, *,
                 core_definition_id: pulumi.Input[str],
                 cores: pulumi.Input[Sequence[pulumi.Input['CoreDefinitionVersionCoreArgs']]]):
        """
        The set of arguments for constructing a CoreDefinitionVersion resource.
        """
        pulumi.set(__self__, "core_definition_id", core_definition_id)
        pulumi.set(__self__, "cores", cores)

    @property
    @pulumi.getter(name="coreDefinitionId")
    def core_definition_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "core_definition_id")

    @core_definition_id.setter
    def core_definition_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "core_definition_id", value)

    @property
    @pulumi.getter
    def cores(self) -> pulumi.Input[Sequence[pulumi.Input['CoreDefinitionVersionCoreArgs']]]:
        return pulumi.get(self, "cores")

    @cores.setter
    def cores(self, value: pulumi.Input[Sequence[pulumi.Input['CoreDefinitionVersionCoreArgs']]]):
        pulumi.set(self, "cores", value)


warnings.warn("""CoreDefinitionVersion is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class CoreDefinitionVersion(pulumi.CustomResource):
    warnings.warn("""CoreDefinitionVersion is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 core_definition_id: Optional[pulumi.Input[str]] = None,
                 cores: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CoreDefinitionVersionCoreArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Greengrass::CoreDefinitionVersion

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CoreDefinitionVersionInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Greengrass::CoreDefinitionVersion

        :param str resource_name: The name of the resource.
        :param CoreDefinitionVersionInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CoreDefinitionVersionInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 core_definition_id: Optional[pulumi.Input[str]] = None,
                 cores: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CoreDefinitionVersionCoreArgs']]]]] = None,
                 __props__=None):
        pulumi.log.warn("""CoreDefinitionVersion is deprecated: CoreDefinitionVersion is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CoreDefinitionVersionInitArgs.__new__(CoreDefinitionVersionInitArgs)

            if core_definition_id is None and not opts.urn:
                raise TypeError("Missing required property 'core_definition_id'")
            __props__.__dict__["core_definition_id"] = core_definition_id
            if cores is None and not opts.urn:
                raise TypeError("Missing required property 'cores'")
            __props__.__dict__["cores"] = cores
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["core_definition_id", "cores[*]"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(CoreDefinitionVersion, __self__).__init__(
            'aws-native:greengrass:CoreDefinitionVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'CoreDefinitionVersion':
        """
        Get an existing CoreDefinitionVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CoreDefinitionVersionInitArgs.__new__(CoreDefinitionVersionInitArgs)

        __props__.__dict__["core_definition_id"] = None
        __props__.__dict__["cores"] = None
        return CoreDefinitionVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="coreDefinitionId")
    def core_definition_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "core_definition_id")

    @property
    @pulumi.getter
    def cores(self) -> pulumi.Output[Sequence['outputs.CoreDefinitionVersionCore']]:
        return pulumi.get(self, "cores")

