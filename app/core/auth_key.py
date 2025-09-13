from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.session import get_db
from app.crud.user.user_crud import UserCRUD

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def generate_access_token(payload: dict) -> str:
    return encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def vefiry_access_token(token: str) -> dict:
    try:
        decoded = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded
    
    except ExpiredSignatureError:
        raise ValueError("Токен истёк")
    
    except InvalidTokenError:
        raise ValueError("Неверный токен")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = vefiry_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = await UserCRUD.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user