from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.services.member_service import add_new_mem, remove_mem, get_all_members
from app.schemas.member import AddMemberRequest, MemberResponse
from app.db.database import get_db
from app.dependencies.dependency import get_current_user
from app.models.users import User
from sqlalchemy.orm import Session
from app.utils.responses import create_response

router = APIRouter(
    prefix="/research-projects/{id}/members",
    tags=["Member"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def add_mem(request: Request, project_id: int, mem: AddMemberRequest, user:User=Depends(get_current_user), db: Session=Depends(get_db)):
    new_nem = add_new_mem(project_id, mem, user, db)
    data = MemberResponse.model_validate(new_nem)
    return create_response(request, 201, "Thêm thành viên vào dự án thành công", data.model_dump(), None)


@router.delete("/{user_id}")
def delete_mem(request: Request, user_id: int, project_id: int,  current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    deleted_mem = remove_mem(user_id, project_id, current_user, db)
    data = MemberResponse.model_validate(deleted_mem)
    return create_response(request, 200, "Xóa thành viên khỏi dự án", data.model_dump(), None)


@router.get("")
def get_members(project_id: int, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    members = get_all_members(project_id, user, db)
    return [
        {
            "user_id": mem.user.id,
            "email": mem.user.email,
            "full_name": mem.user.full_name,
            "role": mem.role
        }
        for mem in members
    ]