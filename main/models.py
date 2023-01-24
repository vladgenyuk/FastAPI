from pydantic import BaseModel


class Man(BaseModel):
    id: int
    name: str
    email: str


class Image(BaseModel):
    file: str
    desc: str


class Item(BaseModel):
    name: str
    price: float
    images: list[Image] | None = None


class PlaneItem(Item):
    tax: float | None = None


class CarItem(Item):
    taxi: float = 11.22