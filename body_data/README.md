# 1. Body Data
When throwing a POST request to an API, appart from defining path and query parameters, additional data can be provided in the body of the request.

To do so in FastAPI, a data class inheriting from PyDantic BaseModel is needed, and an instance of this class should be passed as input to the POST request function. Find next an example

```python
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
```

# 2. Singular values in body data
It is also possible to specify body data without a data class inheriting from BaseModel, thus being body data singular values such as strings or integers. We can do this
by specifying a function parameter as:

**body_singlurar_value: Annotation(int, Body())**

It is crucial to add this "Body()" annotation since otherwise **body_singular_value** will be interpreted by FastAPI as a query or path param.

# 3. Embedded body parameters
Regular body parameters are taken by FastAPI as follows:
```json
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

However, we can also force FastAPI to interpret body parameters as embedded body parameters:
```json
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```
This can be achieved by adding **embed=True** parameter to Body():

**body_singlurar_value: Annotation(SomeBodyClass, Body(embed=True))**

# 4. Validation on Body fields
Validation can also be applied to Body parameter fields. This can be done as follows:

```python
from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel, Field

class BodyClass(BaseModel):
    id: str
    name: str =  Field(
        default=None, title="name of the item", max_length=300
    )
    attr1: str | None
    attr2: int
```