from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal

from schemas.user_schema import UserCreate, UserUpdate
from schemas.workout_schema import WorkoutCreate

from models.user_model import User
from models.workout_model import WorkoutSchedule

# Automatically create tables in the database if they don't exist yet
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()

# Dependency: Open a database session when a request comes, and safely close it afterward
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to register a new user
@app.post("/register")
def user_register(user: UserCreate, db: Session = Depends(get_db)):
    
    # Map the incoming data (Pydantic schema) to our database model (SQLAlchemy)
    new_user = User(
        name=user.name,
        age=user.age,
        body_weight_kg=user.body_weight_kg,
        body_height_cm=user.body_height_cm
    )
    
    # Save the new user, commit the transaction, and fetch the generated ID
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Data successfully inserted into the database!",
        "user_data": new_user
    }

# Endpoint to fetch user profile by ID and calculate their BMR on the fly
@app.get("/users/{user.id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):

    # Query the database to find a user with the matching ID
    user = db.query(User).filter(User.id == user_id).first()

    # Protect the endpoint: if no user is found, throw a 404 error
    if not user:
        raise HTTPException(status_code=404, detail="User not found in our database")
    
    # Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor equation
    bmr = (10 * user.body_weight_kg) + (6.25 * user.body_height_cm) - (5 * user.age) + 5

    # Calculate Total Daily Energy Expenditure (TDEE) assuming moderate activity level (multiplier: 1.55)
    tdee = bmr * 1.55
    # Return the dynamic response containing both DB data and calculated metrics
    return{
        "message": "User profile and BMR fetched succesfully!",
        "user_data": {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "body_weight_kg": user.body_weight_kg,
            "body_height_cm": user.body_height_cm
        },
        "metrics": {
        "calculated_bmr": bmr,
        "calculated_tdee": tdee,
        "activity_level": "Moderate (Exercise 3-5 times/week)"
        },
        "workout_schedules": [
            {
                "schedule_id": workout.id,
                "day_name": workout.day_name,
                "split_type": workout.split_type
            } for workout in user.workouts
        ]
    }

# Endpoint to update user data (PUT)
@app.put("/users/{user_id}")
def update_user_profile(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    
    # 1. Search for the user in the database
    user = db.query(User).filter(User.id == user_id).first()

    # 2. If user doesn't exist, throw a 404 error
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 3. Dynamic Update: Loop through the incoming data and only update fields that are provided
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    # 4. Save changes permanently to PostgreSQL
    db.commit()
    db.refresh(user)

    return{
        "message": "User profile updated succesfully!",
        "updated_data": user
    }

# Endpoint to delete a user and their data (DELETE)
@app.delete("/users/{user_id}")
def delete_user_account(user_id: int, db: Session = Depends(get_db)):

    # 1. Search for the target user
    user = db.query(User).filter(User.id == user_id).first()

    # 2. Protect the endpoint from ghost IDs
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 3. Delete from the database basket and commit permanently
    db.delete(user)
    db.commit()

    return{
        "message": f"User with ID {user_id} and all their have been deleted permanently"
    }

@app.post ("/workouts")
def create_workout_schedule(workout: WorkoutCreate, db: Session = Depends(get_db)):

    # 1. Foreign Key Protection: Verify if the user actually exists first
    user_exist = db.query(User).filter(User.id == workout.user_id).first()

    if not user_exist:
        raise HTTPException(
            status_code=404,
            detail="User ID not found. Cannot asign workout"
        )
    
    # 2. Map the validated incoming data to our SQLAlchemy model
    new_workout = WorkoutSchedule(
        user_id = workout.user_id,
        day_name = workout.day_name,
        split_type = workout.split_type
    )

    # 3. Save to database, commit the transaction, and fetch the generated ID
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return{
        "message": "Workout schedule added succesfully!",
        "workout_data": new_workout
    }