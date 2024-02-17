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

__all__ = ['ApplicationSettingsArgs', 'ApplicationSettings']

@pulumi.input_type
class ApplicationSettingsArgs:
    def __init__(__self__, *,
                 application_id: pulumi.Input[str],
                 campaign_hook: Optional[pulumi.Input['ApplicationSettingsCampaignHookArgs']] = None,
                 cloud_watch_metrics_enabled: Optional[pulumi.Input[bool]] = None,
                 limits: Optional[pulumi.Input['ApplicationSettingsLimitsArgs']] = None,
                 quiet_time: Optional[pulumi.Input['ApplicationSettingsQuietTimeArgs']] = None):
        """
        The set of arguments for constructing a ApplicationSettings resource.
        """
        pulumi.set(__self__, "application_id", application_id)
        if campaign_hook is not None:
            pulumi.set(__self__, "campaign_hook", campaign_hook)
        if cloud_watch_metrics_enabled is not None:
            pulumi.set(__self__, "cloud_watch_metrics_enabled", cloud_watch_metrics_enabled)
        if limits is not None:
            pulumi.set(__self__, "limits", limits)
        if quiet_time is not None:
            pulumi.set(__self__, "quiet_time", quiet_time)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_id", value)

    @property
    @pulumi.getter(name="campaignHook")
    def campaign_hook(self) -> Optional[pulumi.Input['ApplicationSettingsCampaignHookArgs']]:
        return pulumi.get(self, "campaign_hook")

    @campaign_hook.setter
    def campaign_hook(self, value: Optional[pulumi.Input['ApplicationSettingsCampaignHookArgs']]):
        pulumi.set(self, "campaign_hook", value)

    @property
    @pulumi.getter(name="cloudWatchMetricsEnabled")
    def cloud_watch_metrics_enabled(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "cloud_watch_metrics_enabled")

    @cloud_watch_metrics_enabled.setter
    def cloud_watch_metrics_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cloud_watch_metrics_enabled", value)

    @property
    @pulumi.getter
    def limits(self) -> Optional[pulumi.Input['ApplicationSettingsLimitsArgs']]:
        return pulumi.get(self, "limits")

    @limits.setter
    def limits(self, value: Optional[pulumi.Input['ApplicationSettingsLimitsArgs']]):
        pulumi.set(self, "limits", value)

    @property
    @pulumi.getter(name="quietTime")
    def quiet_time(self) -> Optional[pulumi.Input['ApplicationSettingsQuietTimeArgs']]:
        return pulumi.get(self, "quiet_time")

    @quiet_time.setter
    def quiet_time(self, value: Optional[pulumi.Input['ApplicationSettingsQuietTimeArgs']]):
        pulumi.set(self, "quiet_time", value)


warnings.warn("""ApplicationSettings is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class ApplicationSettings(pulumi.CustomResource):
    warnings.warn("""ApplicationSettings is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 campaign_hook: Optional[pulumi.Input[pulumi.InputType['ApplicationSettingsCampaignHookArgs']]] = None,
                 cloud_watch_metrics_enabled: Optional[pulumi.Input[bool]] = None,
                 limits: Optional[pulumi.Input[pulumi.InputType['ApplicationSettingsLimitsArgs']]] = None,
                 quiet_time: Optional[pulumi.Input[pulumi.InputType['ApplicationSettingsQuietTimeArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Pinpoint::ApplicationSettings

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplicationSettingsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Pinpoint::ApplicationSettings

        :param str resource_name: The name of the resource.
        :param ApplicationSettingsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationSettingsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 campaign_hook: Optional[pulumi.Input[pulumi.InputType['ApplicationSettingsCampaignHookArgs']]] = None,
                 cloud_watch_metrics_enabled: Optional[pulumi.Input[bool]] = None,
                 limits: Optional[pulumi.Input[pulumi.InputType['ApplicationSettingsLimitsArgs']]] = None,
                 quiet_time: Optional[pulumi.Input[pulumi.InputType['ApplicationSettingsQuietTimeArgs']]] = None,
                 __props__=None):
        pulumi.log.warn("""ApplicationSettings is deprecated: ApplicationSettings is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationSettingsArgs.__new__(ApplicationSettingsArgs)

            if application_id is None and not opts.urn:
                raise TypeError("Missing required property 'application_id'")
            __props__.__dict__["application_id"] = application_id
            __props__.__dict__["campaign_hook"] = campaign_hook
            __props__.__dict__["cloud_watch_metrics_enabled"] = cloud_watch_metrics_enabled
            __props__.__dict__["limits"] = limits
            __props__.__dict__["quiet_time"] = quiet_time
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["application_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ApplicationSettings, __self__).__init__(
            'aws-native:pinpoint:ApplicationSettings',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApplicationSettings':
        """
        Get an existing ApplicationSettings resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApplicationSettingsArgs.__new__(ApplicationSettingsArgs)

        __props__.__dict__["application_id"] = None
        __props__.__dict__["campaign_hook"] = None
        __props__.__dict__["cloud_watch_metrics_enabled"] = None
        __props__.__dict__["limits"] = None
        __props__.__dict__["quiet_time"] = None
        return ApplicationSettings(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter(name="campaignHook")
    def campaign_hook(self) -> pulumi.Output[Optional['outputs.ApplicationSettingsCampaignHook']]:
        return pulumi.get(self, "campaign_hook")

    @property
    @pulumi.getter(name="cloudWatchMetricsEnabled")
    def cloud_watch_metrics_enabled(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "cloud_watch_metrics_enabled")

    @property
    @pulumi.getter
    def limits(self) -> pulumi.Output[Optional['outputs.ApplicationSettingsLimits']]:
        return pulumi.get(self, "limits")

    @property
    @pulumi.getter(name="quietTime")
    def quiet_time(self) -> pulumi.Output[Optional['outputs.ApplicationSettingsQuietTime']]:
        return pulumi.get(self, "quiet_time")

