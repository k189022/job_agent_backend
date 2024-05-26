from sqlalchemy.orm import Session
from mySQL.models.motivation_letter import MotivationLetter
from mySQL.schemas.motivation_letter import MotivationLetterCreate


# Motivation Letter CRUD
def get_motivation_letter(db: Session, letter_id: int):
    return db.query(MotivationLetter).filter(MotivationLetter.id == letter_id).first()

def get_motivation_letters(db: Session, skip: int = 0, limit: int = 10):
    return db.query(MotivationLetter).offset(skip).limit(limit).all()

def create_motivation_letter(db: Session, letter: MotivationLetterCreate):
    db_letter = MotivationLetter(**letter.dict())
    db.add(db_letter)
    db.commit()
    db.refresh(db_letter)
    return db_letter
