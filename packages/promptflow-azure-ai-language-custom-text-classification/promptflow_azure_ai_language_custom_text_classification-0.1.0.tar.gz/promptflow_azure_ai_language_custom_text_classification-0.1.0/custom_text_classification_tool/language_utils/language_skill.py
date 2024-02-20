# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from enum import Enum
from custom_text_classification_tool.language_utils.language_mode import LanguageMode

MAX_SYNC_CHARS = 5120
MAX_ASYNC_CHARS = 125000
MAX_TRANSLATION_CHARS = 50000


# Supported language skills:
class LanguageSkill(Enum):
    CUSTOM_TEXT_CLASSIFICATION = 0

    @staticmethod
    def to_str(skill):
        return skill_to_str.get(skill, "Unsupported")

    # Does skill deal with conversations rather than documents?
    @staticmethod
    def is_conversational(skill):
        return skill_to_conversational.get(skill, False)

    @staticmethod
    def is_async_capable(skill):
        return skill_to_async_capabilities.get(skill, False)

    @staticmethod
    def get_mode(skill, input):
        mode = skill_to_default_mode.get(skill, LanguageMode.SYNC)

        if mode == LanguageMode.SYNC and LanguageSkill.is_async_capable(skill):
            # Translation skill has field "Text" instead of "text":
            input_length = None
            if "Text" in input:
                input_length = len(input["Text"])
            elif "text" in input:
                input_length = len(input["text"])

            if input_length > get_max_sync_chars(skill):
                mode = LanguageMode.ASYNC

        return mode

    @staticmethod
    def get_inter_path(skill, mode):
        if LanguageSkill.is_conversational(skill):
            return conversation_inter_paths[mode]
        else:
            return document_inter_paths[mode]


def get_max_sync_chars(skill):
    return MAX_SYNC_CHARS


skill_to_str = {
    LanguageSkill.CUSTOM_TEXT_CLASSIFICATION: "CustomSingleLabelClassification"
}

skill_to_conversational = {
    LanguageSkill.CUSTOM_TEXT_CLASSIFICATION: False
}

skill_to_async_capabilities = {
    LanguageSkill.CUSTOM_TEXT_CLASSIFICATION: True
}

skill_to_default_mode = {
    LanguageSkill.CUSTOM_TEXT_CLASSIFICATION: LanguageMode.ASYNC
}

document_inter_paths = {
    LanguageMode.SYNC: "/language/:analyze-text",
    LanguageMode.ASYNC: "/language/analyze-text/jobs"
}

conversation_inter_paths = {
    LanguageMode.SYNC: "/language/:analyze-conversations",
    LanguageMode.ASYNC: "/language/analyze-conversations/jobs"
}
