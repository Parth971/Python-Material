import datetime
import time
from enum import Enum
from typing import List, Any, Sequence

from fastapi import FastAPI, Query, Body, Cookie, Header, Form, File, UploadFile, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, Field, HttpUrl
from pydantic.networks import IPv4Address, EmailStr
from fastapi.responses import RedirectResponse, Response, HTMLResponse, JSONResponse
from fastapi.requests import Request
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()


# class UserType(Enum):
#     admin = 'admin'
#     user = 'customer'
#
#
# class Item(BaseModel):
#     name: str
#     price: int
#     brand: Optional[str] = None
#
# items = {
#     1: {
#         'name': 'Apples',
#         'price': 10.50
#     },
#     2: {
#         'name': 'Orange',
#         'price': 50.52
#     },
#     3: {
#         'name': 'Banana',
#         'price': 100.23
#     }
# }
#
#
# @app.get('/item/{item_id}')
# def get(*, item_id: int, name: str = None, test: int):
#     return items.get(item_id, {'data': 'Item not found'})
#
#
# @app.post('/create-item')
# def create_item(item: Item):
#
#     x = random.randint(1, 3)
#     print(x, items.keys())
#     time.sleep(x)
#     item_id = len(items) + 1
#     time.sleep(x)
#     if item_id in items.keys():
#         raise HTTPException(status_code=400)
#
#     items[item_id] = item.dict()
#     print(item_id)
#     return items
#
# @app.get('/test')
# async def test(name: Union[bool, None] = None):
#     return {'data': name}
#
#
# @app.post('/{user_type}')
# def test(user_type: UserType = None):
#     return {'data': UserType.user}
#
#
# Request Body
# class Item(BaseModel):
#     id: int
#     name: str
#     price: float
#
# @app.post('/create')
# def create(item: Item):
#     return item
#
# Request body + path parameters
# class Item(BaseModel):
#     id: int
#     name: str
#     price: float
#
# data = {
#     1: {
#         'id': 1,
#         'name': 'Apple',
#         'price': 10.1,
#     }
# }
# @app.post('/update/{item_id}')
# def update(item: Item, item_id: int):
#     res = item.dict()
#     res['id'] = item_id
#     return res
#
# Request body + path + query parameters
# class Item(BaseModel):
#     id: int
#     name: str
#     price: float
#
# data = {
#     1: {
#         'id': 1,
#         'name': 'Apple',
#         'price': 10.1,
#     }
# }
# @app.post('/update/{item_id}')
# def update(item: Item, item_id: int, name, price: float | None = None):
#     res = item.dict()
#     res['id'] = item_id
#     res['name'] = name
#     res['price'] = price or res['price']
#     return res
#
#
#
# Query Parameters and String Validations
# @app.post('/update/{item_id}')
# def update(item_id: int, name: str, price: float | None = Query(default=..., gt=20)):
#     return {'id': item_id, 'name': name, 'price': price}
#
# Query parameter list / multiple values with defaults
# class Item(BaseModel):
#     id: int
#     name: str
#     price: float
#
#
# @app.post('/update/{item_id}')
# def update(
#         *,
#         item_id: int,
#         name: List | None = Query(default=[], alias='10 sasas'),
#         item: Item,
#         price: float | None = Query(default=..., gt=20)
# ):
#     return {**item.dict(), 'id': item_id, 'name': name, 'price': price}
#
# Multiple body parameters
# class Item(BaseModel):
#     id: int
#     name: str
#     price: float
#
# class User(BaseModel):
#     id: int
#     name: str
#
# @app.post('/create')
# def create(
#         item: Item,
#         user: User,
# ):
#     return {'user_data': user.dict(), 'item_data': item.dict()}
#
# Singular values in body
# class Item(BaseModel):
#     id: int
#     name: str
#     price: float
#
# class User(BaseModel):
#     id: int
#     name: str
#
# @app.post('/create')
# def create(
#         item: Item,
#         user: User,
#         importance: str = Body()
# ):
#     return {'user_data': user.dict(), 'item_data': item.dict(), 'extra_data': {'importance': importance}}

