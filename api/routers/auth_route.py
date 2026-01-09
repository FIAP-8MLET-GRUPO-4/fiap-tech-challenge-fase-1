# api/routers/auth_route.py
from fastapi import APIRouter, Depends, HTTPException, status
#from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.core.db import get_db
from api.models.users import User
from api.core.security import verify_password, create_access_token, create_refresh_token, decode_token, get_password_hash
from api.schemas.auth_schema import TokenResponse, RefreshInput, LoginInput

router = APIRouter()

# @router.post("/login", response_model=TokenResponse)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     """
#     Recebe username e password (via Form Data compatível com Swagger) e retorna tokens.
#     """
#     # O form_data tem os campos .username e .password automaticamente
#     user = db.query(User).filter(User.username == form_data.username).first()
    
#     if not user or not verify_password(form_data.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Username ou senha incorretos"
#         )
        
#     access_token = create_access_token(subject=user.username)
#     refresh_token = create_refresh_token(subject=user.username)
    
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer"
#     }

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginInput, db: Session = Depends(get_db)):
    """
    Recebe username e password, valida no banco e retorna tokens.
    """
    # 1. Buscar usuário
    user = db.query(User).filter(User.username == login_data.username).first()
    
    # 2. Verificar senha (Hash vs Texto)
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos"
        )
        
    # 3. Gerar Tokens
    access_token = create_access_token(subject=user.username)
    refresh_token = create_refresh_token(subject=user.username)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(input_data: RefreshInput):
    """
    Gera um novo access_token usando um refresh_token válido.
    """
    decoded = decode_token(input_data.refresh_token)
    
    if not decoded or decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")
        
    username = decoded.get("sub")
    
    # Gera novos tokens
    new_access_token = create_access_token(subject=username)
    
    # Rotacionar o refresh token também (mais seguro)
    new_refresh_token = create_refresh_token(subject=username)
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

# Rota auxiliar APENAS PARA DESENVOLVIMENTO (Criar o primeiro usuário)
@router.post("/register-admin")
def create_admin_user(login_data: LoginInput, db: Session = Depends(get_db)):
    """Rota temporária para criar um usuário com senha hashada"""
    existing = db.query(User).filter(User.username == login_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        username=login_data.username,
        password=get_password_hash(login_data.password) 
    )
    db.add(new_user)
    db.commit()
    return {"msg": "Admin criado com sucesso"}