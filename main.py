from fastapi import FastAPI
from simple.simple import router as simple_router
from crud import router as crud_router
app = FastAPI()

app.include_router(simple_router)
app.include_router(crud_router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI! 🎉"}
