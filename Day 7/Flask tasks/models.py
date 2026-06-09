from pydantic import BaseModel, Field
from uuid import uuid4

class PredictionRequest(BaseModel):
    age: int = Field(gt=0)
    salary: float = Field(gt=0)

class PredictionResponse(BaseModel):
    id: str
    prediction: str