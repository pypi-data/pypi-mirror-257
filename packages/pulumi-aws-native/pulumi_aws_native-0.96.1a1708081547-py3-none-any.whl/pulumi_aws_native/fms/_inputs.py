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
    'PolicyIeMapArgs',
    'PolicyNetworkFirewallPolicyArgs',
    'PolicyOptionArgs',
    'PolicyResourceTagArgs',
    'PolicySecurityServicePolicyDataArgs',
    'PolicyTagArgs',
    'PolicyThirdPartyFirewallPolicyArgs',
    'ResourceSetTagArgs',
]

@pulumi.input_type
class PolicyIeMapArgs:
    def __init__(__self__, *,
                 account: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 orgunit: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        An FMS includeMap or excludeMap.
        """
        if account is not None:
            pulumi.set(__self__, "account", account)
        if orgunit is not None:
            pulumi.set(__self__, "orgunit", orgunit)

    @property
    @pulumi.getter
    def account(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "account")

    @account.setter
    def account(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "account", value)

    @property
    @pulumi.getter
    def orgunit(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "orgunit")

    @orgunit.setter
    def orgunit(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "orgunit", value)


@pulumi.input_type
class PolicyNetworkFirewallPolicyArgs:
    def __init__(__self__, *,
                 firewall_deployment_model: pulumi.Input['PolicyFirewallDeploymentModel']):
        """
        Network firewall policy.
        """
        pulumi.set(__self__, "firewall_deployment_model", firewall_deployment_model)

    @property
    @pulumi.getter(name="firewallDeploymentModel")
    def firewall_deployment_model(self) -> pulumi.Input['PolicyFirewallDeploymentModel']:
        return pulumi.get(self, "firewall_deployment_model")

    @firewall_deployment_model.setter
    def firewall_deployment_model(self, value: pulumi.Input['PolicyFirewallDeploymentModel']):
        pulumi.set(self, "firewall_deployment_model", value)


@pulumi.input_type
class PolicyOptionArgs:
    def __init__(__self__, *,
                 network_firewall_policy: Optional[pulumi.Input['PolicyNetworkFirewallPolicyArgs']] = None,
                 third_party_firewall_policy: Optional[pulumi.Input['PolicyThirdPartyFirewallPolicyArgs']] = None):
        """
        Firewall policy option.
        """
        if network_firewall_policy is not None:
            pulumi.set(__self__, "network_firewall_policy", network_firewall_policy)
        if third_party_firewall_policy is not None:
            pulumi.set(__self__, "third_party_firewall_policy", third_party_firewall_policy)

    @property
    @pulumi.getter(name="networkFirewallPolicy")
    def network_firewall_policy(self) -> Optional[pulumi.Input['PolicyNetworkFirewallPolicyArgs']]:
        return pulumi.get(self, "network_firewall_policy")

    @network_firewall_policy.setter
    def network_firewall_policy(self, value: Optional[pulumi.Input['PolicyNetworkFirewallPolicyArgs']]):
        pulumi.set(self, "network_firewall_policy", value)

    @property
    @pulumi.getter(name="thirdPartyFirewallPolicy")
    def third_party_firewall_policy(self) -> Optional[pulumi.Input['PolicyThirdPartyFirewallPolicyArgs']]:
        return pulumi.get(self, "third_party_firewall_policy")

    @third_party_firewall_policy.setter
    def third_party_firewall_policy(self, value: Optional[pulumi.Input['PolicyThirdPartyFirewallPolicyArgs']]):
        pulumi.set(self, "third_party_firewall_policy", value)


@pulumi.input_type
class PolicyResourceTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: Optional[pulumi.Input[str]] = None):
        """
        A resource tag.
        """
        pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class PolicySecurityServicePolicyDataArgs:
    def __init__(__self__, *,
                 type: pulumi.Input['PolicyType'],
                 managed_service_data: Optional[pulumi.Input[str]] = None,
                 policy_option: Optional[pulumi.Input['PolicyOptionArgs']] = None):
        """
        Firewall security service policy data.
        """
        pulumi.set(__self__, "type", type)
        if managed_service_data is not None:
            pulumi.set(__self__, "managed_service_data", managed_service_data)
        if policy_option is not None:
            pulumi.set(__self__, "policy_option", policy_option)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['PolicyType']:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['PolicyType']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="managedServiceData")
    def managed_service_data(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "managed_service_data")

    @managed_service_data.setter
    def managed_service_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "managed_service_data", value)

    @property
    @pulumi.getter(name="policyOption")
    def policy_option(self) -> Optional[pulumi.Input['PolicyOptionArgs']]:
        return pulumi.get(self, "policy_option")

    @policy_option.setter
    def policy_option(self, value: Optional[pulumi.Input['PolicyOptionArgs']]):
        pulumi.set(self, "policy_option", value)


@pulumi.input_type
class PolicyTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        A policy tag.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class PolicyThirdPartyFirewallPolicyArgs:
    def __init__(__self__, *,
                 firewall_deployment_model: pulumi.Input['PolicyFirewallDeploymentModel']):
        """
        Third party firewall policy.
        """
        pulumi.set(__self__, "firewall_deployment_model", firewall_deployment_model)

    @property
    @pulumi.getter(name="firewallDeploymentModel")
    def firewall_deployment_model(self) -> pulumi.Input['PolicyFirewallDeploymentModel']:
        return pulumi.get(self, "firewall_deployment_model")

    @firewall_deployment_model.setter
    def firewall_deployment_model(self, value: pulumi.Input['PolicyFirewallDeploymentModel']):
        pulumi.set(self, "firewall_deployment_model", value)


@pulumi.input_type
class ResourceSetTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        A tag.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


