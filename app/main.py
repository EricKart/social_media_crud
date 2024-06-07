from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


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
        print("Erros: ", error)
        time.sleep(3)
    finally:
        print("Attempt to connect has completed.")


#####-----------Schema------------------------


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]


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
def get_posts():
    cursor.execute("""select *from posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


# -------/posts path to create post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """insert into posts (title, content, published) values(%s, %s, %s) returning*""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# to get a post by id search through my_post via id to get the specific post
@app.get("/posts/{post_id}")
def get_post(post_id: str):
    cursor.execute("""select *from posts where id = %s""", (str(post_id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} is not found!",
        )
    return {"post_details": post}


# Deleting the post-----


@app.delete("/posts/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):

    cursor.execute(
        """delete from posts where id = %s returning*""",
        (str(post_id)),
    )
    delete_post = cursor.fetchone()
    conn.commit()

    if delete_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found!",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---Update the post


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    cursor.execute(
        """
        UPDATE posts 
        SET title = %s, content = %s, published = %s 
        WHERE id = %s 
        RETURNING *;
        """,
        (post.title, post.content, post.published, post_id),
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} does not exist!",
        )

    return {"message": "Post has been updated", "updated_post": updated_post}


# Title str, Content str(we want just two things from user!)
