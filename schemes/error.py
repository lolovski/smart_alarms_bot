import datetime
from typing import Optional, Union

from fastapi import Body
from pydantic import BaseModel, Field, ConfigDict


class ErrorCreate(BaseModel):
    message: str = Field(max_length=2048)
    title: str = Field(max_length=128)
    board_id: int = Field(...)


class ErrorRead(ErrorCreate):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    date: [datetime.datetime] = Field(...)
