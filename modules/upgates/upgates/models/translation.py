
from pydantic import BaseModel

class TranslationRequest(BaseModel):
    product_id: int
    source_lang: str
    target_lang: str
    fields: list[str]

class TranslationResponse(BaseModel):
    product_id: int
    translated_data: dict[str, str]
