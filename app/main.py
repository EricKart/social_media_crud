from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


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


#####-----------Schema------------------------




my_posts = [
    {
        "title": "title of the post 1",
        "content": "content of post 1",
        "published": True,
        "id": 1,
    },
    {"title": "Favourite food", "content": "Pizza", "published": True, "id": 2},
]


########


def find_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    return None


def find_index_post(post_id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == post_id:
            return i
    return None


###Root path


@app.get("/")
def root():
    return {"message": "Welcome to this FAST API Project!"}


# /posts path to retrieve post


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""select *from posts""")
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(models.Post).all()
    return {"data": posts}


# -------/posts path to create post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """insert into posts (title, content, published) values(%s, %s, %s) returning*""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    post_data = post.model_dump(exclude_unset=True)
    # post_data.pop('rating', None)  # Remove rating if it is not a part of the model
    new_post = models.Post(**post_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


# to get a post by id search through my_post via id to get the specific post
@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} is not found!",
        )
    return {"post_details": post}

    # if not post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {post_id} is not found!",
    #     )
    # return {"post_details": post}


# Deleting the post-----


@app.delete("/posts/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """delete from posts where id = %s returning*""",
    #     (str(post_id)),
    # )
    # delete_post = cursor.fetchone()
    # conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if delete_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found!",
        )
    db.delete(delete_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---Update the post


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: schemas.Post, db:Session=Depends(get_db)):
    # cursor.execute(
    #     """
    #     UPDATE posts 
    #     SET title = %s, content = %s, published = %s 
    #     WHERE id = %s 
    #     RETURNING *;
    #     """,
    #     (post.title, post.content, post.published, post_id),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id==post_id).first()
    

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} does not exist!",
        )
    for key, value in post.model_dump(exclude_unset=True).items():
        setattr(updated_post, key, value)

    # Commit the changes to the database
    db.commit()
    db.refresh(updated_post)

    # Return the updated post
    return {"data": updated_post}



# Title str, Content str(we want just two things from user!)
