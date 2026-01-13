import os
import joblib
import pandas as pd
from sqlalchemy.orm import Session

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

from api.models.books import Book

MODEL_PATH = os.path.join("api", "ml_models", "model_books_price.joblib")

FEATURE_COLS = ["rating", "quantity", "availability", "category_id"]
TARGET_COL = "target_price"

def get_book_features(db: Session):
    books = db.query(Book).all()
    out = []
    for b in books:
        if b.category_id is None or b.price is None:
            continue
        out.append({
            "rating": b.rating,
            "quantity": b.quantity if b.quantity is not None else 0,
            "availability": bool(b.availability),
            "category_id": b.category_id,
        })
    return out

def get_training_data_price(db: Session):
    books = db.query(Book).all()
    rows = []
    for b in books:
        if b.category_id is None or b.price is None:
            continue
        rows.append({
            "rating": int(b.rating) if b.rating is not None else None,
            "quantity": int(b.quantity) if b.quantity is not None else 0,
            "availability": bool(b.availability) if b.availability is not None else False,
            "category_id": int(b.category_id),
            "target_price": float(b.price),
        })
    return rows

def _to_rows(books):
    rows = []
    for b in books:
        if b.price is None:
            continue

        rows.append({
            "rating": int(b.rating) if b.rating is not None else None,
            "quantity": int(b.quantity) if b.quantity is not None else 0,
            "availability": bool(b.availability) if b.availability is not None else False,
            "category_id": int(b.category_id) if b.category_id is not None else None,
            "price": float(b.price),
        })
    return rows

def train_price_model(db: Session):
    rows = get_training_data_price(db)
    df = pd.DataFrame(rows)
    df["availability"] = df["availability"].astype(int)

    if df.empty or len(df) < 30:
        raise ValueError(f"Poucos dados para treino: {len(df)} linhas. Rode o scraper e alimente o DB.")

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    numeric_features = ["rating", "quantity"]
    bool_features = ["availability"]
    cat_features = ["category_id"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
            ]), numeric_features),

            ("bool", Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
            ]), bool_features),

            ("cat", Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]), cat_features),
        ]
    )

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1
        )),
    ])

    model.fit(X_train, y_train)

    # métricas do treino
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return {
        "status": "trained",
        "model_path": MODEL_PATH,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "metrics": {"mae": float(mae), "rmse": float(rmse), "r2": float(r2)},
    }

def load_price_model():
    """Carrega modelo salvo; se não existir, apresenta um erro."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Modelo não encontrado. Rode POST /api/v1/ml/books/train-model para treinar e salvar."
        )
    return joblib.load(MODEL_PATH)

def predict_price(payload_dict: dict):
    model = load_price_model()

    X = pd.DataFrame([payload_dict])

    # garante colunas e tipos esperados
    X = X[FEATURE_COLS].copy()
    X["availability"] = X["availability"].astype(int)
    X["category_id"] = X["category_id"].astype(int)

    pred = float(model.predict(X)[0])
    return {"target_price": max(0.0, pred)}



