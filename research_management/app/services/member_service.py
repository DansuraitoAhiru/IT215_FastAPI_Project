from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.research_members import ResearchMember, MemberRole
from app.models.users import User
from app.schemas.member import AddMemberRequest
from app.services.project_service import get_project_by_id, get_project_member, check_owner

def add_new_mem(project_id: int, mem: AddMemberRequest, current_user: User, db: Session):
    try:
        project = get_project_by_id(project_id, db)
        check_owner(project_id, current_user, db)
        user = db.query(User).filter(User.id == mem.user_id).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User không tồn tại")

        exist = get_project_member(project_id, user.id, db)
        if exist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User đã là mem rồi")

        new_mem = ResearchMember(
            project_id=project_id,
            user_id= mem.user_id,
            role= MemberRole.MEMBER
        )
        db.add(new_mem)
        db.commit()
        db.refresh(new_mem)
        return new_mem
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))


def remove_mem(user_id: int, project_id: int, current_user: User, db: Session):
    try:
        project = get_project_by_id(project_id, db)
        check_owner(project_id, current_user, db)

        mem = get_project_member(project_id, user_id, db)
        if not mem:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User không phải thành viên của đề tài")

        if mem.role == MemberRole.OWNER:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Không thể xóa OWNER")

        db.delete(mem)
        db.commit()
        return mem
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))


def get_all_members(project_id: int, user: User, db: Session):
    project = get_project_by_id(project_id, db)
    mem = get_project_member(project_id, user.id, db)
    if not mem:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User không phải thành viên của đề tài")
    return db.query(ResearchMember).join(User).filter(ResearchMember.project_id == project_id).all()
