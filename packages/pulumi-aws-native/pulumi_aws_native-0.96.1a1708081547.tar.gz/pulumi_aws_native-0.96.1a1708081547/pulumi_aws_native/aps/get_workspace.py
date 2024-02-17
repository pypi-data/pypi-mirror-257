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

__all__ = [
    'GetWorkspaceResult',
    'AwaitableGetWorkspaceResult',
    'get_workspace',
    'get_workspace_output',
]

@pulumi.output_type
class GetWorkspaceResult:
    def __init__(__self__, alert_manager_definition=None, alias=None, arn=None, logging_configuration=None, prometheus_endpoint=None, tags=None, workspace_id=None):
        if alert_manager_definition and not isinstance(alert_manager_definition, str):
            raise TypeError("Expected argument 'alert_manager_definition' to be a str")
        pulumi.set(__self__, "alert_manager_definition", alert_manager_definition)
        if alias and not isinstance(alias, str):
            raise TypeError("Expected argument 'alias' to be a str")
        pulumi.set(__self__, "alias", alias)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if logging_configuration and not isinstance(logging_configuration, dict):
            raise TypeError("Expected argument 'logging_configuration' to be a dict")
        pulumi.set(__self__, "logging_configuration", logging_configuration)
        if prometheus_endpoint and not isinstance(prometheus_endpoint, str):
            raise TypeError("Expected argument 'prometheus_endpoint' to be a str")
        pulumi.set(__self__, "prometheus_endpoint", prometheus_endpoint)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if workspace_id and not isinstance(workspace_id, str):
            raise TypeError("Expected argument 'workspace_id' to be a str")
        pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="alertManagerDefinition")
    def alert_manager_definition(self) -> Optional[str]:
        """
        The AMP Workspace alert manager definition data
        """
        return pulumi.get(self, "alert_manager_definition")

    @property
    @pulumi.getter
    def alias(self) -> Optional[str]:
        """
        AMP Workspace alias.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Workspace arn.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="loggingConfiguration")
    def logging_configuration(self) -> Optional['outputs.WorkspaceLoggingConfiguration']:
        return pulumi.get(self, "logging_configuration")

    @property
    @pulumi.getter(name="prometheusEndpoint")
    def prometheus_endpoint(self) -> Optional[str]:
        """
        AMP Workspace prometheus endpoint
        """
        return pulumi.get(self, "prometheus_endpoint")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.WorkspaceTag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> Optional[str]:
        """
        Required to identify a specific APS Workspace.
        """
        return pulumi.get(self, "workspace_id")


class AwaitableGetWorkspaceResult(GetWorkspaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkspaceResult(
            alert_manager_definition=self.alert_manager_definition,
            alias=self.alias,
            arn=self.arn,
            logging_configuration=self.logging_configuration,
            prometheus_endpoint=self.prometheus_endpoint,
            tags=self.tags,
            workspace_id=self.workspace_id)


def get_workspace(arn: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkspaceResult:
    """
    Resource Type definition for AWS::APS::Workspace


    :param str arn: Workspace arn.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:aps:getWorkspace', __args__, opts=opts, typ=GetWorkspaceResult).value

    return AwaitableGetWorkspaceResult(
        alert_manager_definition=pulumi.get(__ret__, 'alert_manager_definition'),
        alias=pulumi.get(__ret__, 'alias'),
        arn=pulumi.get(__ret__, 'arn'),
        logging_configuration=pulumi.get(__ret__, 'logging_configuration'),
        prometheus_endpoint=pulumi.get(__ret__, 'prometheus_endpoint'),
        tags=pulumi.get(__ret__, 'tags'),
        workspace_id=pulumi.get(__ret__, 'workspace_id'))


@_utilities.lift_output_func(get_workspace)
def get_workspace_output(arn: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWorkspaceResult]:
    """
    Resource Type definition for AWS::APS::Workspace


    :param str arn: Workspace arn.
    """
    ...
