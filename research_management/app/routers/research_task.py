from fastapi import APIRouter, status, Depends, Request
from app.services.task_service import create_task_service, get_all_tasks, get_task_by_id, update_task_service, delete_task_service
from app.utils.responses import create_response
from app.dependencies.dependency import get_current_user
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.users import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from typing import Literal

router = APIRouter(
    tags=["Task"]
)

@router.post("/research-projects/{id}/research-tasks", status_code=status.HTTP_201_CREATED)
def create_task(request: Request, project_id: int, task: TaskCreate, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    new_task = create_task_service(project_id, task, user, db)
    data = TaskResponse.model_validate(new_task)
    return create_response(request, 201, "Thêm nhiệm vụ nghiên cứu thành công", data.model_dump(), None)


@router.get("/research-projects/{id}/research-tasks", response_model=list[TaskResponse])
def get_tasks(
    project_id: int, 
    user: User=Depends(get_current_user), 
    db: Session=Depends(get_db),
    task_status: Literal["TODO", "IN_PROGRESS", "DONE"] | None=None,
    priority: Literal["LOW", "MEDIUM", "HIGH"] | None=None,
    asignee_id: int | None=None,
    keyword: str | None=None,
    limit: int = 1,
    offset: int = 0,
    sort: Literal["created_at", "due_date"] | None=None
):
    return get_all_tasks(project_id, user, db, task_status, priority, asignee_id, keyword, limit, offset, sort)


@router.get("/research-tasks/{id}", response_model=TaskResponse)
def get_detail_task(task_id: int, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return get_task_by_id(task_id, user, db)


@router.patch("/research-tasks/{id}")
def update_task(request: Request, task_id: int, task_update: TaskUpdate, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    task = update_task_service(task_id, task_update, user, db)
    data = TaskResponse.model_validate(task)
    return create_response(request, 200, "Cập nhật nhiệm vụ thành công", data.model_dump(), None)


@router.delete("/research-tasks/{id}")
def delete_task(request: Request, task_id: int, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    deleted_task = delete_task_service(task_id, user, db)
    data = TaskResponse.model_validate(deleted_task)
    return create_response(request, 200, "Xóa nhiệm vụ thành công", data.model_dump(), None)