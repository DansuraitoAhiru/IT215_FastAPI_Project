from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.users import User
from app.models.research_members import MemberRole
from app.models.research_tasks import ResearchTask, TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.project_service import get_project_by_id, get_project_member, check_owner
from app.utils.validate import validate_space

def create_task_service(project_id: int, task: TaskCreate, user: User, db: Session):
    try:
        project=get_project_by_id(project_id, db)
        member = get_project_member(project_id, user.id, db)
        if not member:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "User không phải thành viên của dự án")

        if task.assignee_id is not None:
            assignee = get_project_member(project_id, task.assignee_id, db)
            if not assignee:
                raise HTTPException(status.HTTP_403_FORBIDDEN, "Assignee phải là thành viên dự án")

        new_task = ResearchTask(
            project_id=project_id,
            title=validate_space(task.title),
            description=task.description.strip(),
            assignee_id = task.assignee_id,
            status=TaskStatus.TODO,
            priority=task.priority,
            due_date=task.due_date,
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))


def get_all_tasks(project_id: int, user: User, db: Session):
    project = get_project_by_id(project_id, db)
    mem = get_project_member(project_id, user.id, db)
    if not mem:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User không phải thành viên của đề tài")
    return db.query(ResearchTask).filter(ResearchTask.project_id == project_id).all()


def get_task_by_id(id: int, user: User, db: Session):
    task = db.query(ResearchTask).filter(ResearchTask.id == id).first()
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Không tìm thấy nhiệm vụ nghiên cứu")
    mem = get_project_member(task.project_id, user.id, db)
    if not mem:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User không phải thành viên của đề tài")
    return task


def update_task_service(task_id: int, data: TaskUpdate, user: User, db: Session):
    try:
        task = get_task_by_id(task_id, user, db)

        if data.assignee_id is not None:
            assignee = get_project_member(task.project_id, data.assignee_id, db)
            if not assignee:
                raise HTTPException(status.HTTP_403_FORBIDDEN, "Assignee phải là thành viên dự án")

        task.title=validate_space(data.title)
        task.description=data.description.strip()
        task.assignee_id = data.assignee_id
        task.status=data.status
        task.priority=data.priority
        task.due_date=data.due_date

        db.commit()
        db.refresh(task)
        return task
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))


def delete_task_service(task_id: int, user: User, db: Session):
    try:
        task = get_task_by_id(task_id, user, db)
        member = get_project_member(task.project_id, user.id, db)
        if member.role != MemberRole.OWNER and task.assignee_id != task_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Chỉ có OWNER hoặc Asignee mới có quyền xóa nhiệm vụ")
        db.delete(task)
        db.commit()
        return task
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)) 

