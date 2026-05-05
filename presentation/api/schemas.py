#Define como entra y sale la información
from pydantic import BaseModel, Field
from typing import List, Optional

#prediccion
class PredictResquest(BaseModel):
    l: List[float] = Field(..., min_items=63, max_items=63)

class PredictResponse(BaseModel):
    l: Optional[str]
    c: float

#guardar ejemplo
class SaveExampleRquest(BaseModel):
    letter: str
    landmrks: List[float] = Field(..., min_items=63, max_items=63)

