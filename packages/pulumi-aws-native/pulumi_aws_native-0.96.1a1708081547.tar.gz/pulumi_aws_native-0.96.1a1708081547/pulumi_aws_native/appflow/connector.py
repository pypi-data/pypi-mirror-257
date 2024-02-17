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

__all__ = ['ConnectorArgs', 'Connector']

@pulumi.input_type
class ConnectorArgs:
    def __init__(__self__, *,
                 connector_provisioning_config: pulumi.Input['ConnectorProvisioningConfigArgs'],
                 connector_provisioning_type: pulumi.Input[str],
                 connector_label: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Connector resource.
        :param pulumi.Input['ConnectorProvisioningConfigArgs'] connector_provisioning_config: Contains information about the configuration of the connector being registered.
        :param pulumi.Input[str] connector_provisioning_type: The provisioning type of the connector. Currently the only supported value is LAMBDA. 
        :param pulumi.Input[str] connector_label:  The name of the connector. The name is unique for each ConnectorRegistration in your AWS account.
        :param pulumi.Input[str] description: A description about the connector that's being registered.
        """
        pulumi.set(__self__, "connector_provisioning_config", connector_provisioning_config)
        pulumi.set(__self__, "connector_provisioning_type", connector_provisioning_type)
        if connector_label is not None:
            pulumi.set(__self__, "connector_label", connector_label)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="connectorProvisioningConfig")
    def connector_provisioning_config(self) -> pulumi.Input['ConnectorProvisioningConfigArgs']:
        """
        Contains information about the configuration of the connector being registered.
        """
        return pulumi.get(self, "connector_provisioning_config")

    @connector_provisioning_config.setter
    def connector_provisioning_config(self, value: pulumi.Input['ConnectorProvisioningConfigArgs']):
        pulumi.set(self, "connector_provisioning_config", value)

    @property
    @pulumi.getter(name="connectorProvisioningType")
    def connector_provisioning_type(self) -> pulumi.Input[str]:
        """
        The provisioning type of the connector. Currently the only supported value is LAMBDA. 
        """
        return pulumi.get(self, "connector_provisioning_type")

    @connector_provisioning_type.setter
    def connector_provisioning_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "connector_provisioning_type", value)

    @property
    @pulumi.getter(name="connectorLabel")
    def connector_label(self) -> Optional[pulumi.Input[str]]:
        """
         The name of the connector. The name is unique for each ConnectorRegistration in your AWS account.
        """
        return pulumi.get(self, "connector_label")

    @connector_label.setter
    def connector_label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connector_label", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description about the connector that's being registered.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


class Connector(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connector_label: Optional[pulumi.Input[str]] = None,
                 connector_provisioning_config: Optional[pulumi.Input[pulumi.InputType['ConnectorProvisioningConfigArgs']]] = None,
                 connector_provisioning_type: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource schema for AWS::AppFlow::Connector

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connector_label:  The name of the connector. The name is unique for each ConnectorRegistration in your AWS account.
        :param pulumi.Input[pulumi.InputType['ConnectorProvisioningConfigArgs']] connector_provisioning_config: Contains information about the configuration of the connector being registered.
        :param pulumi.Input[str] connector_provisioning_type: The provisioning type of the connector. Currently the only supported value is LAMBDA. 
        :param pulumi.Input[str] description: A description about the connector that's being registered.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConnectorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::AppFlow::Connector

        :param str resource_name: The name of the resource.
        :param ConnectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connector_label: Optional[pulumi.Input[str]] = None,
                 connector_provisioning_config: Optional[pulumi.Input[pulumi.InputType['ConnectorProvisioningConfigArgs']]] = None,
                 connector_provisioning_type: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConnectorArgs.__new__(ConnectorArgs)

            __props__.__dict__["connector_label"] = connector_label
            if connector_provisioning_config is None and not opts.urn:
                raise TypeError("Missing required property 'connector_provisioning_config'")
            __props__.__dict__["connector_provisioning_config"] = connector_provisioning_config
            if connector_provisioning_type is None and not opts.urn:
                raise TypeError("Missing required property 'connector_provisioning_type'")
            __props__.__dict__["connector_provisioning_type"] = connector_provisioning_type
            __props__.__dict__["description"] = description
            __props__.__dict__["connector_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["connector_label"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Connector, __self__).__init__(
            'aws-native:appflow:Connector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Connector':
        """
        Get an existing Connector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConnectorArgs.__new__(ConnectorArgs)

        __props__.__dict__["connector_arn"] = None
        __props__.__dict__["connector_label"] = None
        __props__.__dict__["connector_provisioning_config"] = None
        __props__.__dict__["connector_provisioning_type"] = None
        __props__.__dict__["description"] = None
        return Connector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectorArn")
    def connector_arn(self) -> pulumi.Output[str]:
        """
         The arn of the connector. The arn is unique for each ConnectorRegistration in your AWS account.
        """
        return pulumi.get(self, "connector_arn")

    @property
    @pulumi.getter(name="connectorLabel")
    def connector_label(self) -> pulumi.Output[Optional[str]]:
        """
         The name of the connector. The name is unique for each ConnectorRegistration in your AWS account.
        """
        return pulumi.get(self, "connector_label")

    @property
    @pulumi.getter(name="connectorProvisioningConfig")
    def connector_provisioning_config(self) -> pulumi.Output['outputs.ConnectorProvisioningConfig']:
        """
        Contains information about the configuration of the connector being registered.
        """
        return pulumi.get(self, "connector_provisioning_config")

    @property
    @pulumi.getter(name="connectorProvisioningType")
    def connector_provisioning_type(self) -> pulumi.Output[str]:
        """
        The provisioning type of the connector. Currently the only supported value is LAMBDA. 
        """
        return pulumi.get(self, "connector_provisioning_type")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description about the connector that's being registered.
        """
        return pulumi.get(self, "description")

