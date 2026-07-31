from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.enums import UserRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.FARMER


class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
