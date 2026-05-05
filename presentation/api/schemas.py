#Define como entra y sale la información
from pydantic import BaseModel, Field
from typing import List, Optional

#prediccion
class PredictRequest(BaseModel):
    l: List[float] = Field(..., min_items=63, max_items=63)

class PredictResponse(BaseModel):
    l: Optional[str]
    c: float

#guardar ejemplo
class SaveExampleRequest(BaseModel):
    letter: str
    landmrks: List[float] = Field(..., min_items=63, max_items=63)

#batch(entrenamiento)

class BatchItem(BaseModel):
    letter: str
    landmarks: List[float]

class BatchResponse(BaseModel):
    saved: int

#dataset info

class DatasetInfoResponse(BaseModel):
    samples: int