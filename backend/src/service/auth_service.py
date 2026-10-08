import os
from datetime import datetime, timedelta, timezone

import jwt

from dao.utilisateur_dao import UtilisateurDao  # à implémenter
from utils.security import hash_password, verify_password

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-development-secret-before-deployment")


def _public_user(user) -> dict:
    return {"id": user.id, "username": user.username, "role": user.role.value}


class AuthService:
    def __init__(self, dao=None) -> None:
        self.dao = dao or UtilisateurDao()

    def _response(self, user) -> dict:
        token = jwt.encode(
            {
                "sub": str(user.id),
                "exp": datetime.now(timezone.utc) + timedelta(hours=12),
            },
            SECRET_KEY,
            algorithm="HS256",
        )
        return {"access_token": token, "token_type": "bearer", "user": _public_user(user)}

    def register(self, username: str, password: str) -> dict:
        username = username.strip()
        if not username:
            raise ValueError("Le nom d'utilisateur ne peut pas être vide.")
        if self.dao.find_by_username(username):
            raise ValueError("Ce nom d'utilisateur est déjà utilisé.")
        user = self.dao.create(username, hash_password(password))
        return self._response(user)

    def login(self, username: str, password: str) -> dict:
        user = self.dao.find_by_username(username.strip())
        if user is None or not verify_password(password, user.password_hash):
            raise PermissionError("Nom d'utilisateur ou mot de passe incorrect.")
        return self._response(user)

    def user_from_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = int(payload["sub"])
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            return None
        return self.dao.find_by_id(user_id)