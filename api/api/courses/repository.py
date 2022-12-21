# Repository.py
from database import db
from .schema import CoursesTable
from .models import Course
from viewmodels import CourseWithTrack

class CourseRepository(): # Eventually, you can create a BaseRepository and make this one inherit from that!
    
    @staticmethod
    def get_all():
        db_objects = db.query(CoursesTable).all()
        return [CourseWithTrack.from_orm(obj) for obj in db_objects] # Convert to the Pydantic objects here
    
    @staticmethod
    def insert(new_course: Course):
        try:
            db_object = CoursesTable(**new_course.dict())
            db.add(db_object)
            db.commit()
            db.refresh(db_object)
            return Course.from_orm(db_object)
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
        