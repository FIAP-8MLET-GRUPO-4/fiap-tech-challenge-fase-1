from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.core.db import get_db
from api.schemas.ml_schema_books import BookPriceFeatures, BookPricePredictionResponse, BookPriceTrainingSample
from api.services.ml_service_books import train_price_model, predict_price, get_book_features, get_training_data_price

router = APIRouter()

@router.get("/features", response_model=list[BookPriceFeatures])
def features(db: Session = Depends(get_db)):
    return get_book_features(db)

@router.get("/training-data", response_model=list[BookPriceTrainingSample])
def training_data(db: Session = Depends(get_db)):
    return get_training_data_price(db)

@router.post("/train-model")
def train_model(db: Session = Depends(get_db)):
    try:
        return train_price_model(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predictions", response_model=BookPricePredictionResponse)
def predictions(payload: BookPriceFeatures):
    try:
        return predict_price(payload.model_dump())
    except FileNotFoundError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))