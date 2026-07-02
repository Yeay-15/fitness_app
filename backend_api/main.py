from fastapi import FastAPI
from schemas.user_schema import UserCreate

app = FastAPI()

@app.post("/register")
def user_register(user: UserCreate):
    return{
        "message" : "Data received, processing",
        "data_received" : user
    }

