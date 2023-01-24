from pydantic import BaseModel


class Item(BaseModel):
    id: int
    title: str
    description: str | None = None


class ItemCreate(BaseModel):
    title: str
    description: str | None = None


class CategoryCreate(BaseModel):
    title: str


class Category(CategoryCreate):
    id: int


class FileCreate(BaseModel):
    address: str
    file_id: str
    filename: str | None = None


class File(FileCreate):
    id: int



