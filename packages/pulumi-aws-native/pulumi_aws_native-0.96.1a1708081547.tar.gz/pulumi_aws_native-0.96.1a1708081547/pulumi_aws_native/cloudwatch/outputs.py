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
    'AlarmDimension',
    'AlarmMetric',
    'AlarmMetricDataQuery',
    'AlarmMetricStat',
    'AnomalyDetectorConfiguration',
    'AnomalyDetectorDimension',
    'AnomalyDetectorMetric',
    'AnomalyDetectorMetricDataQuery',
    'AnomalyDetectorMetricMathAnomalyDetector',
    'AnomalyDetectorMetricStat',
    'AnomalyDetectorRange',
    'AnomalyDetectorSingleMetricAnomalyDetector',
    'InsightRuleTags',
    'MetricStreamFilter',
    'MetricStreamStatisticsConfiguration',
    'MetricStreamStatisticsMetric',
    'MetricStreamTag',
]

@pulumi.output_type
class AlarmDimension(dict):
    """
    Dimensions are arbitrary name/value pairs that can be associated with a CloudWatch metric.
    """
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        Dimensions are arbitrary name/value pairs that can be associated with a CloudWatch metric.
        :param str name: The name of the dimension.
        :param str value: The value for the dimension.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the dimension.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the dimension.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class AlarmMetric(dict):
    """
    The Metric property type represents a specific metric.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricName":
            suggest = "metric_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AlarmMetric. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AlarmMetric.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AlarmMetric.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 dimensions: Optional[Sequence['outputs.AlarmDimension']] = None,
                 metric_name: Optional[str] = None,
                 namespace: Optional[str] = None):
        """
        The Metric property type represents a specific metric.
        :param Sequence['AlarmDimension'] dimensions: The dimensions for the metric.
        :param str metric_name: The name of the metric.
        :param str namespace: The namespace of the metric.
        """
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)
        if metric_name is not None:
            pulumi.set(__self__, "metric_name", metric_name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[Sequence['outputs.AlarmDimension']]:
        """
        The dimensions for the metric.
        """
        return pulumi.get(self, "dimensions")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> Optional[str]:
        """
        The name of the metric.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        """
        The namespace of the metric.
        """
        return pulumi.get(self, "namespace")


@pulumi.output_type
class AlarmMetricDataQuery(dict):
    """
    This property type specifies the metric data to return, and whether this call is just retrieving a batch set of data for one metric, or is performing a math expression on metric data.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accountId":
            suggest = "account_id"
        elif key == "metricStat":
            suggest = "metric_stat"
        elif key == "returnData":
            suggest = "return_data"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AlarmMetricDataQuery. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AlarmMetricDataQuery.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AlarmMetricDataQuery.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 account_id: Optional[str] = None,
                 expression: Optional[str] = None,
                 label: Optional[str] = None,
                 metric_stat: Optional['outputs.AlarmMetricStat'] = None,
                 period: Optional[int] = None,
                 return_data: Optional[bool] = None):
        """
        This property type specifies the metric data to return, and whether this call is just retrieving a batch set of data for one metric, or is performing a math expression on metric data.
        :param str id: A short name used to tie this object to the results in the response.
        :param str account_id: The ID of the account where the metrics are located, if this is a cross-account alarm.
        :param str expression: The math expression to be performed on the returned data.
        :param str label: A human-readable label for this metric or expression.
        :param 'AlarmMetricStat' metric_stat: The metric to be returned, along with statistics, period, and units.
        :param int period: The period in seconds, over which the statistic is applied.
        :param bool return_data: This option indicates whether to return the timestamps and raw data values of this metric.
        """
        pulumi.set(__self__, "id", id)
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if expression is not None:
            pulumi.set(__self__, "expression", expression)
        if label is not None:
            pulumi.set(__self__, "label", label)
        if metric_stat is not None:
            pulumi.set(__self__, "metric_stat", metric_stat)
        if period is not None:
            pulumi.set(__self__, "period", period)
        if return_data is not None:
            pulumi.set(__self__, "return_data", return_data)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        A short name used to tie this object to the results in the response.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[str]:
        """
        The ID of the account where the metrics are located, if this is a cross-account alarm.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def expression(self) -> Optional[str]:
        """
        The math expression to be performed on the returned data.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def label(self) -> Optional[str]:
        """
        A human-readable label for this metric or expression.
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter(name="metricStat")
    def metric_stat(self) -> Optional['outputs.AlarmMetricStat']:
        """
        The metric to be returned, along with statistics, period, and units.
        """
        return pulumi.get(self, "metric_stat")

    @property
    @pulumi.getter
    def period(self) -> Optional[int]:
        """
        The period in seconds, over which the statistic is applied.
        """
        return pulumi.get(self, "period")

    @property
    @pulumi.getter(name="returnData")
    def return_data(self) -> Optional[bool]:
        """
        This option indicates whether to return the timestamps and raw data values of this metric.
        """
        return pulumi.get(self, "return_data")


