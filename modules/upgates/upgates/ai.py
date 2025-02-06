#!/usr/bin/env python3
"""
upgates/pydantic_ai.py v0.4.1
File: upgates/pydantic_ai.py

This module uses the official pydantic_ai.Agent to implement the AI translation
functionality. It defines a structured TranslationResult model and TranslationDeps
for dependency injection, and instantiates an Agent with a static system prompt.
The async function translate_text() runs the agent and returns the validated data.
"""

#import asyncio

from datetime import datetime
from dataclasses import dataclass
import os
#import toml

import logfire
from pydantic import BaseModel, Field
from pydantic_ai import Agent

from upgates.config import config

# Ensure OpenAI API key is loaded in environment
if config['openai']['enabled']:
    os.environ['OPENAI_API_KEY'] = config['openai']['api_key']
else:
    raise NotImplementedError("OpenAI API key is required for translation.")

# Update the agent to use the default model from config
target_model = config['openai']['default_model']

# Define the result model for translation.
class TranslationResult(BaseModel):
    target_language: str = Field(..., description="The target language for translation.", title="Target Language")
    title: str = Field(..., description="The optimized product title.", title="Optimized Title")
    short_description: str = Field(..., description="A concise product description.", title="Short Description")
    long_description: str = Field(..., description="The translated and optimized long description.", title="Translated Long Description")
    seo_description: str = Field(..., description="SEO-friendly description for the product.", title="SEO Description")
    seo_title: str = Field(..., description="SEO-friendly title for the product.", title="SEO Title")
    seo_keywords: list = Field(..., description="SEO-friendly keywords for the product.", title="SEO Keywords")
    seo_url: str = Field(..., description="SEO-friendly (relative page) URL for the product.", title="SEO URL")
    unit: str = Field(..., description="The unit of measurement for the product. (default 'ks' if unsure)", title="Unit")
    error: str = Field("", description="Error message if transformation failed.", title="Error")
    error_code: int = Field(0, description="Error code if transformation failed. 200 OK, 400 ERROR", title="Error Code")
    #today_datetime: datetime = Field(..., description="Today's datetime as an ISO string.", title="Today's Datetime")

# Define the dependency dataclass for translation.
@dataclass
class TranslationDeps:
   ''' Translation dependencies '''
   #today_datetime_str: str
   pass

def get_today_datetime() -> datetime:
    """
    Returns today's datetime.
    """
    #logfire.debug("Getting today's datetime.")
    return datetime.now()


# Instantiate the official pydantic_ai.Agent.
agent = Agent(
    target_model,
    result_type=TranslationResult,
    deps_type=TranslationDeps,
    system_prompt=(
        "You are a multi-lingual translator and an clean html expert, originally from Czech Republic."
    ),
    #tools=[get_today_datetime],
    retries=5,
)

async def translate_text(prompt: str, deps: TranslationDeps) -> TranslationResult:
    """
    Asynchronously translates text using the official pydantic_ai.Agent.
    The agent sends the system prompt along with the user prompt to the LLM.
    Returns:
        A dictionary containing the validated translation result.
    """
    result = await agent.run(prompt, deps=deps)
    return result.data

# End of upgates/pydantic_ai.py v0.4.1