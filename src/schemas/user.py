from pydantic import EmailStr, BaseModel


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
