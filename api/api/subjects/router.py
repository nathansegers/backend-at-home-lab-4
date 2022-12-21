# router.py

from fastapi.routing import APIRouter
from .repository import SubjectRepository
from .models import Subject
from typing import List
router = APIRouter()

# Very basic, up to you to add some more documentation to it!
@router.get("/", response_model=List[Subject])
def get_all_subjects():
    # Currently there is no error handling on this API, but that's up to you!
    tracks = SubjectRepository.get_all()
    return tracks

@router.post("/", name="Create a subject", response_model=str)
def create_subject(subject: Subject):
    result = SubjectRepository.create(subject)
    return result

# Add some more functionalities later on ...
