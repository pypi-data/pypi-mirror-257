# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AssociationComplianceSeverity',
    'AssociationSyncCompliance',
    'DocumentAttachmentsSourceKey',
    'DocumentFormat',
    'DocumentType',
    'DocumentUpdateMethod',
    'ParameterDataType',
    'ParameterTier',
    'ParameterType',
    'PatchBaselineApprovedPatchesComplianceLevel',
    'PatchBaselineOperatingSystem',
    'PatchBaselinePatchFilterKey',
    'PatchBaselineRejectedPatchesAction',
    'PatchBaselineRuleComplianceLevel',
]


class AssociationComplianceSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNSPECIFIED = "UNSPECIFIED"


class AssociationSyncCompliance(str, Enum):
    AUTO = "AUTO"
    MANUAL = "MANUAL"


class DocumentAttachmentsSourceKey(str, Enum):
    """
    The key of a key-value pair that identifies the location of an attachment to a document.
    """
    SOURCE_URL = "SourceUrl"
    S3_FILE_URL = "S3FileUrl"
    ATTACHMENT_REFERENCE = "AttachmentReference"


class DocumentFormat(str, Enum):
    """
    Specify the document format for the request. The document format can be either JSON or YAML. JSON is the default format.
    """
    YAML = "YAML"
    JSON = "JSON"
    TEXT = "TEXT"


class DocumentType(str, Enum):
    """
    The type of document to create.
    """
    APPLICATION_CONFIGURATION = "ApplicationConfiguration"
    APPLICATION_CONFIGURATION_SCHEMA = "ApplicationConfigurationSchema"
    AUTOMATION = "Automation"
    AUTOMATION_CHANGE_TEMPLATE = "Automation.ChangeTemplate"
    CHANGE_CALENDAR = "ChangeCalendar"
    CLOUD_FORMATION = "CloudFormation"
    COMMAND = "Command"
    DEPLOYMENT_STRATEGY = "DeploymentStrategy"
    PACKAGE = "Package"
    POLICY = "Policy"
    PROBLEM_ANALYSIS = "ProblemAnalysis"
    PROBLEM_ANALYSIS_TEMPLATE = "ProblemAnalysisTemplate"
    SESSION = "Session"


class DocumentUpdateMethod(str, Enum):
    """
    Update method - when set to 'Replace', the update will replace the existing document; when set to 'NewVersion', the update will create a new version.
    """
    REPLACE = "Replace"
    NEW_VERSION = "NewVersion"


class ParameterDataType(str, Enum):
    """
    The data type of the parameter, such as ``text`` or ``aws:ec2:image``. The default is ``text``.
    """
    TEXT = "text"
    AWSEC2IMAGE = "aws:ec2:image"


class ParameterTier(str, Enum):
    """
    The parameter tier.
    """
    STANDARD = "Standard"
    ADVANCED = "Advanced"
    INTELLIGENT_TIERING = "Intelligent-Tiering"


class ParameterType(str, Enum):
    """
    The type of parameter.
      Although ``SecureString`` is included in the list of valid values, CFNlong does *not* currently support creating a ``SecureString`` parameter type.
    """
    STRING = "String"
    STRING_LIST = "StringList"


class PatchBaselineApprovedPatchesComplianceLevel(str, Enum):
    """
    Defines the compliance level for approved patches. This means that if an approved patch is reported as missing, this is the severity of the compliance violation. The default value is UNSPECIFIED.
    """
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"
    UNSPECIFIED = "UNSPECIFIED"


class PatchBaselineOperatingSystem(str, Enum):
    """
    Defines the operating system the patch baseline applies to. The Default value is WINDOWS.
    """
    WINDOWS = "WINDOWS"
    AMAZON_LINUX = "AMAZON_LINUX"
    AMAZON_LINUX2 = "AMAZON_LINUX_2"
    AMAZON_LINUX2022 = "AMAZON_LINUX_2022"
    AMAZON_LINUX2023 = "AMAZON_LINUX_2023"
    UBUNTU = "UBUNTU"
    REDHAT_ENTERPRISE_LINUX = "REDHAT_ENTERPRISE_LINUX"
    SUSE = "SUSE"
    CENTOS = "CENTOS"
    ORACLE_LINUX = "ORACLE_LINUX"
    DEBIAN = "DEBIAN"
    MACOS = "MACOS"
    RASPBIAN = "RASPBIAN"
    ROCKY_LINUX = "ROCKY_LINUX"


class PatchBaselinePatchFilterKey(str, Enum):
    ADVISORY_ID = "ADVISORY_ID"
    ARCH = "ARCH"
    BUGZILLA_ID = "BUGZILLA_ID"
    CLASSIFICATION = "CLASSIFICATION"
    CVE_ID = "CVE_ID"
    EPOCH = "EPOCH"
    MSRC_SEVERITY = "MSRC_SEVERITY"
    NAME = "NAME"
    PATCH_ID = "PATCH_ID"
    PATCH_SET = "PATCH_SET"
    PRIORITY = "PRIORITY"
    PRODUCT = "PRODUCT"
    PRODUCT_FAMILY = "PRODUCT_FAMILY"
    RELEASE = "RELEASE"
    REPOSITORY = "REPOSITORY"
    SECTION = "SECTION"
    SECURITY = "SECURITY"
    SEVERITY = "SEVERITY"
    VERSION = "VERSION"


class PatchBaselineRejectedPatchesAction(str, Enum):
    """
    The action for Patch Manager to take on patches included in the RejectedPackages list.
    """
    ALLOW_AS_DEPENDENCY = "ALLOW_AS_DEPENDENCY"
    BLOCK = "BLOCK"


class PatchBaselineRuleComplianceLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    INFORMATIONAL = "INFORMATIONAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    UNSPECIFIED = "UNSPECIFIED"
