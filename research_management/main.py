from fastapi import FastAPI, Depends, HTTPException, status
from app.db.database import engine, Base, get_db
from app.models.research_members import ResearchMember
from app.models.research_projects import ResearchProject
from app.models.research_tasks import ResearchTask
from app.models.users import User
from app.utils.exceptions import exception_handlers
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.routers.auth import router as auth_router
from app.routers.users import router as user_router
from app.routers.research_project import router as project_router
from app.routers.research_member import router as member_router
from app.routers.research_task import router as task_router

Base.metadata.create_all(engine)
app = FastAPI()

exception_handlers(app)
@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        return {
            "status": "Sucess",
            "message": "Still alive"
        }
    except Exception as errors:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(errors))
    
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(member_router)
app.include_router(task_router)
