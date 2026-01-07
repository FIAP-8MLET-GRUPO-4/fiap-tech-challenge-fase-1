# api/routers/ml_route.py
from fastapi import APIRouter, HTTPException, Depends
from api.services.ml_service import get_iris_training_data, train_model, predict_single, list_features_history
from api.schemas.ml_schema import TrainingDataResponse, TrainResponse, PredictionInput, PredictionResponse, FeatureLogResponse
from sqlalchemy.orm import Session
from typing import List
from api.core.db import get_db

router = APIRouter()


@router.get("/training-data", response_model=TrainingDataResponse)
def get_training_data():
    """
    Retorna o dataset Iris completo formatado para treinamento.
    Fonte: Scikit-Learn load_iris()
    """
    return get_iris_training_data()


@router.post("/train-model", response_model=TrainResponse)
def train_model_endpoint():
    """
    Dispara o retreinamento do modelo com os dados atuais
    e salva o arquivo .pkl no servidor.
    """
    try:
        result = train_model()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha no treinamento: {str(e)}")


@router.post("/predictions", response_model=PredictionResponse)
def predict_flower(input_data: PredictionInput, db: Session = Depends(get_db)):
    """
    Recebe as medidas de uma flor Iris, retorna a espécie prevista pelo modelo e salva o log no banco de dados.
    """
    try:
        result = predict_single(
            input_data.sepal_length,
            input_data.sepal_width,
            input_data.petal_length,
            input_data.petal_width,
            db
        )
        return result
        
    except FileNotFoundError as e:
        # Retorna 400 Bad Request se o modelo ainda não foi treinado
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar predição: {str(e)}")
    
@router.get("/features", response_model=List[FeatureLogResponse])
def get_features_history(db: Session = Depends(get_db)):
    """
    Retorna o histórico de features (dados de entrada) submetidos à API de predição.    
    """
    return list_features_history(db)