# 1. The return type
Defining return types in FastAPI is crucial:
1. Automatic documentation
2. Errors when returned variable type does not match specified type
3. THE MOST IMPORTANT: filtering and limiting out the returned object

Let's deep dive in bullet 3. Imagine a reflex function that takes an object "User", and returns it as it is received:
```python
from fastapi import FastAPI
from pydantic import BaseModel

class UserIn(BaseModel):
    id: str
    name: str
    password: str

@app.post("/users/new/")
async def create_user(user: UserIn) -> UserIn:
    # Do some stuff like adding user to the DB
    # ...
    # ...
    # Return new user (the same as input)
    return user
```

If we do this, well be returning the password, something which is quite dangerous. Our first instict would be to create a new object and manually get rid of this password. However, FastAPI return type will do the work for us in two different ways.

## 1.1 The response model
```python
from fastapi import FastAPI
from pydantic import BaseModel

class UserIn(BaseModel):
    id: str
    name: str
    password: str

class UserOut(BaseModel):
    id: str
    name: str

@app.post("/users/new/", response_model=UserOut)
async def create_user(user: UserIn) -> any:
    # Do some stuff like adding user to the DB
    # ...
    # ...
    # Return new user (the same as input)
    return user
```
By defining **return_type=UserOut**, FastAPI identifies UserOut does not have a password attribute and thus filters it out. Notice that we changed the return typehint from **UserIn** to **any** since, from the code POV we are returning a UserIn object, so leaving **UserIn** as return typehint will lead to an error. Thus, by adding return_type attribute in the app.post decorator we manage ot:
- Filter out undersired files, in this example, the password.
- Return different object types than the actual ones we are returning.

## 1.2 Filtering with return typehint
Previous way allowed us to trigger FastAPI data filtering, but since we had to define **any** as the return type, we lost some of the functionality offered by code editors. However, we can achieve the same effet without losing this extra functionality by defining a parent-child relationship between input and output object types.

```python
class UserOut(BaseModel):
    id: str
    name: str
    password: str

class UserIn(UserOut):
    password: str

@app.post("/users/new/")
async def create_user(user: UserIn) -> UserOut:
    # Do some stuff like adding user to the DB
    # ...
    # ...
    # Return new user (the same as input)
    return user
```

This way, we still achieve filtering by FastAPI and we'll not get any error since the return type we are specifying as a parent of the actual returned type of the function.

# 1.3 Disabling response model validation
There are cases where the return type is a complext tpye that cannot be handled by PyDantic. In this cases, return annotation will yield errors on response model validations. In these cases, it is possible to disable model validation to still have return type annotations. 

In next example, we'll not have automatic data validation or documentation, but our code will not fail.

```python
@app.post("/users/new/", response_model=None)
async def create_user(user: UserIn) -> any:
    # Do some stuff like adding user to the DB
    # ...
    # ...
    # Return new user (the same as input)
    return user
```

# 1.4 Including and excluding fields from the response
Appart from automatic filtering performed by FastAPI using typehints and response models, it is also possible to include or exclude specific fields from the response manually by using the following parameters in the **app.get** (an the rest) decorators:
- response_model_exclude_unset: Includes only parameters that were set, excluding those that were left as default. If the value provided is the same as default, it is **included**.
- response_model_exclude: Exclude fields specified in the set value provided, including the rest.
- response_model_include: Include fields specified in the set value provided, ignoring the rest.

# 1.5 Response model types
As of now, we have seen response models can be single PyDantic objects. However, they could be:
- PyDantic model
- Union of PyDantic models (any of the set of models provided)
- A raw dictionary (not even a class!)
- Lots more possibilities.

# 2. Response status code
Response status code can be defined in the app decorator using the status_code parameter. This status code will be added to the documentation.

**status_code** parameter can be defined with simply an integer value, but also using constant variables available in fastapi.status.

```python
@app.get("/status_code_example/", status_code = status.HTTP_200_OK)
async def status_code_200():
    return {"response_status":"OK"}
```


