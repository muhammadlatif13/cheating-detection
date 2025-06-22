import uvicorn # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, exam, questions, camera_monitoring

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from separate modules
app.include_router(auth.router, tags=["Authentication"])
app.include_router(exam.router, tags=["Exams"])
app.include_router(questions.router, tags=["Exam Questions"])
app.include_router(camera_monitoring.router, tags=["Camera Monitoring"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)