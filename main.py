from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]


my_posts = [
    {
        "title": "title of the post 1",
        "content": "content of post 1",
        "publised": True,
        "id": 1,
    },
    {"title": "Favourite food", 
     "content": "Pizza", 
     "publised": True, 
     "id": 2},
]

def find_post(post_id):
    for p in my_posts:
        if p["id"] == post_id:
            return p
    raise HTTPException(status_code=404, detail="There is no post at this URL")    


@app.get("/")
def root():
    return {"message": "Welcome to this FAST API Project!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()  # using model_dump instead of dict
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}



#to get a post by id search through my_post via id to get the specific post
@app.get('/posts/{post_id}')
def get_post(post_id: str):
    post = find_post(post_id)
    return {"post_details":post}
    
    



# Title str, Content str(we want just two things from user!)
