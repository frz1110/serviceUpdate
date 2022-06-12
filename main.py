from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import databases
import sqlalchemy

DATABASE_URL = "sqlite:///../store.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

mahasiswa = sqlalchemy.Table(
    "mahasiswa",
    metadata,
    sqlalchemy.Column("npm", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("nama", sqlalchemy.String),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"message": "Welcome"}

@app.post("/update")
async def update_npm(npm: str, nama: str):
    query = mahasiswa.insert().values(npm=npm, nama=nama)
    await database.execute(query)
    return {"status":"OK"}
