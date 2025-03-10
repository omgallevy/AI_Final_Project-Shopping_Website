from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    phone: int
    city: str
    country: str
    password: str
