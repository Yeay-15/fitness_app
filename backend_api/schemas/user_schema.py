from pydantic import BaseModel

class UserCreate(BaseModel):
    name : str
    age : int
    body_weight_kg : float
    body_height_cm : float
