from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import get_current_user, AuthData
from config import configs
from db.models import Staff
import bcrypt

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/staff")


@router.get("/", response_class=HTMLResponse)
def staff_page(
    request: Request,
    authenticated: AuthData = Depends(get_current_user),
):
    staff = Staff.select().order_by(Staff.permission.desc())

    context = {
        "title": "Персонал",
        "authenticated": authenticated,
        "request": request,
        "project": configs.project_name,
        "staff": staff,
    }

    return templates.TemplateResponse("staff.html", context)


@router.post("/")
def create_staff(
    user_id: int = Body(...),
    password: str = Body(...),
    permission: int = Body(...),
    authenticated: AuthData = Depends(get_current_user),
):
    if permission >= authenticated.permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to add staff member",
        )

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    staff, created = Staff.get_or_create(
        id=user_id,
        defaults={
            "id": user_id,
            "permission": permission,
            "password_hash": password_hash,
        },
    )

    if not created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Staff member with this ID already exists",
        )

    return {"message": "Staff member successful added"}


@router.delete("/{user_id}")
def delete_staff(
    user_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    if user_id != authenticated.id:
        staff = Staff.get_or_none(Staff.id == user_id)
        if staff and (authenticated.permission > staff.permission):
            staff.delete_instance()
            return {"message": "Staff member deleted"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to delete staff member"
    )
