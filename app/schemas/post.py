from datetime import datetime
from pydantic import BaseModel

class PostPublic(BaseModel):
    id: int
    title: str
    content: str
    image_url: str | None
    likes_count: int
    created_at: datetime

    class Config:
        from_attributes = True
