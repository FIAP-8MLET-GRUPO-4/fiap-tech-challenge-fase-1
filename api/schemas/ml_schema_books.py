from pydantic import BaseModel, ConfigDict
from typing import Optional


class BookPriceFeatures(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rating: Optional[int] = None
    quantity: int
    availability: bool
    category_id: int


class BookPriceTrainingSample(BookPriceFeatures):
    target_price: float


class BookPricePredictionResponse(BaseModel):
    target_price: float