from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models import User, Post
from app.schemas.post import PostPublic, PostCreate

router = APIRouter(tags=["posts"])


@router.get("/users/{username}/posts", response_model=list[PostPublic])
def get_user_posts(username: str, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    posts = db.scalars(
        select(Post)
        .where(Post.user_id == user.id)
        .order_by(Post.created_at.desc())
    ).all()
    return posts


# Create a post for a specific user
@router.post(
    "/users/{username}/posts",
    response_model=PostPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_post(username: str, payload: PostCreate, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    post = Post(
        user_id=user.id,
        title=payload.title,
        content=payload.content,
        image_url=payload.image_url,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# Like a post
@router.post("/posts/{post_id}/like", response_model=PostPublic)
def like_post(post_id: int, db: Session = Depends(get_db)):
    post = db.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    post.likes_count += 1
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
