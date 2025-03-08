from fastapi import FastAPI 
from backend.database import Base,engine  
from backend.routes import auth_routes, feed_routes, user_routes


app = FastAPI()


#  Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(feed_routes.router, prefix="/feeds", tags=["Feeds"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Welcome to FlickFeed!"}