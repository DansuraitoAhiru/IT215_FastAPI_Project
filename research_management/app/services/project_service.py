from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.research_projects import ResearchProject
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.models.research_members import ResearchMember, MemberRole
from app.models.users import User, UserRole
from app.utils.validate import validate_space

def create_project_service(project: ProjectCreate, owner: User, db: Session):
    try:
        new_project = ResearchProject(
            name=validate_space(project.name),
            description=project.description.strip(),
            owner_id=owner.id
        )
        db.add(new_project)
        db.flush()   # để lưu lại project nhưng chưa commit, nma vẫn cần phải add member nên cần có project id

        member = ResearchMember(
            project_id=new_project.id,
            user_id=owner.id,
            role=MemberRole.OWNER
        )
        db.add(member)
        db.commit()
        db.refresh(new_project)
        return new_project
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))


def get_projects_service(user: User, db: Session, keyword: str | None = None):
    query = db.query(ResearchProject).join(ResearchMember, ResearchMember.project_id == ResearchProject.id).filter(user.id == ResearchMember.user_id)
    if keyword:
        query = query.filter(ResearchProject.name.ilike(f"%{keyword}%"))
    return query.all()


def get_project_by_id(id: int, db: Session):
    project = db.query(ResearchProject).filter(ResearchProject.id == id).first()
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Đề tài nghiên cứu không tồn tại")
    return project


def get_project_member(id: int, user_id: int, db: Session):
    member = db.query(ResearchMember).filter(ResearchMember.project_id == id, ResearchMember.user_id == user_id).first()
    if not member:
        return None
    return member


def check_owner(id: int, user: User, db: Session):
    member = get_project_member(id, user.id, db)
    if not member or member.role != MemberRole.OWNER:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Chỉ có Owner dự án mới có thể dùng các chức năng này")
    return member


def get_project_service(id: int, user: User, db: Session):
    project = get_project_by_id(id, db)
    if user.role == UserRole.ADMIN:
        return project
    member = get_project_member(id, user.id, db)
    if not member:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User không phải thành viên của dự án này")
    return project


def update_project_service(data: ProjectUpdate, id: int, user: User, db: Session):
    try: 
        project = get_project_by_id(id, db)
        member = check_owner(id, user, db)
        for key, value in data.model_dump(exclude_unset=True).items():
            if key == "name":
                project.name = validate_space(data.name)
            elif key == "description":
                project.description = data.description.strip()
            setattr(project, key, value)
        
        db.commit()
        db.refresh(project)
        return project
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))


def delete_project_service(id: int, user: User, db: Session):
    try:
        project = get_project_by_id(id, db)
        member = check_owner(id, user, db)
        deleted_project = ProjectResponse.model_validate(project)
        db.delete(project)
        db.commit()
        return deleted_project
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))
