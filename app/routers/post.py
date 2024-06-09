from .. import models, schemas, utils
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts" ,
    tags =  ["Posts"],
)



@router.get("/", response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""select *from posts""")
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(models.Post).all()
    return posts


# -------/posts path to create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):
    post_data = post.model_dump(exclude_unset=True)
    # post_data.pop('rating', None)  # Remove rating if it is not a part of the model
    new_post = models.Post(**post_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# to get a post by id search through my_post via id to get the specific post
@router.get("/{post_id}" , response_model= schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} is not found!",
        )
    return post


# Deleting the post-----
@router.delete("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
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
@router.put("/{post_id}",  response_model= schemas.Post)
def update_post(post_id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == post_id).first()

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
    return updated_post