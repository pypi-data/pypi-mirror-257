# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetBasePathMappingResult',
    'AwaitableGetBasePathMappingResult',
    'get_base_path_mapping',
    'get_base_path_mapping_output',
]

@pulumi.output_type
class GetBasePathMappingResult:
    def __init__(__self__, rest_api_id=None, stage=None):
        if rest_api_id and not isinstance(rest_api_id, str):
            raise TypeError("Expected argument 'rest_api_id' to be a str")
        pulumi.set(__self__, "rest_api_id", rest_api_id)
        if stage and not isinstance(stage, str):
            raise TypeError("Expected argument 'stage' to be a str")
        pulumi.set(__self__, "stage", stage)

    @property
    @pulumi.getter(name="restApiId")
    def rest_api_id(self) -> Optional[str]:
        """
        The string identifier of the associated RestApi.
        """
        return pulumi.get(self, "rest_api_id")

    @property
    @pulumi.getter
    def stage(self) -> Optional[str]:
        """
        The name of the associated stage.
        """
        return pulumi.get(self, "stage")


class AwaitableGetBasePathMappingResult(GetBasePathMappingResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBasePathMappingResult(
            rest_api_id=self.rest_api_id,
            stage=self.stage)


def get_base_path_mapping(base_path: Optional[str] = None,
                          domain_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBasePathMappingResult:
    """
    The ``AWS::ApiGateway::BasePathMapping`` resource creates a base path that clients who call your API must use in the invocation URL.


    :param str base_path: The base path name that callers of the API must provide as part of the URL after the domain name.
    :param str domain_name: The domain name of the BasePathMapping resource to be described.
    """
    __args__ = dict()
    __args__['basePath'] = base_path
    __args__['domainName'] = domain_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:apigateway:getBasePathMapping', __args__, opts=opts, typ=GetBasePathMappingResult).value

    return AwaitableGetBasePathMappingResult(
        rest_api_id=pulumi.get(__ret__, 'rest_api_id'),
        stage=pulumi.get(__ret__, 'stage'))


@_utilities.lift_output_func(get_base_path_mapping)
def get_base_path_mapping_output(base_path: Optional[pulumi.Input[str]] = None,
                                 domain_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBasePathMappingResult]:
    """
    The ``AWS::ApiGateway::BasePathMapping`` resource creates a base path that clients who call your API must use in the invocation URL.


    :param str base_path: The base path name that callers of the API must provide as part of the URL after the domain name.
    :param str domain_name: The domain name of the BasePathMapping resource to be described.
    """
    ...
