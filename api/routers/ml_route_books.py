from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.core.db import get_db
from api.schemas.ml_schema_books import (
    BookPriceFeatures,
    BookPricePredictionResponse,
    BookPriceTrainingSample,
    BookPriceTrainResponse,
)

from api.services.ml_service_books import (
    NoValidBooksError,
    train_price_model,
    predict_price,
    get_book_features,
    get_training_data_price
)

router = APIRouter()


@router.get(
    "/features",
    response_model=List[BookPriceFeatures],
    responses={
        200: {"description": "Features geradas com sucesso"},
        404: {"description": "Nenhum livro válido encontrado"},
        500: {"description": "Erro interno ao gerar features"},
    },
)
def features(db: Session = Depends(get_db)):
    try:
        return get_book_features(db)
    except NoValidBooksError:
        raise HTTPException(
            status_code=404,
            detail="Nenhum livro válido encontrado para gerar features."
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro inesperado ao gerar features."
        )

@router.get(
    "/training-data",
    response_model=List[BookPriceTrainingSample], 
    summary="Dados rotulados para treino do modelo",
    responses={
        200: {"description": "Dados retornados com sucesso"},
        404: {"description": "Nenhum dado válido para treino"},
        500: {"description": "Erro interno"},
    },
)
def training_data(db: Session = Depends(get_db)):
    try:
        return get_training_data_price(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/train-model", 
    response_model=BookPriceTrainResponse,
    responses={
        200: {"description": "Modelo treinado com sucesso"},
        400: {"description": "Dados insuficientes para treino"},
        500: {"description": "Erro interno"},
    },
)
def train_model(db: Session = Depends(get_db)):
    try:
        return train_price_model(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao treinar modelo.")


@router.post(
    "/predictions",
    response_model=BookPricePredictionResponse,
    responses={
        200: {"description": "Dados retornados com sucesso"},
        404: {"description": "Nenhum dado válido para treino"},
        500: {"description": "Erro interno"},
    },
)
def predictions(payload: BookPriceFeatures):
    try:
        return predict_price(payload.model_dump())

    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar predição: {str(e)}"
        )
        