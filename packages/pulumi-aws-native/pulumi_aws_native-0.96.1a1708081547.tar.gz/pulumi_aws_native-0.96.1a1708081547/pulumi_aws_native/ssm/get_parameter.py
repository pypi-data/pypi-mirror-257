# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'GetParameterResult',
    'AwaitableGetParameterResult',
    'get_parameter',
    'get_parameter_output',
]

@pulumi.output_type
class GetParameterResult:
    def __init__(__self__, data_type=None, type=None, value=None):
        if data_type and not isinstance(data_type, str):
            raise TypeError("Expected argument 'data_type' to be a str")
        pulumi.set(__self__, "data_type", data_type)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="dataType")
    def data_type(self) -> Optional['ParameterDataType']:
        """
        The data type of the parameter, such as ``text`` or ``aws:ec2:image``. The default is ``text``.
        """
        return pulumi.get(self, "data_type")

    @property
    @pulumi.getter
    def type(self) -> Optional['ParameterType']:
        """
        The type of parameter.
          Although ``SecureString`` is included in the list of valid values, CFNlong does *not* currently support creating a ``SecureString`` parameter type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        The parameter value.
          If type is ``StringList``, the system returns a comma-separated string with no spaces between commas in the ``Value`` field.
        """
        return pulumi.get(self, "value")


class AwaitableGetParameterResult(GetParameterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetParameterResult(
            data_type=self.data_type,
            type=self.type,
            value=self.value)


def get_parameter(name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetParameterResult:
    """
    The ``AWS::SSM::Parameter`` resource creates an SSM parameter in SYSlong Parameter Store.
      To create an SSM parameter, you must have the IAMlong (IAM) permissions ``ssm:PutParameter`` and ``ssm:AddTagsToResource``. On stack creation, CFNlong adds the following three tags to the parameter: ``aws:cloudformation:stack-name``, ``aws:cloudformation:logical-id``, and ``aws:cloudformation:stack-id``, in addition to any custom tags you specify.
     To add, update, or remove tags during stack update, you must have IAM permissions for both ``ssm:AddTagsToResource`` and ``ssm:RemoveTagsFromResource``. For more information, see [Managing Access Using Policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/security-iam.html#security_iam_access-manage) in the *User Guide*.
      For information about valid values for parameters, see [Requirements and Constraints for Parameter Names](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-create.html#sysman-paramete


    :param str name: The name of the parameter.
            The maximum length constraint listed below includes capacity for additional system attributes that aren't part of the name. The maximum length for a parameter name, including the full length of the parameter ARN, is 1011 characters. For example, the length of the following parameter name is 65 characters, not 20 characters: ``arn:aws:ssm:us-east-2:111222333444:parameter/ExampleParameterName``
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ssm:getParameter', __args__, opts=opts, typ=GetParameterResult).value

    return AwaitableGetParameterResult(
        data_type=pulumi.get(__ret__, 'data_type'),
        type=pulumi.get(__ret__, 'type'),
        value=pulumi.get(__ret__, 'value'))


@_utilities.lift_output_func(get_parameter)
def get_parameter_output(name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetParameterResult]:
    """
    The ``AWS::SSM::Parameter`` resource creates an SSM parameter in SYSlong Parameter Store.
      To create an SSM parameter, you must have the IAMlong (IAM) permissions ``ssm:PutParameter`` and ``ssm:AddTagsToResource``. On stack creation, CFNlong adds the following three tags to the parameter: ``aws:cloudformation:stack-name``, ``aws:cloudformation:logical-id``, and ``aws:cloudformation:stack-id``, in addition to any custom tags you specify.
     To add, update, or remove tags during stack update, you must have IAM permissions for both ``ssm:AddTagsToResource`` and ``ssm:RemoveTagsFromResource``. For more information, see [Managing Access Using Policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/security-iam.html#security_iam_access-manage) in the *User Guide*.
      For information about valid values for parameters, see [Requirements and Constraints for Parameter Names](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-create.html#sysman-paramete


    :param str name: The name of the parameter.
            The maximum length constraint listed below includes capacity for additional system attributes that aren't part of the name. The maximum length for a parameter name, including the full length of the parameter ARN, is 1011 characters. For example, the length of the following parameter name is 65 characters, not 20 characters: ``arn:aws:ssm:us-east-2:111222333444:parameter/ExampleParameterName``
    """
    ...
