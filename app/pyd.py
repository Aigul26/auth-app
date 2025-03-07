from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    phone: str = Field(..., max_length=12, examples=['+79876543210'])
    firstname: str = Field(..., examples=['Ivan'])
    lastname: str = Field(..., examples=['Ivanov'])