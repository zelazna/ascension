import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel  # type: ignore


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    username: str = Field(max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)
    username: str = Field(default=None, max_length=255)


class UserUpdateMe(SQLModel):
    username: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    # items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
# class ItemBase(SQLModel):
#     title: str = Field(min_length=1, max_length=255)
#     description: str | None = Field(default=None, max_length=255)


# # Properties to receive on item creation
# class ItemCreate(ItemBase):
#     pass


# # Properties to receive on item update
# class ItemUpdate(ItemBase):
#     title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# # Database model, database table inferred from class name
# class Item(ItemBase, table=True):
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     title: str = Field(max_length=255)
#     owner_id: uuid.UUID = Field(
#         foreign_key="user.id", nullable=False, ondelete="CASCADE"
#     )
#     owner: User | None = Relationship(back_populates="items")


# # Properties to return via API, id is always required
# class ItemPublic(ItemBase):
#     id: uuid.UUID
#     owner_id: uuid.UUID


# class ItemsPublic(SQLModel):
#     data: list[ItemPublic]
#     count: int


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
