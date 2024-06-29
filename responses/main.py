from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class UserIn(BaseModel):
    id: str
    name: str
    age: int = 18
    password: str

class UserOut(BaseModel):
    id: str
    name: str 
    age: int = 18

class UserIn2(UserOut):
    password: str


@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }

# Filtering Example 1: Using return_model
@app.get("/filtering/return_model", response_model=UserOut)
async def return_model_filtering(user: UserIn) -> any:
    return user

# Filtering Example 2: Using type annotations
@app.get("/filtering/type_annotation")
async def return_model_filtering(user: UserIn2) -> UserOut:
    return user

# Filtering Example 3: Explicitly removing fields
@app.get("/filtering/explicit_exclusion", response_model=UserIn, response_model_exclude={"password"})
async def return_model_filtering(user: UserIn):
    return user

# Status code example
@app.get("/status_code_example/", status_code = status.HTTP_200_OK)
async def status_code_200():
    return {"response_status":"OK"}


