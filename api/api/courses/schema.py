from database import Base

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

class CoursesTable(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    tools = Column(Text)
    semester = Column(Integer)
    weight = Column(Integer)
    pillar = Column(String(255))
    content = Column(Text)

    # track_id = Column(Integer)
    track_id = Column(Integer, ForeignKey("tracks.id"))
    track = relationship("TracksTable", back_populates="courses")
