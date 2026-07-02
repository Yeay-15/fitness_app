from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate
from database import engine, Base, SessionLocal
from models.user_model import User


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def user_register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name = user.name,
        age = user.age,
        body_weight_kg = user.body_weight_kg,
        body_height_cm = user.body_height_cm
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "message" : "Data successfully insert into database!",
        "user_data" : new_user
    }

