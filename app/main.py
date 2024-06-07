from fastapi import FastAPI, HTTPException, status, Response
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
        "published": True,
        "id": 1,
    },
    {"title": "Favourite food", 
     "content": "Pizza", 
     "published": True, 
     "id": 2},
]

def find_post(post_id:int):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    return None


def find_index_post(post_id: int):
    for i, p in enumerate(my_posts):
        if p['id'] == post_id:
            return i
    return None

@app.get("/")
def root():
    return {"message": "Welcome to this FAST API Project!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()  # using model_dump instead of dict
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return Response(content= f"Your post: {post_dict} has been Created",status_code=status.HTTP_201_CREATED)



#to get a post by id search through my_post via id to get the specific post
@app.get('/posts/{post_id}')
def get_post(post_id: int):
    post = find_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found!")
    return {"post_details":post}
    

@app.delete("/posts/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    #----Deleting specific post---------#
    #find index in terms of id to delete that post
    # post = find_post(post_id)
    # if post is None:
    #     raise HTTPException(status_code=404, detail="Post not found")
    # my_posts.remove(post)
    # return {"Deleted Details": f"Post with id {post_id} has been deleted! and the post is {post}"}
    #--------Or you can use below code as in below code we are using find_index_post function from above code
    
   index = find_index_post(post_id)
   if index is None:
        raise HTTPException(status_code=404, detail="Post not found!")
   deleted_post = my_posts.pop(index)
   return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    index = find_index_post(post_id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} does not exist!")
    
    # print(f"Updating post at index {index}")  # Debugging print statement
    post_dict = post.model_dump()  # using model_dump instead of dict
    post_dict["id"] = post_id
    my_posts[index] = post_dict
    # print(f"Updated post: {my_posts[index]}")  # Debugging print statement
    
    return {'message': "Post has been updated", 'updated_post': post_dict}

# Title str, Content str(we want just two things from user!)
