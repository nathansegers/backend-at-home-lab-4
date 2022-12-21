# track.py
from pydantic import BaseModel
from typing import Optional

class Track(BaseModel):
    id: Optional[int]
    title: str
    weight: int
    description: str
    
    class Config:
        orm_mode = True