@pulumi.output_type
class AlarmMetricStat(dict):
    """
    This structure defines the metric to be returned, along with the statistics, period, and units.
    """
    def __init__(__self__, *,
                 metric: 'outputs.AlarmMetric',
                 period: int,
                 stat: str,
                 unit: Optional[str] = None):
        """
        This structure defines the metric to be returned, along with the statistics, period, and units.
        :param 'AlarmMetric' metric: The metric to return, including the metric name, namespace, and dimensions.
        :param int period: The granularity, in seconds, of the returned data points.
        :param str stat: The statistic to return.
        :param str unit: The unit to use for the returned data points.
        """
        pulumi.set(__self__, "metric", metric)
        pulumi.set(__self__, "period", period)
        pulumi.set(__self__, "stat", stat)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter
    def metric(self) -> 'outputs.AlarmMetric':
        """
        The metric to return, including the metric name, namespace, and dimensions.
        """
        return pulumi.get(self, "metric")

    @property
    @pulumi.getter
    def period(self) -> int:
        """
        The granularity, in seconds, of the returned data points.
        """
        return pulumi.get(self, "period")

    @property
    @pulumi.getter
    def stat(self) -> str:
        """
        The statistic to return.
        """
        return pulumi.get(self, "stat")

    @property
    @pulumi.getter
    def unit(self) -> Optional[str]:
        """
        The unit to use for the returned data points.
        """
        return pulumi.get(self, "unit")


@pulumi.output_type
class AnomalyDetectorConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "excludedTimeRanges":
            suggest = "excluded_time_ranges"
        elif key == "metricTimeZone":
            suggest = "metric_time_zone"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AnomalyDetectorConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AnomalyDetectorConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AnomalyDetectorConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 excluded_time_ranges: Optional[Sequence['outputs.AnomalyDetectorRange']] = None,
                 metric_time_zone: Optional[str] = None):
        if excluded_time_ranges is not None:
            pulumi.set(__self__, "excluded_time_ranges", excluded_time_ranges)
        if metric_time_zone is not None:
            pulumi.set(__self__, "metric_time_zone", metric_time_zone)

    @property
    @pulumi.getter(name="excludedTimeRanges")
    def excluded_time_ranges(self) -> Optional[Sequence['outputs.AnomalyDetectorRange']]:
        return pulumi.get(self, "excluded_time_ranges")

    @property
    @pulumi.getter(name="metricTimeZone")
    def metric_time_zone(self) -> Optional[str]:
        return pulumi.get(self, "metric_time_zone")


