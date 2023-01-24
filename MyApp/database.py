import databases
import sqlalchemy

DB_INFO = 'postgresql://postgres:qseawdzxc1@localhost:5432/Psyc_lesson_1'

database = databases.Database(DB_INFO)

metadata = sqlalchemy.MetaData()


engine = sqlalchemy.create_engine(
    DB_INFO,
)

metadata.create_all(engine)
