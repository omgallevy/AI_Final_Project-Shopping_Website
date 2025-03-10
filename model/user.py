from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    phone: int
    address: str
    hashed_password: str
