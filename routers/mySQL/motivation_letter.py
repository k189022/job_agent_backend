from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from mySQL.config.db import SessionLocal
from mySQL.schemas.motivation_letter import MotivationLetter, MotivationLetterCreate
from mySQL.database.motivation_letter import get_motivation_letter, create_motivation_letter, get_motivation_letters

motivation_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@motivation_router.post("/", response_model=MotivationLetter)
def create_motivation_letter(letter: MotivationLetterCreate, db: Session = Depends(get_db)):
    return create_motivation_letter(db=db, letter=letter)

@motivation_router.get("/{letter_id}", response_model=MotivationLetter)
def read_motivation_letter(letter_id: int, db: Session = Depends(get_db)):
    db_letter = get_motivation_letter(db, letter_id=letter_id)
    if db_letter is None:
        raise HTTPException(status_code=404, detail="Motivation Letter not found")
    return db_letter

@motivation_router.get("/", response_model=List[MotivationLetter])
def read_motivation_letters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    letters = get_motivation_letters(db, skip=skip, limit=limit)
    return letters
