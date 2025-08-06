from pydantic import BaseModel


class Comments(BaseModel):
    id: int
    texto: str

    class Config:
        extra = "forbid"


class Credentials(BaseModel):
    username: str
    password: str

    class Config:
        extra = "forbid"
