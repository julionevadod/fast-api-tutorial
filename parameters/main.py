from fastapi import FastAPI, Query
from enum import Enum
from typing_extensions import Annotated

app = FastAPI()

class TransportSelector(str,Enum):
    car = 1
    motorbike = 2
    bicycle = 3


@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: Annotated(str, Query(max_length=50))):
    return {"user_id": user_id}

@app.get("/users/transport/{transport_type}")
async def get_transport(transport_type: TransportSelector):
    if transport_type is TransportSelector.car:
        return {"transport":TransportSelector.car.name}
    
    if transport_type.value == "motorbike":
        return {"transport":TransportSelector.motorbike.name}
    
    return {"transport":TransportSelector.bicycle.name}
