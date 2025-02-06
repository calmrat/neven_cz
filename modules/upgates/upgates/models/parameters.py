
from pydantic import BaseModel

class Parameter(BaseModel):
    key: str
    value: str
