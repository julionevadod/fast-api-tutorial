from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

class BodyClass(BaseModel):
    id: str
    name: str
    attr1: str | None
    attr2: int

@app.get("/")
async def root():
    return {
        "message": "Hello World!"
    }

@app.get("/items/")
async def create_body(body: BodyClass):
    return {"body":body}
