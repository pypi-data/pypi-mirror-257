# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'DataSourceEnableSetting',
    'DataSourceFilterExpressionType',
    'DataSourceStatus',
    'DomainAuthType',
    'DomainStatus',
    'DomainUserAssignment',
    'EnvironmentStatus',
]


class DataSourceEnableSetting(str, Enum):
    """
    Specifies whether the data source is enabled.
    """
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class DataSourceFilterExpressionType(str, Enum):
    """
    The search filter expression type.
    """
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class DataSourceStatus(str, Enum):
    """
    The status of the data source.
    """
    CREATING = "CREATING"
    FAILED_CREATION = "FAILED_CREATION"
    READY = "READY"
    UPDATING = "UPDATING"
    FAILED_UPDATE = "FAILED_UPDATE"
    RUNNING = "RUNNING"
    DELETING = "DELETING"
    FAILED_DELETION = "FAILED_DELETION"


class DomainAuthType(str, Enum):
    """
    The type of single sign-on in Amazon DataZone.
    """
    IAM_IDC = "IAM_IDC"
    DISABLED = "DISABLED"


class DomainStatus(str, Enum):
    """
    The status of the Amazon DataZone domain.
    """
    CREATING = "CREATING"
    AVAILABLE = "AVAILABLE"
    CREATION_FAILED = "CREATION_FAILED"
    DELETING = "DELETING"
    DELETED = "DELETED"
    DELETION_FAILED = "DELETION_FAILED"


class DomainUserAssignment(str, Enum):
    """
    The single sign-on user assignment in Amazon DataZone.
    """
    AUTOMATIC = "AUTOMATIC"
    MANUAL = "MANUAL"


class EnvironmentStatus(str, Enum):
    """
    The status of the Amazon DataZone environment.
    """
    ACTIVE = "ACTIVE"
    CREATING = "CREATING"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    CREATE_FAILED = "CREATE_FAILED"
    UPDATE_FAILED = "UPDATE_FAILED"
    DELETE_FAILED = "DELETE_FAILED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    SUSPENDED = "SUSPENDED"
    DISABLED = "DISABLED"
    EXPIRED = "EXPIRED"
    DELETED = "DELETED"
    INACCESSIBLE = "INACCESSIBLE"
