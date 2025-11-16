# 👥 10. USER ROUTER

# app/routers/user_router.py

# python
from fastapi import APIRouter, Depends
from myapp.backend.auth.role_checker import role_required, permission_required
from myapp.backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/admin-only")
def admin_data(user=Depends(role_required("admin"))):
    return {"msg": "Welcome admin"}

@router.get("/update")
def update_data(user=Depends(permission_required("edit_profile"))):
    return {"msg": "You can edit profile!"}




@router.get("/me")
def get_profile(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "roles": [r.role.name for r in user.roles]
    }


@router.get("/dashboard")
def dashboard(user=Depends(get_current_user)):
    return {"message": f"Welcome to your dashboard, {user.email}!"}


@router.get("/admin-section")
def admin_panel(user=Depends(role_required("admin"))):
    return {"message": "Admin privilege granted!"}
