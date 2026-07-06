from pydantic import BaseModel

class UserCreate(BaseModel):
    name : str
    age : int
    body_weight_kg : float
    body_height_cm : float

class UserUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    body_weight_kg: float | None = None
    body_height_cm: float | None = None
