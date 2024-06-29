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

# 5. Example data
Example data can be provided to Body fields. This is a quite interesting feature since this examples will be added to automatic documentation by OpenAPI. We can provide example data in three ways:

1. Using the **model_config** attribute in the class defining the body:
```python
class BodyClass(BaseModel):
    id: str
    name: str
    attr1: str | None
    attr2: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                "id": "1a2s3f5",
                "name": "test_name",
                "attr1": "value1",
                "attr2": 37
            ]
        }
    }
```
2. As a parameter of **Field()** object: 
```python
class BodyClass(BaseModel):
    id: str
    name: str =  Field(
        default=None, title="name of the item", max_length=300, examples = ["test_name"]
    )
    attr1: str | None
    attr2: int
```
3. Using open_api_examples in **Body()** object call. Swagger UI has the limitation that only shows a single example. We can overcome this limitation using this third method. the **open_api_examples** parameter is a dict, where each example should be the value of a specific key. These examples will be shown as a selectbox where the name in the selectbox will be these keys.
```python
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
...
```

Finally, bear in mind examples can be used with any of:
- Path()
- Query()
- Header()
- Cookie()
- Body()
- Form()
- File() -> files are uploaded as form data