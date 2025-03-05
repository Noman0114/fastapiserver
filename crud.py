from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

users_db = []

class User(BaseModel):
    id: int
    name: str
    email: str
@router.post("/users/", response_model=User)
def create_user(user: User):
    users_db.append(user)
    return user

@router.get("/users/", response_model=List[User])
def get_users():
    return users_db

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    return {"error": "User not found"}

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            users_db[index] = updated_user
            return updated_user
    return {"error": "User not found"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users_db
    users_db = [user for user in users_db if user.id != user_id]
    return {"message": "User deleted successfully"}
