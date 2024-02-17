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
    'GetStackSetConstraintResult',
    'AwaitableGetStackSetConstraintResult',
    'get_stack_set_constraint',
    'get_stack_set_constraint_output',
]

@pulumi.output_type
class GetStackSetConstraintResult:
    def __init__(__self__, accept_language=None, account_list=None, admin_role=None, description=None, execution_role=None, id=None, region_list=None, stack_instance_control=None):
        if accept_language and not isinstance(accept_language, str):
            raise TypeError("Expected argument 'accept_language' to be a str")
        pulumi.set(__self__, "accept_language", accept_language)
        if account_list and not isinstance(account_list, list):
            raise TypeError("Expected argument 'account_list' to be a list")
        pulumi.set(__self__, "account_list", account_list)
        if admin_role and not isinstance(admin_role, str):
            raise TypeError("Expected argument 'admin_role' to be a str")
        pulumi.set(__self__, "admin_role", admin_role)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if execution_role and not isinstance(execution_role, str):
            raise TypeError("Expected argument 'execution_role' to be a str")
        pulumi.set(__self__, "execution_role", execution_role)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if region_list and not isinstance(region_list, list):
            raise TypeError("Expected argument 'region_list' to be a list")
        pulumi.set(__self__, "region_list", region_list)
        if stack_instance_control and not isinstance(stack_instance_control, str):
            raise TypeError("Expected argument 'stack_instance_control' to be a str")
        pulumi.set(__self__, "stack_instance_control", stack_instance_control)

    @property
    @pulumi.getter(name="acceptLanguage")
    def accept_language(self) -> Optional[str]:
        return pulumi.get(self, "accept_language")

    @property
    @pulumi.getter(name="accountList")
    def account_list(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "account_list")

    @property
    @pulumi.getter(name="adminRole")
    def admin_role(self) -> Optional[str]:
        return pulumi.get(self, "admin_role")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="executionRole")
    def execution_role(self) -> Optional[str]:
        return pulumi.get(self, "execution_role")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="regionList")
    def region_list(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "region_list")

    @property
    @pulumi.getter(name="stackInstanceControl")
    def stack_instance_control(self) -> Optional[str]:
        return pulumi.get(self, "stack_instance_control")


class AwaitableGetStackSetConstraintResult(GetStackSetConstraintResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStackSetConstraintResult(
            accept_language=self.accept_language,
            account_list=self.account_list,
            admin_role=self.admin_role,
            description=self.description,
            execution_role=self.execution_role,
            id=self.id,
            region_list=self.region_list,
            stack_instance_control=self.stack_instance_control)


def get_stack_set_constraint(id: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStackSetConstraintResult:
    """
    Resource Type definition for AWS::ServiceCatalog::StackSetConstraint
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:servicecatalog:getStackSetConstraint', __args__, opts=opts, typ=GetStackSetConstraintResult).value

    return AwaitableGetStackSetConstraintResult(
        accept_language=pulumi.get(__ret__, 'accept_language'),
        account_list=pulumi.get(__ret__, 'account_list'),
        admin_role=pulumi.get(__ret__, 'admin_role'),
        description=pulumi.get(__ret__, 'description'),
        execution_role=pulumi.get(__ret__, 'execution_role'),
        id=pulumi.get(__ret__, 'id'),
        region_list=pulumi.get(__ret__, 'region_list'),
        stack_instance_control=pulumi.get(__ret__, 'stack_instance_control'))


@_utilities.lift_output_func(get_stack_set_constraint)
def get_stack_set_constraint_output(id: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStackSetConstraintResult]:
    """
    Resource Type definition for AWS::ServiceCatalog::StackSetConstraint
    """
    ...
