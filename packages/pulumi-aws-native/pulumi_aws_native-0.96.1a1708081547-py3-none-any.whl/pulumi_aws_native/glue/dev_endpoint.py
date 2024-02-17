# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DevEndpointArgs', 'DevEndpoint']

@pulumi.input_type
class DevEndpointArgs:
    def __init__(__self__, *,
                 role_arn: pulumi.Input[str],
                 arguments: Optional[Any] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 extra_jars_s3_path: Optional[pulumi.Input[str]] = None,
                 extra_python_libs_s3_path: Optional[pulumi.Input[str]] = None,
                 glue_version: Optional[pulumi.Input[str]] = None,
                 number_of_nodes: Optional[pulumi.Input[int]] = None,
                 number_of_workers: Optional[pulumi.Input[int]] = None,
                 public_key: Optional[pulumi.Input[str]] = None,
                 public_keys: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 security_configuration: Optional[pulumi.Input[str]] = None,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 worker_type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DevEndpoint resource.
        """
        pulumi.set(__self__, "role_arn", role_arn)
        if arguments is not None:
            pulumi.set(__self__, "arguments", arguments)
        if endpoint_name is not None:
            pulumi.set(__self__, "endpoint_name", endpoint_name)
        if extra_jars_s3_path is not None:
            pulumi.set(__self__, "extra_jars_s3_path", extra_jars_s3_path)
        if extra_python_libs_s3_path is not None:
            pulumi.set(__self__, "extra_python_libs_s3_path", extra_python_libs_s3_path)
        if glue_version is not None:
            pulumi.set(__self__, "glue_version", glue_version)
        if number_of_nodes is not None:
            pulumi.set(__self__, "number_of_nodes", number_of_nodes)
        if number_of_workers is not None:
            pulumi.set(__self__, "number_of_workers", number_of_workers)
        if public_key is not None:
            pulumi.set(__self__, "public_key", public_key)
        if public_keys is not None:
            pulumi.set(__self__, "public_keys", public_keys)
        if security_configuration is not None:
            pulumi.set(__self__, "security_configuration", security_configuration)
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if worker_type is not None:
            pulumi.set(__self__, "worker_type", worker_type)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter
    def arguments(self) -> Optional[Any]:
        return pulumi.get(self, "arguments")

    @arguments.setter
    def arguments(self, value: Optional[Any]):
        pulumi.set(self, "arguments", value)

    @property
    @pulumi.getter(name="endpointName")
    def endpoint_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "endpoint_name")

    @endpoint_name.setter
    def endpoint_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_name", value)

    @property
    @pulumi.getter(name="extraJarsS3Path")
    def extra_jars_s3_path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "extra_jars_s3_path")

    @extra_jars_s3_path.setter
    def extra_jars_s3_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "extra_jars_s3_path", value)

    @property
    @pulumi.getter(name="extraPythonLibsS3Path")
    def extra_python_libs_s3_path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "extra_python_libs_s3_path")

    @extra_python_libs_s3_path.setter
    def extra_python_libs_s3_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "extra_python_libs_s3_path", value)

    @property
    @pulumi.getter(name="glueVersion")
    def glue_version(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "glue_version")

    @glue_version.setter
    def glue_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "glue_version", value)

    @property
    @pulumi.getter(name="numberOfNodes")
    def number_of_nodes(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "number_of_nodes")

    @number_of_nodes.setter
    def number_of_nodes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "number_of_nodes", value)

    @property
    @pulumi.getter(name="numberOfWorkers")
    def number_of_workers(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "number_of_workers")

    @number_of_workers.setter
    def number_of_workers(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "number_of_workers", value)

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "public_key")

    @public_key.setter
    def public_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_key", value)

    @property
    @pulumi.getter(name="publicKeys")
    def public_keys(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "public_keys")

    @public_keys.setter
    def public_keys(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "public_keys", value)

    @property
    @pulumi.getter(name="securityConfiguration")
    def security_configuration(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "security_configuration")

    @security_configuration.setter
    def security_configuration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_configuration", value)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[Any]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="workerType")
    def worker_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "worker_type")

    @worker_type.setter
    def worker_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "worker_type", value)


warnings.warn("""DevEndpoint is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class DevEndpoint(pulumi.CustomResource):
    warnings.warn("""DevEndpoint is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 arguments: Optional[Any] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 extra_jars_s3_path: Optional[pulumi.Input[str]] = None,
                 extra_python_libs_s3_path: Optional[pulumi.Input[str]] = None,
                 glue_version: Optional[pulumi.Input[str]] = None,
                 number_of_nodes: Optional[pulumi.Input[int]] = None,
                 number_of_workers: Optional[pulumi.Input[int]] = None,
                 public_key: Optional[pulumi.Input[str]] = None,
                 public_keys: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 security_configuration: Optional[pulumi.Input[str]] = None,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 worker_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Glue::DevEndpoint

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DevEndpointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Glue::DevEndpoint

        :param str resource_name: The name of the resource.
        :param DevEndpointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DevEndpointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 arguments: Optional[Any] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 extra_jars_s3_path: Optional[pulumi.Input[str]] = None,
                 extra_python_libs_s3_path: Optional[pulumi.Input[str]] = None,
                 glue_version: Optional[pulumi.Input[str]] = None,
                 number_of_nodes: Optional[pulumi.Input[int]] = None,
                 number_of_workers: Optional[pulumi.Input[int]] = None,
                 public_key: Optional[pulumi.Input[str]] = None,
                 public_keys: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 security_configuration: Optional[pulumi.Input[str]] = None,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 worker_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""DevEndpoint is deprecated: DevEndpoint is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DevEndpointArgs.__new__(DevEndpointArgs)

            __props__.__dict__["arguments"] = arguments
            __props__.__dict__["endpoint_name"] = endpoint_name
            __props__.__dict__["extra_jars_s3_path"] = extra_jars_s3_path
            __props__.__dict__["extra_python_libs_s3_path"] = extra_python_libs_s3_path
            __props__.__dict__["glue_version"] = glue_version
            __props__.__dict__["number_of_nodes"] = number_of_nodes
            __props__.__dict__["number_of_workers"] = number_of_workers
            __props__.__dict__["public_key"] = public_key
            __props__.__dict__["public_keys"] = public_keys
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["security_configuration"] = security_configuration
            __props__.__dict__["security_group_ids"] = security_group_ids
            __props__.__dict__["subnet_id"] = subnet_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["worker_type"] = worker_type
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["endpoint_name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(DevEndpoint, __self__).__init__(
            'aws-native:glue:DevEndpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DevEndpoint':
        """
        Get an existing DevEndpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DevEndpointArgs.__new__(DevEndpointArgs)

        __props__.__dict__["arguments"] = None
        __props__.__dict__["endpoint_name"] = None
        __props__.__dict__["extra_jars_s3_path"] = None
        __props__.__dict__["extra_python_libs_s3_path"] = None
        __props__.__dict__["glue_version"] = None
        __props__.__dict__["number_of_nodes"] = None
        __props__.__dict__["number_of_workers"] = None
        __props__.__dict__["public_key"] = None
        __props__.__dict__["public_keys"] = None
        __props__.__dict__["role_arn"] = None
        __props__.__dict__["security_configuration"] = None
        __props__.__dict__["security_group_ids"] = None
        __props__.__dict__["subnet_id"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["worker_type"] = None
        return DevEndpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arguments(self) -> pulumi.Output[Optional[Any]]:
        return pulumi.get(self, "arguments")

    @property
    @pulumi.getter(name="endpointName")
    def endpoint_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "endpoint_name")

    @property
    @pulumi.getter(name="extraJarsS3Path")
    def extra_jars_s3_path(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "extra_jars_s3_path")

    @property
    @pulumi.getter(name="extraPythonLibsS3Path")
    def extra_python_libs_s3_path(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "extra_python_libs_s3_path")

    @property
    @pulumi.getter(name="glueVersion")
    def glue_version(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "glue_version")

    @property
    @pulumi.getter(name="numberOfNodes")
    def number_of_nodes(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "number_of_nodes")

    @property
    @pulumi.getter(name="numberOfWorkers")
    def number_of_workers(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "number_of_workers")

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "public_key")

    @property
    @pulumi.getter(name="publicKeys")
    def public_keys(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "public_keys")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="securityConfiguration")
    def security_configuration(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "security_configuration")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Any]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="workerType")
    def worker_type(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "worker_type")

