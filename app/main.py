from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

##############-------------DataBase Connection--------------------------------
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="102030",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print(
            "##########_-------------------##########---------Database connection is successful!------------------################"
        )
        break
    except Exception as error:
        print(
            "######################------------------########Connection to Database failed!-----------------"
        )
        print("Errors: ", error)
        time.sleep(3)
    finally:
        print("Attempt to connect has completed.")


app.include_router(post.router)
app.include_router(user.router)

###Root path
@app.get("/")
def root():
    return {"message": "Welcome to this FAST API Project!"}