# Embed a single body parameter: To take dic with name of argument
# class Item(BaseModel):
#     id: int
#     name: str
#     price: float
#
# class User(BaseModel):
#     id: int
#     name: str
#
# @app.post('/create')
# def create(
#         *,
#         item: Item = Body(embed=True),
#         # user: User = Body(embed=True),
#         importance: str
# ):
#     return {'item_data': item.dict(), 'extra_data': {'importance': importance}}
#
#
# Body - Fields
# class Item(BaseModel):
#     id: int
#     name: str = Field(default='-', min_length=20)
#     price: float
#
# @app.post('/create')
# def create(
#         *,
#         item: Item,
#         importance: str
# ):
#     return {'item_data': item.dict(), 'extra_data': {'importance': importance}}
#
#
# Body - Nested Models
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = []
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, "item": item}
#
# Nested Models and Bodies of pure lists
# class Image(BaseModel):
#     url: str
#     name: str
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()
#     image: list[Image] | None = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, "item": item}
#
# @app.put("/items")
# async def create_item(item: list[Item]):
#     return {"item": item}
#
# Declare Request Example Data
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Foo",
#                 "description": "A very nice Item",
#                 "price": 35.4,
#                 "tax": 3.2,
#             }
#         }
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, "item": item}
#
# Extra Data Types
# @app.put("/create")
# async def create(item: datetime.date = Body(embed=True, alias='Purchase date')):
#     return {"item": item}
#
# Cookie Parameters
# @app.get("/items/")
# async def read_items(ads_id: str | None = Cookie(default=None)):
#     return {"ads_id": ads_id}
#
# Header Parameters
# @app.get("/items/")
# async def read_items(user_agent: str | None = Header(default=None), csrftoken: str | None = Cookie(default=None)):
#     return {"User-Agent": user_agent, 'csrftoken': csrftoken}
#
# @app.get("/items/")
# async def read_items(x_token: list[str] | None = Header(default=None)):
#     return {"X-Token values": x_token}
#
# Response Model - Return Type¶
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: list[str] = []
#
#
# @app.post("/items/")
# async def create_item(item: Item) -> Item:
#     return item
#
#
# @app.get("/items/")
# async def read_items() -> list[Item]:
#     return [
#         Item(name="Portal Gun", price=42.0),
#         Item(name="Plumbus", price=32.0),
#     ]
#
# Add an output model
# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None
#
#
# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None
#
#
# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn) -> Any:
#     return user

# This will not work
# @app.get("/portal")
# async def get_portal(teleport: bool = False) -> Response | dict:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return {"message": "Here's your interdimensional portal."}

# But this will work
# @app.get("/portal", response_model=None)
# async def get_portal(teleport: bool = False) -> Response | dict:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return {"message": "Here's your interdimensional portal."}


# Response Model encoding parameters¶
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float = 10.5
#     tags: list[str] = []
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }
#
# # This will pass all whether key have value or not
# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items[item_id]
#
# @app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
# async def read_item(item_id: str):
#     return items[item_id]
#
# Form Data
# @app.post("/login/")
# async def login(username: str = Form(), password: str = Form()):
#     return {"username": username, 'password': password}
#
# File Uploading
# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     # print(file)
#     with open("my_file.docx", "wb") as binary_file:
#         # Write bytes to file
#         binary_file.write(file)
#     return {"file_size": len(file)}
#
#
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     # contents = await file.read()
#     # print(contents)
#     return {"filename": file.filename, 'size': file.size}
#
# @app.post("/files/")
# async def create_files(files: list[bytes] = File()):
#     return {"file_sizes": [len(file) for file in files]}
#
#
# @app.post("/uploadfiles/")
# async def create_upload_files(files: list[UploadFile]):
#     return {"filenames": [file.filename for file in files]}
#
#
# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)
#
# @app.post("/files/")
# async def create_file(
#     file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
# ):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#     }
#
# Handling Errors
# items = {"foo": "The Foo Wrestlers"}
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"item": items[item_id]}
#
# items = {"foo": "The Foo Wrestlers"}
# @app.get("/items-header/{item_id}")
# async def read_item_header(item_id: str):
#     if item_id not in items:
#         raise HTTPException(
#             status_code=404,
#             detail="Item not found",
#             headers={"X-Error": "There goes my error"},
#         )
#     return {"item": items[item_id]}

