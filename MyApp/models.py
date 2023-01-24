from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.orm import declarative_base

from database import metadata

Base = declarative_base()


Items = Table(
    "item",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String),
)

Categories = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column('title', String)
)

Files = Table(
    'media',
    metadata,
    Column("id", Integer, primary_key=True),
    Column('address', String),
    Column('file_id', String),
    Column("filename", String)
)

