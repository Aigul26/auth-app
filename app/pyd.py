from pydantic import BaseModel, Field, field_validator
import re


class UserBase(BaseModel):
    phone: str = Field(..., max_length=12, examples=['+79876543210'])
    firstname: str = Field(..., examples=['Ivan'])
    lastname: str = Field(..., examples=['Ivanov'])


    @field_validator('phone')
    def validate_phone_format(cls, value):
        if not re.match(r'^\+7\d{10}$', value):
            raise ValueError('Номер телефона должен быть в формате +79876543210')
        return value