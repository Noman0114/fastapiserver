from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg

app = FastAPI()

# PostgreSQL database connection details
DATABASE_URL = "postgresql://username:password@localhost/mydatabase"

# Pydantic model for request body validation
class User(BaseModel):
    name: str
    email: str

# Establishing a connection pool
@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)
    await create_table_if_not_exists()

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

# Function to create the table if it does not exist
async def create_table_if_not_exists():
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE
    );
    """
    async with app.state.db.acquire() as connection:
        await connection.execute(query)

# POST API to add a new user
@app.post("/users/")
async def create_user(user: User):
    query = "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id"
    try:
        async with app.state.db.acquire() as connection:
            user_id = await connection.fetchval(query, user.name, user.email)
        return {"id": user_id, "name": user.name, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail="User already exists or invalid data")

# For testing, get all users
@app.get("/users/")
async def get_users():
    query = "SELECT * FROM users"
    async with app.state.db.acquire() as connection:
        rows = await connection.fetch(query)
    return [dict(row) for row in rows]
