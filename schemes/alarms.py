from datetime import datetime
from typing import Optional, Union

from fastapi import Body
from pydantic import BaseModel, Field


class AlarmsRead(BaseModel):
    date: Union[str, datetime] = Field(...)

    class Config:
        orm_mode = True
