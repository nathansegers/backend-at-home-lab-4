from courses.models import Course
from tracks.models import Track
from typing import Optional, List

class CourseWithTrack(Course):
    track: Optional[Track] # Optional in case it is null...

class TrackWithCourses(Track):
    courses: Optional[List[Course]]