# 1. The simplest API
The simplest API can be created by replicating the following code.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }
```

root() function is executed when **base url** is queried, returning **{"message": "Hello World"}**. 
Bear in mind this base url is defined when serving the API by means of the following command:
```bash
fastapi dev main.py
```

Since we're not specifying any base endpoint, **localhost:8080** is taken as base url. Thus, **{"message": "Hello World"}**
is retrieved when accessing **https://localhost:8000/**.


# 2. Providing parameters
## 2.1 Path Parameters
Parameters can be provided within the url used to query the API. Find next a simple example.
```python
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```

By adding previous code, we can still query **https://localhost:8000/** to get **{"message": "Hello World"}**, and also
**https://localhost:8000/items/anyhting_you_want**, to get  **{"message": anything_you_want}** This **anything_you_want** is by default a string, even if we type 
**https://localhost:8000/items/1234**. However, we can modify this behaviour by using typehints.

Updating previous code with:
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

Allows us to restrict **item_id** to only accept integer values. In fact, using **:int** typehint, will raise an error if *item_id** is not an integer
since fastAPI will try to parse it to an integer value (422 error).

Same routes can be used to retrieve different data. Let's imagine we are logged into our X account. If I want to go to my personal profile, I can visit **/users/me**. However, 
we could also visit our friends account by querying **users/my_friend_user_id**. However, my friend would see the contents in **users/my_friend_user_id** when he queries **/users/me**.

To achieve this behaviour, we need to carefully define the different functions in order. Let's study two options.
#### Option 1:
```python
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

```
Functions are evauluated in order, so **/users/me** will never come into play since it will also match **/users/{user_id}**

#### Option 2:
```python
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```
We can now achieve expected behaviour.

### Predefined path parameters
Enum classes can be very very helpful when predefined parameter values are needed, as if we were talking about a selectbox.
This "selectbox" behavior also propagates to autodocumentation. When using an Enum class, path parameter can ONLY take the class VALUES (not names), otherwise, an error will raise otherwise.
```python
class TransportSelector(str,Enum):
    car = 1
    motorbike = 2
    bicycle = 3
    
@app.get("/users/transport/{transport_type}")
async def get_transport(transport_type: TransportSelector):
    if transport_type is TransportSelector.car:
        return {"transport":TransportSelector.car.name}
    
    if transport_type.value == "motorbike":
        return {"transport":TransportSelector.motorbike.name}
    
    return {"transport":TransportSelector.bicycle.name}
```

### Path as path parameters
Sometimes path parameters need to be paths themselves. This can be achieved easily transitioning from **{path_parameter}** to **{path: path_parameter}**. Using this **path:** tag inside parameter definition let FastAPI know parameter could be a path.


## 2.2 Query Parameters
Appart from path parameters, other parameters can be defined in the query, **query parameters**. These are defined as:

**<BASE_URL>/<PATH>/<PATH_PARAMETERS>?query_param1=value1&query_param2=value2&query_param3=value3**

Everything we stated about path parameters is also applicable to query parameters:
- Typehints
- Predefined parameters
- Automatic documentation 

Query parameters can be:
- Optional: If we provide a default value. This default value can be None. In this case, URL query may lack this parameter
- Compulsory: It we do not provide a default value. In this case an URL lacking this parameter will raise an error. Another way to make a parameter compulsory is to use ellipsis, making "..." as default.

These parameter enter the GET function as path parameters and FastAPI knows under the hood which parameter is coming from path parameter and which one from query parameters.

# 3. Parameter Validations
Annotated module from typing_extension params can be used to perform validations on data such as:
- String length
- Default values
- Regex

Find next an example. We use "Query" since we are validating the values of a query parameter
```python
from fastapi import FastAPI, Query
from typing_extensions import Annotated
...
@app.get("/items/")
async def read_user(item: Annotated(str, Query(max_length=50))):
    return {"item": item}
```

For sure, validation of other datatypes like numbers can be performed, as well as for other parameter types appart from query:
- Path()
- Body()
- Header()
- Cookie()
All of them accept the same parameters as Query()

Find [here](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/) additional tips on numeric validations