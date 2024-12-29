from fastapi import FastAPI
import models
from database import engine
from router import blog, authentication,user,auth_token,upload
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


models.Blog.metadata.create_all(bind=engine)

# For Routing 
app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth_token.router)
app.include_router(upload.router)



app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

