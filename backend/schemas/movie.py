from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    genre: str
    release_year: int

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int

    class Config:
        from_attributes = True  # Ensures proper ORM conversion
