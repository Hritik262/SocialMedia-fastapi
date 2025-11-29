from fastapi import FastAPI, Body,  Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


my_posts = [
    {"id": 1, "title": "title of post 1", "content": "content of post 1", "published": True}, 
    {"id": 2, "title": "title of post 2", "content": "content of post 2", "published": False, "rating": 4}
]

def find(id: int):
    for i in my_posts:
        if i['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello, Hritik"}



# title str, content str
