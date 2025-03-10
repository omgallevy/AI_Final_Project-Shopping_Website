from fastapi.security import OAuth2PasswordBearer
from starlette import status

from model.user_request import UserRequest
from fastapi import APIRouter, Depends, HTTPException

from service import auth_service
from service import user_service
from exceptions.security_exceptions import token_exception

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={401: {"user": "Not authorized"}}
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    return await user_service.get_user_by_id(user_response.id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: UserRequest):
    user = await user_service.create_user(user_request)
    return user


@router.put("/{user_id}")
async def update_user(user_id: int, user: UserRequest):
    existing_user = await user_service.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"Can't update user with id: {user_id}, user not found")

    await user_service.update_user(user_id, user)
    updated_user = await user_service.get_user_by_id(user_id)
    return updated_user


@router.delete("/delete/{user_id}", status_code=204)
async def delete_user(token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    if user is None:
        raise token_exception()
    await user_service.delete_user(user.id)


@router.delete("/delete/{username}", status_code=204)
async def delete_user_by_username(username: str, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    if user is None:
        raise token_exception()
    await user_service.delete_user_by_username(username)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    return await user_service.get_users()


@router.get("/user/{username}")
async def get_user_by_username(username: str, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    if user.username != username:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return user

