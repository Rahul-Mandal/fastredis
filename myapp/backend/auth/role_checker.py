
# # 🛡️ 7. AUTH – Role & Permission Checker

# app/auth/role_checker.py

# python
from fastapi import Depends, HTTPException
from myapp.backend.auth.dependencies import get_current_user

def role_required(*roles):
    def wrapper(user=Depends(get_current_user)):
        user_roles = [r.role.name for r in user.roles]
        if not any(r in roles for r in user_roles):
            raise HTTPException(403, f"Requires roles: {roles}")
        return user
    return wrapper

def permission_required(*permissions):
    def wrapper(user=Depends(get_current_user)):
        user_permissions = set()
        for user_role in user.roles:
            for role_permission in user_role.role.permissions:
                user_permissions.add(role_permission.permission.name)

        if not any(p in user_permissions for p in permissions):
            raise HTTPException(403, f"Requires permissions: {permissions}")
        return user
    return wrapper
