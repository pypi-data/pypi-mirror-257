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

__all__ = ['AnomalyMonitorArgs', 'AnomalyMonitor']

@pulumi.input_type
class AnomalyMonitorArgs:
    def __init__(__self__, *,
                 monitor_name: pulumi.Input[str],
                 monitor_type: pulumi.Input['AnomalyMonitorMonitorType'],
                 monitor_dimension: Optional[pulumi.Input['AnomalyMonitorMonitorDimension']] = None,
                 monitor_specification: Optional[pulumi.Input[str]] = None,
                 resource_tags: Optional[pulumi.Input[Sequence[pulumi.Input['AnomalyMonitorResourceTagArgs']]]] = None):
        """
        The set of arguments for constructing a AnomalyMonitor resource.
        :param pulumi.Input[str] monitor_name: The name of the monitor.
        :param pulumi.Input['AnomalyMonitorMonitorDimension'] monitor_dimension: The dimensions to evaluate
        :param pulumi.Input[Sequence[pulumi.Input['AnomalyMonitorResourceTagArgs']]] resource_tags: Tags to assign to monitor.
        """
        pulumi.set(__self__, "monitor_name", monitor_name)
        pulumi.set(__self__, "monitor_type", monitor_type)
        if monitor_dimension is not None:
            pulumi.set(__self__, "monitor_dimension", monitor_dimension)
        if monitor_specification is not None:
            pulumi.set(__self__, "monitor_specification", monitor_specification)
        if resource_tags is not None:
            pulumi.set(__self__, "resource_tags", resource_tags)

    @property
    @pulumi.getter(name="monitorName")
    def monitor_name(self) -> pulumi.Input[str]:
        """
        The name of the monitor.
        """
        return pulumi.get(self, "monitor_name")

    @monitor_name.setter
    def monitor_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "monitor_name", value)

    @property
    @pulumi.getter(name="monitorType")
    def monitor_type(self) -> pulumi.Input['AnomalyMonitorMonitorType']:
        return pulumi.get(self, "monitor_type")

    @monitor_type.setter
    def monitor_type(self, value: pulumi.Input['AnomalyMonitorMonitorType']):
        pulumi.set(self, "monitor_type", value)

    @property
    @pulumi.getter(name="monitorDimension")
    def monitor_dimension(self) -> Optional[pulumi.Input['AnomalyMonitorMonitorDimension']]:
        """
        The dimensions to evaluate
        """
        return pulumi.get(self, "monitor_dimension")

    @monitor_dimension.setter
    def monitor_dimension(self, value: Optional[pulumi.Input['AnomalyMonitorMonitorDimension']]):
        pulumi.set(self, "monitor_dimension", value)

    @property
    @pulumi.getter(name="monitorSpecification")
    def monitor_specification(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "monitor_specification")

    @monitor_specification.setter
    def monitor_specification(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "monitor_specification", value)

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AnomalyMonitorResourceTagArgs']]]]:
        """
        Tags to assign to monitor.
        """
        return pulumi.get(self, "resource_tags")

    @resource_tags.setter
    def resource_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AnomalyMonitorResourceTagArgs']]]]):
        pulumi.set(self, "resource_tags", value)


