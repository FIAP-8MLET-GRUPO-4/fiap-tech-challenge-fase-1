# api/services/ml_service.py
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import logging
import os
import numpy as np
from sqlalchemy.orm import Session
from api.models.prediction_log import PredictionLog

logger = logging.getLogger(__name__)

MODEL_PATH = "model_iris.pkl"

def get_iris_training_data():
    """
    Carrega o dataset Iris do Scikit-Learn e formata para JSON.
    """
    try:
        # Carrega o dataset nativo do sklearn
        iris = load_iris()
        X = iris.data
        y = iris.target
        target_names = iris.target_names
        feature_names = iris.feature_names # ['sepal length (cm)', ...]

        formatted_data = []

        # Itera sobre os dados e monta a lista de objetos
        for i in range(len(X)):
            formatted_data.append({
                # Mapeando os índices 0,1,2,3 para nomes amigáveis
                "sepal_length": X[i][0],
                "sepal_width": X[i][1],
                "petal_length": X[i][2],
                "petal_width": X[i][3],
                "target": int(y[i]),
                "target_name": str(target_names[y[i]])
            })
            
        logger.info(f"Dataset Iris carregado: {len(formatted_data)} registros.")
        
        return {
            "data": formatted_data,
            "total_samples": len(formatted_data)
        }

    except Exception as e:
        logger.error(f"Erro ao carregar dataset Iris: {e}")
        return {"data": [], "total_samples": 0}
    
def train_model():
    """
    Executa o pipeline de treinamento:
    1. Carrega dados
    2. Split Train/Test
    3. Fit do Modelo (Logistic Regression)
    4. Avaliação
    5. Salva o .pkl
    """
    logger.info("Iniciando treinamento do modelo...")
    try:
        # 1. Carregar Dados
        data = load_iris()
        X, y = data.data, data.target
        
        # 2. Split 
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # 3. Treinar
        model = LogisticRegression(max_iter=200, random_state=42)
        model.fit(X_train, y_train)
        
        # 4. Avaliar
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        # 5. Salvar (Pickle)
        joblib.dump(model, MODEL_PATH)
        
        logger.info(f"Modelo treinado com sucesso! Acurácia: {accuracy}")
        
        return {
            "message": "Modelo treinado e salvo com sucesso.",
            "accuracy": accuracy,
            "model_path": MODEL_PATH
        }
        
    except Exception as e:
        logger.error(f"Erro no treinamento: {e}")
        raise e
    
def predict_single(sepal_length, sepal_width, petal_length, petal_width, db: Session):
    """
    Carrega o modelo salvo e faz a predição para um único registro.
    """
    # 1. Verificar se o modelo existe
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Modelo não encontrado. Execute o endpoint /train-model primeiro.")

    try:
        # 2. Carregar o Modelo
        # Em produção de alta escala, carregaríamos isso na memória global no startup do app
        # para não ler disco a cada request. Mas para este MVP, ler aqui é seguro.
        model = joblib.load(MODEL_PATH)
        
        # 3. Preparar os dados (O sklearn espera uma matriz 2D: [[v1, v2, v3, v4]])
        input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        
        # 4. Predizer
        prediction = model.predict(input_data)[0] # Pega o primeiro (e único) item
        
        # Opcional: Pegar probabilidades (confiança)
        # model.predict_proba retorna algo como [[0.9, 0.05, 0.05]]
        probs = model.predict_proba(input_data)[0]
        confidence = float(max(probs))
        
        # 5. Mapear número para nome (0 -> setosa, etc)
        # O Iris tem nomes fixos, podemos hardcodar ou carregar do dataset
        target_names = ['setosa', 'versicolor', 'virginica']
        label = target_names[int(prediction)]
        
        log_entry = PredictionLog(
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width,
            predicted_class=int(prediction),
            predicted_label=label,
            probability=confidence
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry) # Para pegar o ID gerado e o created_at
        
        return {
            "predicted_class": int(prediction),
            "predicted_label": label,
            "probability": round(confidence, 4)
        }

    except Exception as e:
        logger.error(f"Erro na predição: {e}")
        db.rollback()
        raise e

def list_features_history(db: Session, limit: int = 100):
    """
    Retorna o histórico de features enviadas para o modelo.
    """
    return db.query(PredictionLog).order_by(PredictionLog.created_at.desc()).limit(limit).all()