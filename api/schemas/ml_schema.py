# api/schemas/ml_schema.py
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class TrainResponse(BaseModel):
    message: str
    accuracy: float
    model_path: str

class IrisDataPoint(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    target: int  # 0, 1 ou 2 (setosa, versicolor, virginica)
    target_name: str # Opcional: para ficar mais legível (ex: "setosa")

class TrainingDataResponse(BaseModel):
    data: List[IrisDataPoint]
    total_samples: int

class PredictionInput(BaseModel):
    sepal_length: float = Field(..., example=5.1, description="Comprimento da sépala (cm)")
    sepal_width: float = Field(..., example=3.5, description="Largura da sépala (cm)")
    petal_length: float = Field(..., example=1.4, description="Comprimento da pétala (cm)")
    petal_width: float = Field(..., example=0.2, description="Largura da pétala (cm)")

class PredictionResponse(BaseModel):
    predicted_class: int
    predicted_label: str
    probability: float = None # Opcional: Para mostrar a confiança do modelo

class FeatureLogResponse(BaseModel):
    id: int
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    predicted_label: str
    created_at: datetime

    class Config:
        from_attributes = True