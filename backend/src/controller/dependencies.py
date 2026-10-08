from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from business_object.role import Role
from service.auth_service import AuthService

bearer = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentification requise.")
    user = AuthService().user_from_token(credentials.credentials)
    if user is None:
        raise HTTPException(status_code=401, detail="Jeton invalide ou expiré.")
    return user


def require_roles(*roles: Role):
    def check_role(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Vous n'avez pas les droits nécessaires.")
        return user

    return check_role