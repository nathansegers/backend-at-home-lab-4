# router.py

from fastapi.routing import APIRouter
from .repository import CourseRepository
from .models import Course
from viewmodels import CourseWithTrack
from typing import List
router = APIRouter()

# Very basic, up to you to add some more documentation to it!
@router.get("/", response_model=List[CourseWithTrack])
def get_courses():
    # Currently there is no error handling on this API, but that's up to you!
    courses = CourseRepository.get_all()
    return courses

# Add some more functionalities later on ...
