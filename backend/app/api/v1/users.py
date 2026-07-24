from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_users()

@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)

    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))