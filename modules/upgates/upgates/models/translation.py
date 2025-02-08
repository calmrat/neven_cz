# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
/Users/cward/Repos/neven_cz/modules/upgates/upgates/models/translation.py

This module defines the data models for translation requests and responses using Pydantic.

Classes:
    TranslationRequest: Model for a translation request containing product ID, source language, target language, and fields to be translated.
    TranslationResponse: Model for a translation response containing product ID and translated data.

Usage example:

    request = TranslationRequest(
        product_id=123,
        source_lang="en",
        target_lang="fr",
        fields=["name", "description"]
    )

    response = TranslationResponse(
        product_id=123,
        translated_data={"name": "Nom", "description": "Description"}
    )
"""

from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):  # noqa: F811
    product_id: int = Field(..., description="ID of the product to be translated")
    source_lang: str = Field(..., description="Source language code")
    target_lang: str = Field(..., description="Target language code")
    fields: list[str] = Field(..., description="List of fields to be translated")

class TranslationResponse(BaseModel):  # noqa: F811
    product_id: int = Field(..., description="ID of the product that was translated")
    translated_data: dict[str, str] = Field(..., description="Dictionary containing translated data")

__all__ = ["TranslationRequest", "TranslationResponse"]

# EOF