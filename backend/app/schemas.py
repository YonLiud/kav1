from pydantic import BaseModel
from typing import Optional, Dict

class VisitorCreate(BaseModel):
    name: str
    visitorid: str
    inside: bool
    properties: Optional[Dict] = None

    class Config:
        orm_mode = True

class VisitorBase(BaseModel):
    dbid: int
    name: str
    visitorid: str
    inside: bool
    properties: Optional[Dict] = None

    class Config:
        orm_mode = True

class VisitorUpdate(BaseModel):
    name: Optional[str] = None
    visitorid: Optional[str] = None
    inside: Optional[bool] = None
    properties: Optional[Dict] = None

    class Config:
        orm_mode = True