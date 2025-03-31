#!/usr/bin/env python3
"""
upgates/pydantic_ai.py v0.4.1
File: upgates/pydantic_ai.py

This module uses the official pydantic_ai.Agent to implement the AI translation
functionality. It defines a structured TranslationResult model and TranslationDeps
for dependency injection, and instantiates an Agent with a static system prompt.
The async function translate_text() runs the agent and returns the validated data.
"""

import os
from dataclasses import dataclass

import logfire
from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent, ModelRetry, RunContext

from upgates import config

# Ensure OpenAI API key is loaded in environment
if config.openai_enabled:
    # Ensure OpenAI API key is loaded in environment
    os.environ["OPENAI_API_KEY"] = config.openai_api_key
    agent_retry_count = int(config.openai_default_retries) or 1
else:
    raise NotImplementedError("OpenAI API key is required for translation.")


# #FIXME: load from config
valid_target_languages = ("cz", "cs", "sk", "en")


# Define the result model for translation.
class TranslationResult(BaseModel):
    target_language: str = Field(
        ..., description="The target language for translation.", title="Target Language"
    )
    title: str = Field(
        ..., description="The optimized product title.", title="Optimized Title"
    )
    short_description: str = Field(
        ..., description="A concise product description.", title="Short Description"
    )
    long_description: str = Field(
        ...,
        description="The translated and optimized long description.",
        title="Translated Long Description",
    )
    seo_description: str = Field(
        ...,
        description="SEO-friendly description for the product.",
        title="SEO Description",
    )
    seo_title: str = Field(
        ..., description="SEO-friendly title for the product.", title="SEO Title"
    )
    seo_keywords: str = Field(
        ...,
        description="REQUIRED: SEO-friendly list (csv) of keywords for the product.",
        title="SEO Keywords",
    )
    seo_url: str = Field(
        ...,
        description="SEO-friendly (relative page) URL for the product.",
        title="SEO URL",
    )
    unit: str = Field(
        ...,
        description="The unit of measurement for the product. (default 'ks' if unsure)",
        title="Unit",
    )
    error: str = Field(
        ...,
        description="Error message if transformation failed or empty.",
        title="Error",
    )
    return_code: int = Field(
        0,
        description="Return status code. [200 SUCCESS, 400 ERROR]",
        title="Error Code",
    )

    @staticmethod
    def migrate_language_code(value: str) -> str:
        """
        Updates.cz uses 'cz' instead of 'cs' for Czech language.
        Migrate language codes to new format.
        """
        logfire.info(f"migrate_language_code: {value}")
        value = str(value).strip().lower()
        value = "cz" if value == "cs" else value
        return value

    @field_validator("target_language", mode="after")
    @classmethod
    def is_valid_target_language(cls, value: str) -> str:
        logfire.info(f"is_valid_target_language: {value}")
        value = str(value).strip().lower()
        value = cls.migrate_language_code(value)
        # import ipdb; ipdb.set_trace()
        if value not in valid_target_languages:
            raise ValueError(
                f"❌ {value} is not a valid target language. Expecting: {valid_target_languages}"
            )
        return value


# Define the dependency dataclass for translation.
@dataclass
class TranslationDeps:
    """Translation dependencies"""

    valid_target_languages: tuple | list = valid_target_languages


# Update the agent to use the default model from config
target_model = config.openai_default_model

system_prompt = """
    You are a multi-lingual translator.
    * Some product names are in English, and they are not intended to be translated.
    * You remain true to the original technical meaning of the text, but your tone is nuanced for the target language.
    * You offer metric, imperial, US measurements for products, when relevant.
    
    Special instructions for "Long Description" field:
    * clean HTML, with only: p, span, h2, h3, h4, b, i, em, strong, img, table, ul, ol, li, br
    * No inline styles, no inline scripts, no inline JS.
    * No <center> tags. Clean up empty and invalid tags.
    * <img>: Set width to 600px, if larger than this max size. Remove img height attribute.
    * Add accessibility tags (alt).
    """.strip()

# Instantiate the Translator Agent
agent_translator = Agent(
    target_model,
    result_type=TranslationResult,
    deps_type=TranslationDeps,
    system_prompt=system_prompt,
    retries=agent_retry_count,
)


@agent_translator.result_validator
async def validate_target_language(
    ctx: RunContext[TranslationDeps], result: TranslationResult
) -> TranslationResult:
    """Validate the translation result"""
    logfire.info(f"validate_target_language: {result.target_language}")
    if result.target_language not in ctx.deps.valid_target_languages:
        raise ModelRetry(
            f"Invalid Target Language: {result.target_language}. Expected: {valid_target_languages}"
        )
    return result


@agent_translator.result_validator
async def validate_fields_are_not_empty(
    ctx: RunContext[TranslationDeps], result: TranslationResult
) -> TranslationResult:
    """Validate that our main fields are not empty"""
    logfire.info(f"validate_fields_are_not_empty: {result}")
    if "" in (
        x.strip()
        for x in (
            result.target_language,
            result.title,
            result.short_description,
            result.long_description,
            result.seo_description,
            result.seo_title,
            result.seo_keywords,
            result.seo_url,
            result.unit,
        )
    ):
        raise ModelRetry(f"No values should be empty! Got {result}")
    return result


async def translate_text(user_prompt: str, deps: TranslationDeps) -> TranslationResult:
    """
    Asynchronously translates text using the official pydantic_ai.Agent.
    The agent sends the system prompt along with the user prompt to the LLM.
    Returns:
        A dictionary containing the validated translation result.
    """
    result = await agent_translator.run(user_prompt, deps=deps)
    return result.data


all_agents = [agent_translator]

# EOF
