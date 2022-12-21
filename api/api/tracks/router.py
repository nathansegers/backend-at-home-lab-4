# router.py

from fastapi.routing import APIRouter
from .repository import TrackRepository
from .models import Track
from typing import List
router = APIRouter()

# Very basic, up to you to add some more documentation to it!
@router.get("/", response_model=List[Track])
def get_tracks():
    # Currently there is no error handling on this API, but that's up to you!
    tracks = TrackRepository.get_all()
    return tracks

# Add some more functionalities later on ...
