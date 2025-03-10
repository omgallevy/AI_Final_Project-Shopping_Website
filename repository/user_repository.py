import json
from typing import Optional, List

from model.user import User
from model.user_request import UserRequest
from model.user_response import UserResponse
from repository.database import database
from service import user_service

TABLE_NAME = "users"


async def get_by_username(username: str) -> Optional[User]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE username=:username"
    result = await database.fetch_one(query, {"username": username})
    if result:
        return User(**result)
    else:
        return None


async def get_by_id(user_id: int) -> Optional[User]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE id=:user_id"
    result = await database.fetch_one(query, values={"user_id": user_id})
    if result:
        return User(**result)
    else:
        return None


async def create_user(user: UserRequest, hashed_password: str):
    query_user = f"""
           INSERT INTO {TABLE_NAME} 
           (username, first_name, last_name, email, phone, address, hashed_password)
           VALUES (:username, :first_name, :last_name, :email, :phone, :address, :hashed_password)
       """

    address_dict = {"city": user.city, "country": user.country}
    address = json.dumps(address_dict)

    user_dict = user.dict()
    del user_dict["password"]
    del user_dict["city"]
    del user_dict["country"]
    values_user = {**user_dict, "address": address, "hashed_password": hashed_password}

    async with database.transaction():
        await database.execute(query_user, values_user)
        user_id = await database.fetch_one("SELECT LAST_INSERT_ID()")

    user = UserResponse(
        id=user_id[0],
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        city=user.city,
        country=user.country
    )

    return user


async def update_user(user_id: int, user: UserRequest):
    query = f"""
        UPDATE {TABLE_NAME}
        SET username = :username,
            first_name = :first_name,
            last_name = :last_name,
            email = :email,
            phone = :phone,
            city = :city,
            country = :country,
            password = COALESCE(:password, password)
        WHERE id = :user_id
    """
    password_hash = user_service.get_password_hash(user.password) if user.password else None

    values = {
        "user_id": user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "city": user.city,
        "country": user.country,
        "password": password_hash
    }
    await database.execute(query, values=values)


async def delete_user_and_related_data(user_id: int):
    async with database.transaction():
        favorite_items_query = "DELETE FROM favorite_item WHERE user_id = :user_id"
        await database.execute(favorite_items_query, values={"user_id": user_id})

        order_items_query = "DELETE FROM order_item WHERE user_id = :user_id"
        await database.execute(order_items_query, values={"user_id": user_id})

        orders_query = "DELETE FROM orders WHERE user_id = :user_id"
        await database.execute(orders_query, values={"user_id": user_id})

        users_query = "DELETE FROM users WHERE id = :user_id"
        await database.execute(users_query, values={"user_id": user_id})


async def get_users() -> List[User]:
    query = f"SELECT * FROM {TABLE_NAME}"
    results = await database.fetch_all(query)
    return [User(**result) for result in results]