# custom exception handlers
# class UnicornException(Exception):
#     def __init__(self, name: str):
#         self.name = name
#
# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
#     )
#
# @app.get("/unicorns/{name}")
# async def read_unicorn(name: str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name": name}
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
#     return {"item_id": item_id}

# Tags
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()
#
#
# @app.post("/items/", response_model=Item, tags=["items"])
# async def create_item(item: Item):
#     return item
#
#
# @app.get("/items/", tags=["items"])
# async def read_items():
#     return [{"name": "Foo", "price": 42}]
#
#
# @app.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "johndoe"}]

# class Tags(Enum):
#     items = "items"
#     users = "users"
#
#
# @app.get("/items/", tags=[Tags.items])
# async def get_items():
#     return ["Portal gun", "Plumbus"]
#
#
# @app.get("/users/", tags=[Tags.users])
# async def read_users():
#     return ["Rick", "Morty"]

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()
#
#
# @app.post(
#     "/items/",
#     response_model=Item,
#     summary="Create an item",
#     description="Create an item with all the information, name, description, price, tax and a set of unique tags",
# )
# async def create_item(item: Item):
#     return item

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()
#
#
# @app.post("/items/", response_model=Item, summary="Create an item")
# async def create_item(item: Item):
#     """
#     Create an item with all the information:
#
#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if the item doesn't have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item

# JSON Compatible Encoder
# fake_db = {}
#
#
# class Item(BaseModel):
#     title: str
#     timestamp: datetime.datetime
#     description: str | None = None
#
# @app.put("/items/{id}")
# def update_item(id: str, item: Item):
#     json_compatible_item_data = jsonable_encoder(item)
#     fake_db[id] = json_compatible_item_data
#     print(json_compatible_item_data)

# Body - Updates
# class Item(BaseModel):
#     name: str | None = None
#     description: str | None = None
#     price: float | None = None
#     tax: float = 10.5
#     tags: list[str] = []
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }
#
#
# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items[item_id]
#
#
# @app.put("/items/{item_id}", response_model=Item)
# async def update_item(item_id: str, item: Item):
#     update_item_encoded = jsonable_encoder(item)
#     items[item_id] = update_item_encoded
#     print(update_item_encoded)
#     return update_item_encoded

# Partial updates
# class Item(BaseModel):
#     name: str | None = None
#     description: str | None = None
#     price: float | None = None
#     tax: float = 10.5
#     tags: list[str] = []
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }
#
#
# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items[item_id]
#
#
# @app.patch("/items/{item_id}", response_model=Item)
# async def update_item(item_id: str, item: Item):
#     stored_item_data = items[item_id]
#     stored_item_model = Item(**stored_item_data)
#     update_data = item.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(updated_item)
#     return updated_item

# Dependency Injection
# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100, extra: dict = Body()):
#     return {"q": q, "skip": skip, "limit": limit, "extra": extra}
#
# @app.get("/items/")
# async def read_items(commons: dict = Depends(common_parameters)):
#     return commons
#
#
# @app.post("/users/")
# async def read_users(commons: dict = Depends(common_parameters), extra: dict = Body()):
#     print(extra)
#     return commons

# Oauth2: without security
# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }
#
# def fake_hash_password(password: str):
#     return f"fakehashed{password}"
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def fake_decode_token(token):
#     return get_user(fake_users_db, token)
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if hashed_password != user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}
#
#
# @app.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# Oauth2: with security and cors with middleware
# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     print('add_process_time_header starts')
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     print(f'add_process_time_header :: {process_time}')
#     response.headers["X-Process-Time"] = str(process_time)
#     print('add_process_time_header ends')
#     return response
#
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }
#
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# class TokenData(BaseModel):
#     username: str | None = None
#
#
# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# app = FastAPI()
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
#     else:
#         expire = datetime.datetime.now(
#             datetime.timezone.utc
#         ) + datetime.timedelta(minutes=15)
#     to_encode["exp"] = expire
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError as e:
#         raise credentials_exception from e
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
#
#
# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()





