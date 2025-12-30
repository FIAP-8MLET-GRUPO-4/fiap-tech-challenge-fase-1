from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from api.core.db import Base

class PredictionLog(Base):
    __tablename__ = 'prediction_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # As Features (Entradas)
    sepal_length = Column(Float, nullable=False)
    sepal_width = Column(Float, nullable=False)
    petal_length = Column(Float, nullable=False)
    petal_width = Column(Float, nullable=False)
    
    # O Resultado (Saída)
    predicted_class = Column(Integer, nullable=False)
    predicted_label = Column(String(50), nullable=False)
    probability = Column(Float)
    
    # Metadados
    created_at = Column(DateTime, default=datetime.now)