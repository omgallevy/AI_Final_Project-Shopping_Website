import json
from typing import Optional, List

from fastapi import HTTPException
from passlib.context import CryptContext

from exceptions.security_exceptions import username_taken_exception
from model.user import User
from model.user_request import UserRequest
from model.user_response import UserResponse
from repository import user_repository

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


async def get_user_by_username(username: str) -> User:
    return await user_repository.get_by_username(username)


async def create_user(user_request: UserRequest):
    if not await validate_unique_username(user_request.username):
        raise username_taken_exception()

    hashed_password = get_password_hash(user_request.password)
    user = await user_repository.create_user(user_request, hashed_password)

    return user


async def get_user_by_id(user_id: int) -> Optional[UserResponse]:
    user = await user_repository.get_by_id(user_id)
    if user:
        address = json.loads(user.address)
        return UserResponse(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            city=address["city"],
            country=address["country"],
            password=user.hashed_password
        )
    else:
        return None


async def update_user(user_id: int, user: UserRequest) -> UserResponse:
    existing_user = await user_repository.get_by_id(user_id)
    if existing_user is None:
        raise Exception(f"Can't update user with id {user_id}, id is not existing")

    if user.password:
        if not verify_password(user.old_password, existing_user.password):
            raise Exception("The old password does not match")
        user.password = get_password_hash(user.password)

    await user_repository.update_user(user_id, user)

    return await user_repository.get_by_id(user_id)


async def delete_user(user_id: int):
    user = await user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    await user_repository.delete_user_and_related_data(user_id)


async def delete_user_by_username(username: str):
    user = await user_repository.get_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="משתמש לא נמצא")
    await user_repository.delete_user_and_related_data(user.id)


async def validate_unique_username(username: str) -> bool:
    existing_user = await user_repository.get_by_username(username)
    return existing_user is None


async def get_users() -> List[UserResponse]:
    users = await user_repository.get_users()
    return [UserResponse(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    ) for user in users]
