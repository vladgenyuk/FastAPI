from typing import List
from fastapi import FastAPI, Depends, UploadFile
from sqlalchemy.orm import Session
from database import database
import models, schemas

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/home')
async def home():
    response = {'key': 'Hello!'}
    return response


@app.post("/items_create/", response_model=schemas.Item)
async def create_note(item: schemas.ItemCreate):
    query = models.Items.insert().values(title=item.title, description=item.description)
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}


@app.get('/items', response_model=List[schemas.Item])
async def get_all_items():
    query = models.Items.select()
    return await database.fetch_all(query)


@app.post('/cat_create', response_model=schemas.Category)
async def create_cat(cat: schemas.CategoryCreate):
    query = models.Categories.insert().values(title=cat.title)
    last_record_id = await database.execute(query)
    return {**cat.dict(), "id": last_record_id}


@app.get('/categories', response_model=List[schemas.Category])
async def get_cat():
    query = models.Categories.select()
    return await database.fetch_all(query)


@app.post('/file_create')
async def create_file(file: UploadFile):
    file_id = hash(file.filename)
    address = 'D:\FastAPI\MyApp\media\\' + file.filename
    query = models.Files.insert().values(address=address, file_id=str(file_id), filename=file.filename)
    last_record_id = await database.execute(query)
    with open(address, 'wb') as f:
        f.write(await file.read())
    return {"id": last_record_id, 'filename': file.filename, 'Success': True}


