from fastapi import HTTPException, status, APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import create_project_service, get_projects_service, get_project_service, update_project_service, delete_project_service
from app.models.users import User
from app.db.database import get_db
from app.dependencies.dependency import get_current_user
from app.utils.responses import create_response

router = APIRouter(
    prefix="/research-projects",
    tags=["Project"]
)


# response_model: FastAPI dùng để định dạng + validate dữ liệu trả về API
# model_validate: Pydantic dùng để chuyển một dữ liệu hoặc object thành Pydantic model - một class dùng để định nghĩa và kiểm tra (validate) dữ liệu trong Python
@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(request: Request, project: ProjectCreate, owner: User = Depends(get_current_user), db: Session=Depends(get_db)):
    new_project = create_project_service(project, owner, db)
    data = ProjectResponse.model_validate(new_project)
    return create_response(request, 201, "Thêm đề tài nghiên mới thành công", data.model_dump(), None)


@router.get("", response_model=list[ProjectResponse])
def get_projects(user: User = Depends(get_current_user), db: Session=Depends(get_db), keyword: str | None = None):
    return get_projects_service(user, db, keyword)


@router.get("/{id}")
def get_project(id: int, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return get_project_service(id, user, db)


@router.patch("/{id}")
def update_project(request: Request, data: ProjectUpdate, id: int, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    project = update_project_service(data, id, user, db)
    data = ProjectResponse.model_validate(project)
    return create_response(request, 200, "Cập nhật đề tài nghiên cứu thành công", data.model_dump(), None)


@router.delete("/{id}")
def delete_project(request: Request, id: int, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    deleted_project = delete_project_service(id, user, db)
    data = ProjectResponse.model_validate(deleted_project)
    return create_response(request, 200, "Xóa đề tài nghiên cứu thành công", data.model_dump(), None)