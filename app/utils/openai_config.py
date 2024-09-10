from enum import Enum


class OpenAIModels(str, Enum):
    GPT3_TURBO = "gpt-3.5-turbo"
    GPT4 = "gpt-4",
    GPT4o = "gpt-4o",
    GPT4o_MINI = "gpt-4o-mini",
    TEXT_EMB_3_SMALL = "text-embedding-3-small"


MODEL_TOKEN_LIMITS = {
    OpenAIModels.GPT3_TURBO: 4_096,
    OpenAIModels.GPT4: 8_192
}