class AnomalyMonitor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 monitor_dimension: Optional[pulumi.Input['AnomalyMonitorMonitorDimension']] = None,
                 monitor_name: Optional[pulumi.Input[str]] = None,
                 monitor_specification: Optional[pulumi.Input[str]] = None,
                 monitor_type: Optional[pulumi.Input['AnomalyMonitorMonitorType']] = None,
                 resource_tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AnomalyMonitorResourceTagArgs']]]]] = None,
                 __props__=None):
        """
        AWS Cost Anomaly Detection leverages advanced Machine Learning technologies to identify anomalous spend and root causes, so you can quickly take action. You can use Cost Anomaly Detection by creating monitor.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input['AnomalyMonitorMonitorDimension'] monitor_dimension: The dimensions to evaluate
        :param pulumi.Input[str] monitor_name: The name of the monitor.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AnomalyMonitorResourceTagArgs']]]] resource_tags: Tags to assign to monitor.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AnomalyMonitorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        AWS Cost Anomaly Detection leverages advanced Machine Learning technologies to identify anomalous spend and root causes, so you can quickly take action. You can use Cost Anomaly Detection by creating monitor.

        :param str resource_name: The name of the resource.
        :param AnomalyMonitorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AnomalyMonitorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 monitor_dimension: Optional[pulumi.Input['AnomalyMonitorMonitorDimension']] = None,
                 monitor_name: Optional[pulumi.Input[str]] = None,
                 monitor_specification: Optional[pulumi.Input[str]] = None,
                 monitor_type: Optional[pulumi.Input['AnomalyMonitorMonitorType']] = None,
                 resource_tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AnomalyMonitorResourceTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AnomalyMonitorArgs.__new__(AnomalyMonitorArgs)

            __props__.__dict__["monitor_dimension"] = monitor_dimension
            if monitor_name is None and not opts.urn:
                raise TypeError("Missing required property 'monitor_name'")
            __props__.__dict__["monitor_name"] = monitor_name
            __props__.__dict__["monitor_specification"] = monitor_specification
            if monitor_type is None and not opts.urn:
                raise TypeError("Missing required property 'monitor_type'")
            __props__.__dict__["monitor_type"] = monitor_type
            __props__.__dict__["resource_tags"] = resource_tags
            __props__.__dict__["creation_date"] = None
            __props__.__dict__["dimensional_value_count"] = None
            __props__.__dict__["last_evaluated_date"] = None
            __props__.__dict__["last_updated_date"] = None
            __props__.__dict__["monitor_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["monitor_dimension", "monitor_specification", "monitor_type", "resource_tags[*]"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(AnomalyMonitor, __self__).__init__(
            'aws-native:ce:AnomalyMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AnomalyMonitor':
        """
        Get an existing AnomalyMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AnomalyMonitorArgs.__new__(AnomalyMonitorArgs)

        __props__.__dict__["creation_date"] = None
        __props__.__dict__["dimensional_value_count"] = None
        __props__.__dict__["last_evaluated_date"] = None
        __props__.__dict__["last_updated_date"] = None
        __props__.__dict__["monitor_arn"] = None
        __props__.__dict__["monitor_dimension"] = None
        __props__.__dict__["monitor_name"] = None
        __props__.__dict__["monitor_specification"] = None
        __props__.__dict__["monitor_type"] = None
        __props__.__dict__["resource_tags"] = None
        return AnomalyMonitor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        The date when the monitor was created. 
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="dimensionalValueCount")
    def dimensional_value_count(self) -> pulumi.Output[int]:
        """
        The value for evaluated dimensions.
        """
        return pulumi.get(self, "dimensional_value_count")

    @property
    @pulumi.getter(name="lastEvaluatedDate")
    def last_evaluated_date(self) -> pulumi.Output[str]:
        """
        The date when the monitor last evaluated for anomalies.
        """
        return pulumi.get(self, "last_evaluated_date")

    @property
    @pulumi.getter(name="lastUpdatedDate")
    def last_updated_date(self) -> pulumi.Output[str]:
        """
        The date when the monitor was last updated.
        """
        return pulumi.get(self, "last_updated_date")

    @property
    @pulumi.getter(name="monitorArn")
    def monitor_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "monitor_arn")

    @property
    @pulumi.getter(name="monitorDimension")
    def monitor_dimension(self) -> pulumi.Output[Optional['AnomalyMonitorMonitorDimension']]:
        """
        The dimensions to evaluate
        """
        return pulumi.get(self, "monitor_dimension")

    @property
    @pulumi.getter(name="monitorName")
    def monitor_name(self) -> pulumi.Output[str]:
        """
        The name of the monitor.
        """
        return pulumi.get(self, "monitor_name")

    @property
    @pulumi.getter(name="monitorSpecification")
    def monitor_specification(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "monitor_specification")

    @property
    @pulumi.getter(name="monitorType")
    def monitor_type(self) -> pulumi.Output['AnomalyMonitorMonitorType']:
        return pulumi.get(self, "monitor_type")

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> pulumi.Output[Optional[Sequence['outputs.AnomalyMonitorResourceTag']]]:
        """
        Tags to assign to monitor.
        """
        return pulumi.get(self, "resource_tags")

