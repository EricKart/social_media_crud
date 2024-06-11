from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings

settings.database_password     


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


###Root path
@app.get("/")
def root():
    return {"message": "Welcome to this FAST API Project!"}
