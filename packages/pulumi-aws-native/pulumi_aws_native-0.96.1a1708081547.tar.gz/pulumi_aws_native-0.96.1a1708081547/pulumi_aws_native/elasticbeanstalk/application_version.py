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

__all__ = ['ApplicationVersionArgs', 'ApplicationVersion']

@pulumi.input_type
class ApplicationVersionArgs:
    def __init__(__self__, *,
                 application_name: pulumi.Input[str],
                 source_bundle: pulumi.Input['ApplicationVersionSourceBundleArgs'],
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ApplicationVersion resource.
        :param pulumi.Input[str] application_name: The name of the Elastic Beanstalk application that is associated with this application version. 
        :param pulumi.Input['ApplicationVersionSourceBundleArgs'] source_bundle: The Amazon S3 bucket and key that identify the location of the source bundle for this version. 
        :param pulumi.Input[str] description: A description of this application version.
        """
        pulumi.set(__self__, "application_name", application_name)
        pulumi.set(__self__, "source_bundle", source_bundle)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="applicationName")
    def application_name(self) -> pulumi.Input[str]:
        """
        The name of the Elastic Beanstalk application that is associated with this application version. 
        """
        return pulumi.get(self, "application_name")

    @application_name.setter
    def application_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_name", value)

    @property
    @pulumi.getter(name="sourceBundle")
    def source_bundle(self) -> pulumi.Input['ApplicationVersionSourceBundleArgs']:
        """
        The Amazon S3 bucket and key that identify the location of the source bundle for this version. 
        """
        return pulumi.get(self, "source_bundle")

    @source_bundle.setter
    def source_bundle(self, value: pulumi.Input['ApplicationVersionSourceBundleArgs']):
        pulumi.set(self, "source_bundle", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this application version.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


class ApplicationVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 source_bundle: Optional[pulumi.Input[pulumi.InputType['ApplicationVersionSourceBundleArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::ElasticBeanstalk::ApplicationVersion

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_name: The name of the Elastic Beanstalk application that is associated with this application version. 
        :param pulumi.Input[str] description: A description of this application version.
        :param pulumi.Input[pulumi.InputType['ApplicationVersionSourceBundleArgs']] source_bundle: The Amazon S3 bucket and key that identify the location of the source bundle for this version. 
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplicationVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::ElasticBeanstalk::ApplicationVersion

        :param str resource_name: The name of the resource.
        :param ApplicationVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 source_bundle: Optional[pulumi.Input[pulumi.InputType['ApplicationVersionSourceBundleArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationVersionArgs.__new__(ApplicationVersionArgs)

            if application_name is None and not opts.urn:
                raise TypeError("Missing required property 'application_name'")
            __props__.__dict__["application_name"] = application_name
            __props__.__dict__["description"] = description
            if source_bundle is None and not opts.urn:
                raise TypeError("Missing required property 'source_bundle'")
            __props__.__dict__["source_bundle"] = source_bundle
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["application_name", "source_bundle"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ApplicationVersion, __self__).__init__(
            'aws-native:elasticbeanstalk:ApplicationVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApplicationVersion':
        """
        Get an existing ApplicationVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApplicationVersionArgs.__new__(ApplicationVersionArgs)

        __props__.__dict__["application_name"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["source_bundle"] = None
        return ApplicationVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationName")
    def application_name(self) -> pulumi.Output[str]:
        """
        The name of the Elastic Beanstalk application that is associated with this application version. 
        """
        return pulumi.get(self, "application_name")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of this application version.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="sourceBundle")
    def source_bundle(self) -> pulumi.Output['outputs.ApplicationVersionSourceBundle']:
        """
        The Amazon S3 bucket and key that identify the location of the source bundle for this version. 
        """
        return pulumi.get(self, "source_bundle")

