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
from ._inputs import *

__all__ = ['BotAliasArgs', 'BotAlias']

@pulumi.input_type
class BotAliasArgs:
    def __init__(__self__, *,
                 bot_id: pulumi.Input[str],
                 bot_alias_locale_settings: Optional[pulumi.Input[Sequence[pulumi.Input['BotAliasLocaleSettingsItemArgs']]]] = None,
                 bot_alias_name: Optional[pulumi.Input[str]] = None,
                 bot_alias_tags: Optional[pulumi.Input[Sequence[pulumi.Input['BotAliasTagArgs']]]] = None,
                 bot_version: Optional[pulumi.Input[str]] = None,
                 conversation_log_settings: Optional[pulumi.Input['BotAliasConversationLogSettingsArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 sentiment_analysis_settings: Optional[pulumi.Input['SentimentAnalysisSettingsPropertiesArgs']] = None):
        """
        The set of arguments for constructing a BotAlias resource.
        :param pulumi.Input[Sequence[pulumi.Input['BotAliasTagArgs']]] bot_alias_tags: A list of tags to add to the bot alias.
        :param pulumi.Input['SentimentAnalysisSettingsPropertiesArgs'] sentiment_analysis_settings: Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.
        """
        pulumi.set(__self__, "bot_id", bot_id)
        if bot_alias_locale_settings is not None:
            pulumi.set(__self__, "bot_alias_locale_settings", bot_alias_locale_settings)
        if bot_alias_name is not None:
            pulumi.set(__self__, "bot_alias_name", bot_alias_name)
        if bot_alias_tags is not None:
            pulumi.set(__self__, "bot_alias_tags", bot_alias_tags)
        if bot_version is not None:
            pulumi.set(__self__, "bot_version", bot_version)
        if conversation_log_settings is not None:
            pulumi.set(__self__, "conversation_log_settings", conversation_log_settings)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if sentiment_analysis_settings is not None:
            pulumi.set(__self__, "sentiment_analysis_settings", sentiment_analysis_settings)

    @property
    @pulumi.getter(name="botId")
    def bot_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "bot_id")

    @bot_id.setter
    def bot_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "bot_id", value)

    @property
    @pulumi.getter(name="botAliasLocaleSettings")
    def bot_alias_locale_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BotAliasLocaleSettingsItemArgs']]]]:
        return pulumi.get(self, "bot_alias_locale_settings")

    @bot_alias_locale_settings.setter
    def bot_alias_locale_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BotAliasLocaleSettingsItemArgs']]]]):
        pulumi.set(self, "bot_alias_locale_settings", value)

    @property
    @pulumi.getter(name="botAliasName")
    def bot_alias_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "bot_alias_name")

    @bot_alias_name.setter
    def bot_alias_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bot_alias_name", value)

    @property
    @pulumi.getter(name="botAliasTags")
    def bot_alias_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BotAliasTagArgs']]]]:
        """
        A list of tags to add to the bot alias.
        """
        return pulumi.get(self, "bot_alias_tags")

    @bot_alias_tags.setter
    def bot_alias_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BotAliasTagArgs']]]]):
        pulumi.set(self, "bot_alias_tags", value)

    @property
    @pulumi.getter(name="botVersion")
    def bot_version(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "bot_version")

    @bot_version.setter
    def bot_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bot_version", value)

    @property
    @pulumi.getter(name="conversationLogSettings")
    def conversation_log_settings(self) -> Optional[pulumi.Input['BotAliasConversationLogSettingsArgs']]:
        return pulumi.get(self, "conversation_log_settings")

    @conversation_log_settings.setter
    def conversation_log_settings(self, value: Optional[pulumi.Input['BotAliasConversationLogSettingsArgs']]):
        pulumi.set(self, "conversation_log_settings", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="sentimentAnalysisSettings")
    def sentiment_analysis_settings(self) -> Optional[pulumi.Input['SentimentAnalysisSettingsPropertiesArgs']]:
        """
        Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.
        """
        return pulumi.get(self, "sentiment_analysis_settings")

    @sentiment_analysis_settings.setter
    def sentiment_analysis_settings(self, value: Optional[pulumi.Input['SentimentAnalysisSettingsPropertiesArgs']]):
        pulumi.set(self, "sentiment_analysis_settings", value)


