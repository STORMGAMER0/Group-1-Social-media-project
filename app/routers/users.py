# app/api/routes/users.py (where your user routes are)

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.session import get_db
from app.models import User, Post
from app.schemas.user import UserCreate, UserPublic, UserList
from app.schemas.post import PostPublic, PostCreate   # ✅ import PostCreate
from app.core.security import hash_password

router = APIRouter(tags=["users"])

# ----------------- USERS -----------------

@router.post("/users/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db.scalar(select(func.count()).select_from(User).where(User.username == payload.username)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    if payload.email and db.scalar(select(func.count()).select_from(User).where(User.email == payload.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    user = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users/", response_model=UserList)
def list_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    total = db.scalar(select(func.count()).select_from(User)) or 0
    items = db.scalars(select(User).order_by(User.id).offset(skip).limit(limit)).all()
    return {"items": items, "total": total}


@router.get("/users/{username}", response_model=UserPublic)
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# ----------------- POSTS -----------------

@router.get("/users/{username}/posts", response_model=list[PostPublic])
def get_user_posts(username: str, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    posts = db.scalars(
        select(Post).where(Post.user_id == user.id).order_by(Post.created_at.desc())
    ).all()
    return posts


@router.post("/users/{username}/posts", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(username: str, payload: PostCreate, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

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

@router.post("/posts/{post_id}/like", response_model=PostPublic)
def like_post(post_id: int, db: Session = Depends(get_db)):
    post = db.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.likes_count += 1
    db.add(post)
    db.commit()
    db.refresh(post)
    return post