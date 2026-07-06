from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index = True)
    age = Column(Integer)
    body_weight_kg = Column(Float)
    body_height_cm = Column(Float)

    workouts = relationship("WorkoutSchedule", back_populates="owner")