class BotAlias(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bot_alias_locale_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotAliasLocaleSettingsItemArgs']]]]] = None,
                 bot_alias_name: Optional[pulumi.Input[str]] = None,
                 bot_alias_tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotAliasTagArgs']]]]] = None,
                 bot_id: Optional[pulumi.Input[str]] = None,
                 bot_version: Optional[pulumi.Input[str]] = None,
                 conversation_log_settings: Optional[pulumi.Input[pulumi.InputType['BotAliasConversationLogSettingsArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 sentiment_analysis_settings: Optional[pulumi.Input[pulumi.InputType['SentimentAnalysisSettingsPropertiesArgs']]] = None,
                 __props__=None):
        """
        A Bot Alias enables you to change the version of a bot without updating applications that use the bot

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotAliasTagArgs']]]] bot_alias_tags: A list of tags to add to the bot alias.
        :param pulumi.Input[pulumi.InputType['SentimentAnalysisSettingsPropertiesArgs']] sentiment_analysis_settings: Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BotAliasArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A Bot Alias enables you to change the version of a bot without updating applications that use the bot

        :param str resource_name: The name of the resource.
        :param BotAliasArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BotAliasArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bot_alias_locale_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotAliasLocaleSettingsItemArgs']]]]] = None,
                 bot_alias_name: Optional[pulumi.Input[str]] = None,
                 bot_alias_tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotAliasTagArgs']]]]] = None,
                 bot_id: Optional[pulumi.Input[str]] = None,
                 bot_version: Optional[pulumi.Input[str]] = None,
                 conversation_log_settings: Optional[pulumi.Input[pulumi.InputType['BotAliasConversationLogSettingsArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 sentiment_analysis_settings: Optional[pulumi.Input[pulumi.InputType['SentimentAnalysisSettingsPropertiesArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BotAliasArgs.__new__(BotAliasArgs)

            __props__.__dict__["bot_alias_locale_settings"] = bot_alias_locale_settings
            __props__.__dict__["bot_alias_name"] = bot_alias_name
            __props__.__dict__["bot_alias_tags"] = bot_alias_tags
            if bot_id is None and not opts.urn:
                raise TypeError("Missing required property 'bot_id'")
            __props__.__dict__["bot_id"] = bot_id
            __props__.__dict__["bot_version"] = bot_version
            __props__.__dict__["conversation_log_settings"] = conversation_log_settings
            __props__.__dict__["description"] = description
            __props__.__dict__["sentiment_analysis_settings"] = sentiment_analysis_settings
            __props__.__dict__["arn"] = None
            __props__.__dict__["bot_alias_id"] = None
            __props__.__dict__["bot_alias_status"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["bot_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(BotAlias, __self__).__init__(
            'aws-native:lex:BotAlias',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BotAlias':
        """
        Get an existing BotAlias resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BotAliasArgs.__new__(BotAliasArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["bot_alias_id"] = None
        __props__.__dict__["bot_alias_locale_settings"] = None
        __props__.__dict__["bot_alias_name"] = None
        __props__.__dict__["bot_alias_status"] = None
        __props__.__dict__["bot_alias_tags"] = None
        __props__.__dict__["bot_id"] = None
        __props__.__dict__["bot_version"] = None
        __props__.__dict__["conversation_log_settings"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["sentiment_analysis_settings"] = None
        return BotAlias(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="botAliasId")
    def bot_alias_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "bot_alias_id")

    @property
    @pulumi.getter(name="botAliasLocaleSettings")
    def bot_alias_locale_settings(self) -> pulumi.Output[Optional[Sequence['outputs.BotAliasLocaleSettingsItem']]]:
        return pulumi.get(self, "bot_alias_locale_settings")

    @property
    @pulumi.getter(name="botAliasName")
    def bot_alias_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "bot_alias_name")

    @property
    @pulumi.getter(name="botAliasStatus")
    def bot_alias_status(self) -> pulumi.Output['BotAliasStatus']:
        return pulumi.get(self, "bot_alias_status")

    @property
    @pulumi.getter(name="botAliasTags")
    def bot_alias_tags(self) -> pulumi.Output[Optional[Sequence['outputs.BotAliasTag']]]:
        """
        A list of tags to add to the bot alias.
        """
        return pulumi.get(self, "bot_alias_tags")

    @property
    @pulumi.getter(name="botId")
    def bot_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "bot_id")

    @property
    @pulumi.getter(name="botVersion")
    def bot_version(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "bot_version")

    @property
    @pulumi.getter(name="conversationLogSettings")
    def conversation_log_settings(self) -> pulumi.Output[Optional['outputs.BotAliasConversationLogSettings']]:
        return pulumi.get(self, "conversation_log_settings")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="sentimentAnalysisSettings")
    def sentiment_analysis_settings(self) -> pulumi.Output[Optional['outputs.SentimentAnalysisSettingsProperties']]:
        """
        Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.
        """
        return pulumi.get(self, "sentiment_analysis_settings")

