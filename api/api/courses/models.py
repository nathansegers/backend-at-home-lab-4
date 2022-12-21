# models.py
from pydantic import BaseModel
from typing import Optional

class Course(BaseModel):
    id: Optional[int]
    title: str
    tools: Optional[str] # Nullable, so optional
    semester: int
    weight: int
    pillar: str # This can be converted to an ENUM if you want to!
    track_id: Optional[int] # Nullable, so optional Currently only one track, no list of tracks in the database!
    content: str
    
    class Config:
        orm_mode = True