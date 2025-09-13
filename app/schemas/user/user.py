from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)