from pydantic import BaseModel, Field
from typing import Optional, Dict


class BookPriceFeatures(BaseModel):
    rating: Optional[int] = Field(default=None, ge=0, le=5)
    quantity: int = Field(default=0, ge=0)
    availability: bool
    category_id: int = Field(ge=1)


class BookPriceTrainingSample(BookPriceFeatures):
    target_price: float


class BookPriceTrainResponse(BaseModel):
    status: str
    model_path: str
    train_size: int
    test_size: int
    metrics: Dict[str, float]

class BookPricePredictionResponse(BaseModel):
    predicted_price: float
