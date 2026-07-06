from pydantic import BaseModel

class WorkoutCreate(BaseModel):
    user_id : int
    day_name : str
    split_type : str