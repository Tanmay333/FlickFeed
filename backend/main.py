from fastapi import FastAPI
from backend.database import Base, engine
from backend.routes import auth_routes, feed_routes

# ✅ Create FastAPI instance (Only Once!)
app = FastAPI()

# ✅ Create database tables (if not exists)
Base.metadata.create_all(bind=engine)

# ✅ Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(feed_routes.router, prefix="/feeds", tags=["Feeds"])

@app.get("/")
def home():
    return {"message": "Welcome to FlickFeed API!"}
