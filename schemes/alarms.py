from datetime import datetime
from typing import Optional, Union

from fastapi import Body
from pydantic import BaseModel, Field


class AlarmsRead(BaseModel):
    date: int = Field(...)

    class Config:
        orm_mode = True
