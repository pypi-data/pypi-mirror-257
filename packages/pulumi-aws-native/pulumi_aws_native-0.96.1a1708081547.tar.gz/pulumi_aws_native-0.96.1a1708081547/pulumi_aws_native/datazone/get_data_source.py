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

__all__ = [
    'GetDataSourceResult',
    'AwaitableGetDataSourceResult',
    'get_data_source',
    'get_data_source_output',
]

@pulumi.output_type
class GetDataSourceResult:
    def __init__(__self__, created_at=None, description=None, domain_id=None, enable_setting=None, environment_id=None, id=None, last_run_asset_count=None, last_run_at=None, last_run_status=None, name=None, project_id=None, publish_on_import=None, recommendation=None, schedule=None, status=None, updated_at=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if domain_id and not isinstance(domain_id, str):
            raise TypeError("Expected argument 'domain_id' to be a str")
        pulumi.set(__self__, "domain_id", domain_id)
        if enable_setting and not isinstance(enable_setting, str):
            raise TypeError("Expected argument 'enable_setting' to be a str")
        pulumi.set(__self__, "enable_setting", enable_setting)
        if environment_id and not isinstance(environment_id, str):
            raise TypeError("Expected argument 'environment_id' to be a str")
        pulumi.set(__self__, "environment_id", environment_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_run_asset_count and not isinstance(last_run_asset_count, float):
            raise TypeError("Expected argument 'last_run_asset_count' to be a float")
        pulumi.set(__self__, "last_run_asset_count", last_run_asset_count)
        if last_run_at and not isinstance(last_run_at, str):
            raise TypeError("Expected argument 'last_run_at' to be a str")
        pulumi.set(__self__, "last_run_at", last_run_at)
        if last_run_status and not isinstance(last_run_status, str):
            raise TypeError("Expected argument 'last_run_status' to be a str")
        pulumi.set(__self__, "last_run_status", last_run_status)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if publish_on_import and not isinstance(publish_on_import, bool):
            raise TypeError("Expected argument 'publish_on_import' to be a bool")
        pulumi.set(__self__, "publish_on_import", publish_on_import)
        if recommendation and not isinstance(recommendation, dict):
            raise TypeError("Expected argument 'recommendation' to be a dict")
        pulumi.set(__self__, "recommendation", recommendation)
        if schedule and not isinstance(schedule, dict):
            raise TypeError("Expected argument 'schedule' to be a dict")
        pulumi.set(__self__, "schedule", schedule)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of when the data source was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the data source.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="domainId")
    def domain_id(self) -> Optional[str]:
        """
        The ID of the Amazon DataZone domain where the data source is created.
        """
        return pulumi.get(self, "domain_id")

    @property
    @pulumi.getter(name="enableSetting")
    def enable_setting(self) -> Optional['DataSourceEnableSetting']:
        """
        Specifies whether the data source is enabled.
        """
        return pulumi.get(self, "enable_setting")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> Optional[str]:
        """
        The unique identifier of the Amazon DataZone environment to which the data source publishes assets.
        """
        return pulumi.get(self, "environment_id")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The unique identifier of the data source.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastRunAssetCount")
    def last_run_asset_count(self) -> Optional[float]:
        """
        The number of assets created by the data source during its last run.
        """
        return pulumi.get(self, "last_run_asset_count")

    @property
    @pulumi.getter(name="lastRunAt")
    def last_run_at(self) -> Optional[str]:
        """
        The timestamp that specifies when the data source was last run.
        """
        return pulumi.get(self, "last_run_at")

    @property
    @pulumi.getter(name="lastRunStatus")
    def last_run_status(self) -> Optional[str]:
        """
        The status of the last run of this data source.
        """
        return pulumi.get(self, "last_run_status")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the data source.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[str]:
        """
        The ID of the Amazon DataZone project to which the data source is added.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="publishOnImport")
    def publish_on_import(self) -> Optional[bool]:
        """
        Specifies whether the assets that this data source creates in the inventory are to be also automatically published to the catalog.
        """
        return pulumi.get(self, "publish_on_import")

    @property
    @pulumi.getter
    def recommendation(self) -> Optional['outputs.DataSourceRecommendationConfiguration']:
        """
        Specifies whether the business name generation is to be enabled for this data source.
        """
        return pulumi.get(self, "recommendation")

    @property
    @pulumi.getter
    def schedule(self) -> Optional['outputs.DataSourceScheduleConfiguration']:
        """
        The schedule of the data source runs.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter
    def status(self) -> Optional['DataSourceStatus']:
        """
        The status of the data source.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[str]:
        """
        The timestamp of when this data source was updated.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetDataSourceResult(GetDataSourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDataSourceResult(
            created_at=self.created_at,
            description=self.description,
            domain_id=self.domain_id,
            enable_setting=self.enable_setting,
            environment_id=self.environment_id,
            id=self.id,
            last_run_asset_count=self.last_run_asset_count,
            last_run_at=self.last_run_at,
            last_run_status=self.last_run_status,
            name=self.name,
            project_id=self.project_id,
            publish_on_import=self.publish_on_import,
            recommendation=self.recommendation,
            schedule=self.schedule,
            status=self.status,
            updated_at=self.updated_at)


def get_data_source(domain_id: Optional[str] = None,
                    id: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDataSourceResult:
    """
    Definition of AWS::DataZone::DataSource Resource Type


    :param str domain_id: The ID of the Amazon DataZone domain where the data source is created.
    :param str id: The unique identifier of the data source.
    """
    __args__ = dict()
    __args__['domainId'] = domain_id
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:datazone:getDataSource', __args__, opts=opts, typ=GetDataSourceResult).value

    return AwaitableGetDataSourceResult(
        created_at=pulumi.get(__ret__, 'created_at'),
        description=pulumi.get(__ret__, 'description'),
        domain_id=pulumi.get(__ret__, 'domain_id'),
        enable_setting=pulumi.get(__ret__, 'enable_setting'),
        environment_id=pulumi.get(__ret__, 'environment_id'),
        id=pulumi.get(__ret__, 'id'),
        last_run_asset_count=pulumi.get(__ret__, 'last_run_asset_count'),
        last_run_at=pulumi.get(__ret__, 'last_run_at'),
        last_run_status=pulumi.get(__ret__, 'last_run_status'),
        name=pulumi.get(__ret__, 'name'),
        project_id=pulumi.get(__ret__, 'project_id'),
        publish_on_import=pulumi.get(__ret__, 'publish_on_import'),
        recommendation=pulumi.get(__ret__, 'recommendation'),
        schedule=pulumi.get(__ret__, 'schedule'),
        status=pulumi.get(__ret__, 'status'),
        updated_at=pulumi.get(__ret__, 'updated_at'))


@_utilities.lift_output_func(get_data_source)
def get_data_source_output(domain_id: Optional[pulumi.Input[str]] = None,
                           id: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDataSourceResult]:
    """
    Definition of AWS::DataZone::DataSource Resource Type


    :param str domain_id: The ID of the Amazon DataZone domain where the data source is created.
    :param str id: The unique identifier of the data source.
    """
    ...
