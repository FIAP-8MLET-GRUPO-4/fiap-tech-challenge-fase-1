# api/core/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from api.core.db import get_db
from api.core.security import decode_token
from api.models.users import User

bearer_scheme = HTTPBearer()

def get_current_user(credentials=Depends(bearer_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_token(token)

    print("PAYLOAD:", payload)

    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()

    print("USER FOUND:", bool(user), "USERNAME:", username)

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user