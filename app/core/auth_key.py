from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError

from app.config import settings

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