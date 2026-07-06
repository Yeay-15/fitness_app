from sqlalchemy import Column, String, Integer, ForeignKey
from database import Base

class WorkoutSchedule(Base):
    __tablename__ = "workout_schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    day_name = Column(String)
    split_type = Column(String)