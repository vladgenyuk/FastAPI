from typing import Union, List, Dict
import time
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Body, Query, Path, Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from models import PlaneItem, CarItem, Man, Item

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.middleware("http")
async def Mid(request: Request, call_next):
    now = time.time()
    response = await call_next(request)
    response.headers["X-Time-handling"] = str(time.time() - now)
    return response


@app.get('/linkoleg/{oleg_id}')
def Vega(oleg_id: int):
    return {"key": oleg_id}


item = {
    "One": {"name": "name", "price": 22.2, "images": [{"file": "first", "desc": "one"}], "tax": 55.5},
    "Two": {"name": "2name", "price": 222.2, "tax": 255.5},
}


def fake_hash_password(password: str):
    return "fakehashed" + password


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    }
}


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def update_item(item_id: str, token: str = Depends(oauth2_scheme)):
    return {"item": item[item_id], "token": token}


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


Items = {
    "foo": {"id": 1, "name": "oleg", "email": "@@"},
    "bar": {"id": 2, "name": "Oleg", "email": "@@@"}
}


@app.get("/test/")
async def main1():
    content = """
<body>
<form action="/test1/" enctype="application/x-www-form-urlencoded" method="post">
<h3>var</h3><input name="var" type="text">
<h3>id</h3><input name="id" type="text">
<h3>name</h3><input name="name" type="text">
<h3>email</h3><input name="email" type="text">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


class MyException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(MyException)
async def my_exception_handler(request: Request, exc: MyException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} goes wrong"}
    )


@app.get("/items1/{item_id}")
def ExceptExample(item_id: str):
    if item_id not in Dict:
        raise MyException(name=item_id)
    return {"item": Dict[item_id]}


class NewException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(NewException)
async def new_exception_handler(request: Request, exc: NewException):
    return JSONResponse(
        status_code=418,
        content={"message": f"{exc.name} po pizde"}
    )


@app.post("/test1/")
def main2(id: int = Form(...), name: str = Form(...), email: str = Form(...), var: str = Form(...)):
    if not var in Items:
        raise NewException(name=var)
    old = jsonable_encoder(Items[var])
    Items[var]["id"] = id
    Items[var]["name"] = name
    Items[var]["email"] = email
    new = Items[var]
    return {"old": old, "new": new}


def SubParams(q: str | None = None,):
    return q


class QueryParams:
    def __init__(self, SubParam = Depends(SubParams), name: str | None = None, num: int | None = None):
        self.SubParam = SubParam
        self.name = name
        if SubParam:
            self.name = SubParam
        self.num = num


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/test2/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def main3(Querypar = Depends(QueryParams, use_cache=False)):
    response = {"key": "value"}
    if Querypar.SubParam:
        response.update({"q": Querypar.SubParam})
    response.update({"name": Querypar.name})
    response.update({"num": Querypar.num})
    return response

# uvicorn main:app --reload
