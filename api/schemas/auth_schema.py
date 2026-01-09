# api/schemas/auth_schema.py
from pydantic import BaseModel

class LoginInput(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshInput(BaseModel):
    refresh_token: str