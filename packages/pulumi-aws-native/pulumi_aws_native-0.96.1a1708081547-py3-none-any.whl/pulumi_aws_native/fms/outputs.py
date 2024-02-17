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
    'PolicyIeMap',
    'PolicyNetworkFirewallPolicy',
    'PolicyOption',
    'PolicyResourceTag',
    'PolicySecurityServicePolicyData',
    'PolicyTag',
    'PolicyThirdPartyFirewallPolicy',
    'ResourceSetTag',
]

@pulumi.output_type
class PolicyIeMap(dict):
    """
    An FMS includeMap or excludeMap.
    """
    def __init__(__self__, *,
                 account: Optional[Sequence[str]] = None,
                 orgunit: Optional[Sequence[str]] = None):
        """
        An FMS includeMap or excludeMap.
        """
        if account is not None:
            pulumi.set(__self__, "account", account)
        if orgunit is not None:
            pulumi.set(__self__, "orgunit", orgunit)

    @property
    @pulumi.getter
    def account(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "account")

    @property
    @pulumi.getter
    def orgunit(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "orgunit")


@pulumi.output_type
class PolicyNetworkFirewallPolicy(dict):
    """
    Network firewall policy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "firewallDeploymentModel":
            suggest = "firewall_deployment_model"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyNetworkFirewallPolicy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyNetworkFirewallPolicy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyNetworkFirewallPolicy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 firewall_deployment_model: 'PolicyFirewallDeploymentModel'):
        """
        Network firewall policy.
        """
        pulumi.set(__self__, "firewall_deployment_model", firewall_deployment_model)

    @property
    @pulumi.getter(name="firewallDeploymentModel")
    def firewall_deployment_model(self) -> 'PolicyFirewallDeploymentModel':
        return pulumi.get(self, "firewall_deployment_model")


@pulumi.output_type
class PolicyOption(dict):
    """
    Firewall policy option.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "networkFirewallPolicy":
            suggest = "network_firewall_policy"
        elif key == "thirdPartyFirewallPolicy":
            suggest = "third_party_firewall_policy"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyOption. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyOption.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyOption.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 network_firewall_policy: Optional['outputs.PolicyNetworkFirewallPolicy'] = None,
                 third_party_firewall_policy: Optional['outputs.PolicyThirdPartyFirewallPolicy'] = None):
        """
        Firewall policy option.
        """
        if network_firewall_policy is not None:
            pulumi.set(__self__, "network_firewall_policy", network_firewall_policy)
        if third_party_firewall_policy is not None:
            pulumi.set(__self__, "third_party_firewall_policy", third_party_firewall_policy)

    @property
    @pulumi.getter(name="networkFirewallPolicy")
    def network_firewall_policy(self) -> Optional['outputs.PolicyNetworkFirewallPolicy']:
        return pulumi.get(self, "network_firewall_policy")

    @property
    @pulumi.getter(name="thirdPartyFirewallPolicy")
    def third_party_firewall_policy(self) -> Optional['outputs.PolicyThirdPartyFirewallPolicy']:
        return pulumi.get(self, "third_party_firewall_policy")


@pulumi.output_type
class PolicyResourceTag(dict):
    """
    A resource tag.
    """
    def __init__(__self__, *,
                 key: str,
                 value: Optional[str] = None):
        """
        A resource tag.
        """
        pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        return pulumi.get(self, "value")


@pulumi.output_type
class PolicySecurityServicePolicyData(dict):
    """
    Firewall security service policy data.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "managedServiceData":
            suggest = "managed_service_data"
        elif key == "policyOption":
            suggest = "policy_option"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicySecurityServicePolicyData. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicySecurityServicePolicyData.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicySecurityServicePolicyData.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: 'PolicyType',
                 managed_service_data: Optional[str] = None,
                 policy_option: Optional['outputs.PolicyOption'] = None):
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
    def type(self) -> 'PolicyType':
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="managedServiceData")
    def managed_service_data(self) -> Optional[str]:
        return pulumi.get(self, "managed_service_data")

    @property
    @pulumi.getter(name="policyOption")
    def policy_option(self) -> Optional['outputs.PolicyOption']:
        return pulumi.get(self, "policy_option")


@pulumi.output_type
class PolicyTag(dict):
    """
    A policy tag.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A policy tag.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class PolicyThirdPartyFirewallPolicy(dict):
    """
    Third party firewall policy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "firewallDeploymentModel":
            suggest = "firewall_deployment_model"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyThirdPartyFirewallPolicy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyThirdPartyFirewallPolicy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyThirdPartyFirewallPolicy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 firewall_deployment_model: 'PolicyFirewallDeploymentModel'):
        """
        Third party firewall policy.
        """
        pulumi.set(__self__, "firewall_deployment_model", firewall_deployment_model)

    @property
    @pulumi.getter(name="firewallDeploymentModel")
    def firewall_deployment_model(self) -> 'PolicyFirewallDeploymentModel':
        return pulumi.get(self, "firewall_deployment_model")


@pulumi.output_type
class ResourceSetTag(dict):
    """
    A tag.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A tag.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


