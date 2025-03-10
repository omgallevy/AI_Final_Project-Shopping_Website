from datetime import timedelta, datetime
from jose import jwt, JWTError
from exceptions.security_exceptions import token_exception
from config.config import Config
from model.auth_response import AuthResponse

from service import user_service

config = Config()


async def authenticate_user(username: str, password: str):
    user = await user_service.get_user_by_username(username)
    if not user or not user_service.verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int) -> AuthResponse:
    user_data = {"subject": username, "id": user_id}
    token_expire = datetime.utcnow() + timedelta(minutes=config.TOKEN_EXPIRY_TIME)
    user_data.update({"exp": token_expire})
    token = jwt.encode(user_data, config.SECRET_KEY, config.ALGORITHM)
    return AuthResponse(jwt_token=token)


async def validate_user(token: str):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("subject")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise token_exception()
        else:
            return await user_service.get_user_by_id(user_id)
    except JWTError:
        raise token_exception()
