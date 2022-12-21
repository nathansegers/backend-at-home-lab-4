from database import Base

from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship

class TracksTable(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    weight = Column(Integer)
    description = Column(Text)

    courses = relationship("CoursesTable", back_populates="track")
