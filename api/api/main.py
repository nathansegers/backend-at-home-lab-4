from fastapi import FastAPI

from courses.router import router as courses_router
from tracks.router import router as tracks_router
from subjects.router import router as subjects_router


import database as db
db.start_db()

app = FastAPI(
    title="FastAPI Demo for Backend@Home",
    description="This is a demo of FastAPI",
    version="0.0.1",
)

app.include_router(courses_router, prefix="/courses")
app.include_router(tracks_router, prefix="/tracks")
app.include_router(subjects_router, prefix="/subjects")

if __name__ == "__main__":
    # Run the app with uvicorn and autoreload
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)