@pulumi.output_type
class AnomalyDetectorDimension(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class AnomalyDetectorMetric(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricName":
            suggest = "metric_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AnomalyDetectorMetric. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AnomalyDetectorMetric.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AnomalyDetectorMetric.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 metric_name: str,
                 namespace: str,
                 dimensions: Optional[Sequence['outputs.AnomalyDetectorDimension']] = None):
        pulumi.set(__self__, "metric_name", metric_name)
        pulumi.set(__self__, "namespace", namespace)
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> str:
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def namespace(self) -> str:
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[Sequence['outputs.AnomalyDetectorDimension']]:
        return pulumi.get(self, "dimensions")


@pulumi.output_type
class AnomalyDetectorMetricDataQuery(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accountId":
            suggest = "account_id"
        elif key == "metricStat":
            suggest = "metric_stat"
        elif key == "returnData":
            suggest = "return_data"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AnomalyDetectorMetricDataQuery. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AnomalyDetectorMetricDataQuery.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AnomalyDetectorMetricDataQuery.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 account_id: Optional[str] = None,
                 expression: Optional[str] = None,
                 label: Optional[str] = None,
                 metric_stat: Optional['outputs.AnomalyDetectorMetricStat'] = None,
                 period: Optional[int] = None,
                 return_data: Optional[bool] = None):
        pulumi.set(__self__, "id", id)
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if expression is not None:
            pulumi.set(__self__, "expression", expression)
        if label is not None:
            pulumi.set(__self__, "label", label)
        if metric_stat is not None:
            pulumi.set(__self__, "metric_stat", metric_stat)
        if period is not None:
            pulumi.set(__self__, "period", period)
        if return_data is not None:
            pulumi.set(__self__, "return_data", return_data)

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[str]:
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def expression(self) -> Optional[str]:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def label(self) -> Optional[str]:
        return pulumi.get(self, "label")

    @property
    @pulumi.getter(name="metricStat")
    def metric_stat(self) -> Optional['outputs.AnomalyDetectorMetricStat']:
        return pulumi.get(self, "metric_stat")

    @property
    @pulumi.getter
    def period(self) -> Optional[int]:
        return pulumi.get(self, "period")

    @property
    @pulumi.getter(name="returnData")
    def return_data(self) -> Optional[bool]:
        return pulumi.get(self, "return_data")


@pulumi.output_type
class AnomalyDetectorMetricMathAnomalyDetector(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricDataQueries":
            suggest = "metric_data_queries"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AnomalyDetectorMetricMathAnomalyDetector. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AnomalyDetectorMetricMathAnomalyDetector.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AnomalyDetectorMetricMathAnomalyDetector.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 metric_data_queries: Optional[Sequence['outputs.AnomalyDetectorMetricDataQuery']] = None):
        if metric_data_queries is not None:
            pulumi.set(__self__, "metric_data_queries", metric_data_queries)

    @property
    @pulumi.getter(name="metricDataQueries")
    def metric_data_queries(self) -> Optional[Sequence['outputs.AnomalyDetectorMetricDataQuery']]:
        return pulumi.get(self, "metric_data_queries")


@pulumi.output_type
class AnomalyDetectorMetricStat(dict):
    def __init__(__self__, *,
                 metric: 'outputs.AnomalyDetectorMetric',
                 period: int,
                 stat: str,
                 unit: Optional[str] = None):
        pulumi.set(__self__, "metric", metric)
        pulumi.set(__self__, "period", period)
        pulumi.set(__self__, "stat", stat)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter
    def metric(self) -> 'outputs.AnomalyDetectorMetric':
        return pulumi.get(self, "metric")

    @property
    @pulumi.getter
    def period(self) -> int:
        return pulumi.get(self, "period")

    @property
    @pulumi.getter
    def stat(self) -> str:
        return pulumi.get(self, "stat")

    @property
    @pulumi.getter
    def unit(self) -> Optional[str]:
        return pulumi.get(self, "unit")


@pulumi.output_type
class AnomalyDetectorRange(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endTime":
            suggest = "end_time"
        elif key == "startTime":
            suggest = "start_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AnomalyDetectorRange. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AnomalyDetectorRange.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AnomalyDetectorRange.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 end_time: str,
                 start_time: str):
        pulumi.set(__self__, "end_time", end_time)
        pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> str:
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        return pulumi.get(self, "start_time")


@pulumi.output_type
class AnomalyDetectorSingleMetricAnomalyDetector(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricName":
            suggest = "metric_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AnomalyDetectorSingleMetricAnomalyDetector. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AnomalyDetectorSingleMetricAnomalyDetector.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AnomalyDetectorSingleMetricAnomalyDetector.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 dimensions: Optional[Sequence['outputs.AnomalyDetectorDimension']] = None,
                 metric_name: Optional[str] = None,
                 namespace: Optional[str] = None,
                 stat: Optional[str] = None):
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)
        if metric_name is not None:
            pulumi.set(__self__, "metric_name", metric_name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if stat is not None:
            pulumi.set(__self__, "stat", stat)

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[Sequence['outputs.AnomalyDetectorDimension']]:
        return pulumi.get(self, "dimensions")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> Optional[str]:
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def stat(self) -> Optional[str]:
        return pulumi.get(self, "stat")


@pulumi.output_type
class InsightRuleTags(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class MetricStreamFilter(dict):
    """
    This structure defines the metrics that will be streamed.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricNames":
            suggest = "metric_names"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MetricStreamFilter. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MetricStreamFilter.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MetricStreamFilter.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 namespace: str,
                 metric_names: Optional[Sequence[str]] = None):
        """
        This structure defines the metrics that will be streamed.
        :param str namespace: Only metrics with Namespace matching this value will be streamed.
        :param Sequence[str] metric_names: Only metrics with MetricNames matching these values will be streamed. Must be set together with Namespace.
        """
        pulumi.set(__self__, "namespace", namespace)
        if metric_names is not None:
            pulumi.set(__self__, "metric_names", metric_names)

    @property
    @pulumi.getter
    def namespace(self) -> str:
        """
        Only metrics with Namespace matching this value will be streamed.
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter(name="metricNames")
    def metric_names(self) -> Optional[Sequence[str]]:
        """
        Only metrics with MetricNames matching these values will be streamed. Must be set together with Namespace.
        """
        return pulumi.get(self, "metric_names")


@pulumi.output_type
class MetricStreamStatisticsConfiguration(dict):
    """
    This structure specifies a list of additional statistics to stream, and the metrics to stream those additional statistics for. All metrics that match the combination of metric name and namespace will be streamed with the extended statistics, no matter their dimensions.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "additionalStatistics":
            suggest = "additional_statistics"
        elif key == "includeMetrics":
            suggest = "include_metrics"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MetricStreamStatisticsConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MetricStreamStatisticsConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MetricStreamStatisticsConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 additional_statistics: Sequence[str],
                 include_metrics: Sequence['outputs.MetricStreamStatisticsMetric']):
        """
        This structure specifies a list of additional statistics to stream, and the metrics to stream those additional statistics for. All metrics that match the combination of metric name and namespace will be streamed with the extended statistics, no matter their dimensions.
        :param Sequence[str] additional_statistics: The additional statistics to stream for the metrics listed in IncludeMetrics.
        :param Sequence['MetricStreamStatisticsMetric'] include_metrics: An array that defines the metrics that are to have additional statistics streamed.
        """
        pulumi.set(__self__, "additional_statistics", additional_statistics)
        pulumi.set(__self__, "include_metrics", include_metrics)

    @property
    @pulumi.getter(name="additionalStatistics")
    def additional_statistics(self) -> Sequence[str]:
        """
        The additional statistics to stream for the metrics listed in IncludeMetrics.
        """
        return pulumi.get(self, "additional_statistics")

    @property
    @pulumi.getter(name="includeMetrics")
    def include_metrics(self) -> Sequence['outputs.MetricStreamStatisticsMetric']:
        """
        An array that defines the metrics that are to have additional statistics streamed.
        """
        return pulumi.get(self, "include_metrics")


@pulumi.output_type
class MetricStreamStatisticsMetric(dict):
    """
    A structure that specifies the metric name and namespace for one metric that is going to have additional statistics included in the stream.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricName":
            suggest = "metric_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MetricStreamStatisticsMetric. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MetricStreamStatisticsMetric.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MetricStreamStatisticsMetric.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 metric_name: str,
                 namespace: str):
        """
        A structure that specifies the metric name and namespace for one metric that is going to have additional statistics included in the stream.
        :param str metric_name: The name of the metric.
        :param str namespace: The namespace of the metric.
        """
        pulumi.set(__self__, "metric_name", metric_name)
        pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> str:
        """
        The name of the metric.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def namespace(self) -> str:
        """
        The namespace of the metric.
        """
        return pulumi.get(self, "namespace")


@pulumi.output_type
class MetricStreamTag(dict):
    """
    Metadata that you can assign to a Metric Stream, consisting of a key-value pair.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        Metadata that you can assign to a Metric Stream, consisting of a key-value pair.
        :param str key: A unique identifier for the tag.
        :param str value: String which you can use to describe or define the tag.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        A unique identifier for the tag.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        String which you can use to describe or define the tag.
        """
        return pulumi.get(self, "value")


