from pydantic import BaseModel
from typing import Optional

class BookPriceFeatures(BaseModel):
    rating: Optional[int] = None
    quantity: int
    availability: bool
    category_id: int

class BookPriceTrainingSample(BookPriceFeatures):
    target_price: float

class BookPricePredictionResponse(BaseModel):
    target_price: float