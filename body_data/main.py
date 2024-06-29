from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel, Field

app = FastAPI()

class BodyClass(BaseModel):
    id: str
    name: str =  Field(
        default=None, title="name of the item", max_length=300, examples = ["test_name"]
    )
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
