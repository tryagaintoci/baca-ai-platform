from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import verify_password


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user: UserCreate) -> User:
        existing_user = self.repository.get_by_email(user.email)

        if existing_user:
            raise ValueError("Email already exists")

        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password_hash=hash_password(user.password),
            is_active=True,
            is_superuser=False,
        )

        return self.repository.create(new_user)

    def get_users(self) -> list[User]:
        return self.repository.get_all()

    def authenticate(self, email: str, password: str):
        user = self.repository.get_by_email(email)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user