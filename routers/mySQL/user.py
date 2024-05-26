from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from mySQL.config.db import SessionLocal
from mySQL.database.user import create_user, get_user, get_users
from mySQL.schemas.user import UserCreate, User


user_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user_router.get("/", status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users
