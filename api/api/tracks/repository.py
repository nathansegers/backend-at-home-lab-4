# Repository.py
from database import db
from .schema import TracksTable
from .models import Track
from viewmodels import TrackWithCourses

class TrackRepository(): # Eventually, you can create a BaseRepository and make this one inherit from that!
    
    @staticmethod
    def get_all():
        db_objects = db.query(TracksTable).all()
        return [TrackWithCourses.from_orm(obj) for obj in db_objects] # Convert to the Pydantic objects here
    
    @staticmethod
    def insert(new_track: Track):
        try:
            db_object = TracksTable(**new_track.dict())
            db.add(db_object)
            db.commit()
            db.refresh(db_object)
            return Track.from_orm(db_object)
        except Exception as err:
            import traceback
            traceback.print_tb(err.__traceback__)
            db.rollback()
    
    # Implement these ones yourselves!
    @staticmethod
    def get_one():
        raise Exception("Not yet implemented")
        
    @staticmethod
    def update():
        raise Exception("Not yet implemented")
        
    @staticmethod
    def delete():
        raise Exception("Not yet implemented")
        