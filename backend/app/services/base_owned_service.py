from fastapi import HTTPException, status

from app.core.enums import UserRole
from app.models.user import User
from app.services.base_service import BaseService


class BaseOwnedService(BaseService):
    """
    Service de base pour les ressources appartenant à un utilisateur.

    Il centralise les vérifications des droits d'accès.
    """

    def check_owner(
        self,
        owner_id: int,
        user: User,
    ):
        if user.role != UserRole.ADMIN and owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

    def check_admin(
        self,
        user: User,
    ):
        if user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Administrator privileges required",
            )
