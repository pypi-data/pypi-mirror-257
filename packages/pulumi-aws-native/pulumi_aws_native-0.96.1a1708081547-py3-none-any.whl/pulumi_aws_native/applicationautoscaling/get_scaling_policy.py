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
    'GetScalingPolicyResult',
    'AwaitableGetScalingPolicyResult',
    'get_scaling_policy',
    'get_scaling_policy_output',
]

@pulumi.output_type
class GetScalingPolicyResult:
    def __init__(__self__, arn=None, policy_type=None, step_scaling_policy_configuration=None, target_tracking_scaling_policy_configuration=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if policy_type and not isinstance(policy_type, str):
            raise TypeError("Expected argument 'policy_type' to be a str")
        pulumi.set(__self__, "policy_type", policy_type)
        if step_scaling_policy_configuration and not isinstance(step_scaling_policy_configuration, dict):
            raise TypeError("Expected argument 'step_scaling_policy_configuration' to be a dict")
        pulumi.set(__self__, "step_scaling_policy_configuration", step_scaling_policy_configuration)
        if target_tracking_scaling_policy_configuration and not isinstance(target_tracking_scaling_policy_configuration, dict):
            raise TypeError("Expected argument 'target_tracking_scaling_policy_configuration' to be a dict")
        pulumi.set(__self__, "target_tracking_scaling_policy_configuration", target_tracking_scaling_policy_configuration)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        ARN is a read only property for the resource.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> Optional[str]:
        """
        The scaling policy type.

        The following policy types are supported:

        TargetTrackingScaling Not supported for Amazon EMR

        StepScaling Not supported for DynamoDB, Amazon Comprehend, Lambda, Amazon Keyspaces, Amazon MSK, Amazon ElastiCache, or Neptune.
        """
        return pulumi.get(self, "policy_type")

    @property
    @pulumi.getter(name="stepScalingPolicyConfiguration")
    def step_scaling_policy_configuration(self) -> Optional['outputs.ScalingPolicyStepScalingPolicyConfiguration']:
        """
        A step scaling policy.
        """
        return pulumi.get(self, "step_scaling_policy_configuration")

    @property
    @pulumi.getter(name="targetTrackingScalingPolicyConfiguration")
    def target_tracking_scaling_policy_configuration(self) -> Optional['outputs.ScalingPolicyTargetTrackingScalingPolicyConfiguration']:
        """
        A target tracking scaling policy.
        """
        return pulumi.get(self, "target_tracking_scaling_policy_configuration")


class AwaitableGetScalingPolicyResult(GetScalingPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetScalingPolicyResult(
            arn=self.arn,
            policy_type=self.policy_type,
            step_scaling_policy_configuration=self.step_scaling_policy_configuration,
            target_tracking_scaling_policy_configuration=self.target_tracking_scaling_policy_configuration)


def get_scaling_policy(arn: Optional[str] = None,
                       scalable_dimension: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetScalingPolicyResult:
    """
    Resource Type definition for AWS::ApplicationAutoScaling::ScalingPolicy


    :param str arn: ARN is a read only property for the resource.
    :param str scalable_dimension: The scalable dimension. This string consists of the service namespace, resource type, and scaling property.
    """
    __args__ = dict()
    __args__['arn'] = arn
    __args__['scalableDimension'] = scalable_dimension
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:applicationautoscaling:getScalingPolicy', __args__, opts=opts, typ=GetScalingPolicyResult).value

    return AwaitableGetScalingPolicyResult(
        arn=pulumi.get(__ret__, 'arn'),
        policy_type=pulumi.get(__ret__, 'policy_type'),
        step_scaling_policy_configuration=pulumi.get(__ret__, 'step_scaling_policy_configuration'),
        target_tracking_scaling_policy_configuration=pulumi.get(__ret__, 'target_tracking_scaling_policy_configuration'))


@_utilities.lift_output_func(get_scaling_policy)
def get_scaling_policy_output(arn: Optional[pulumi.Input[str]] = None,
                              scalable_dimension: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetScalingPolicyResult]:
    """
    Resource Type definition for AWS::ApplicationAutoScaling::ScalingPolicy


    :param str arn: ARN is a read only property for the resource.
    :param str scalable_dimension: The scalable dimension. This string consists of the service namespace, resource type, and scaling property.
    """
    ...
