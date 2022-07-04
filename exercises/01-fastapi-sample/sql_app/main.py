from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session

from . import crud, models, schemas, auth
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

depends_db = Depends(get_db)


@app.get("/health-check")
def health_check(db: Session = depends_db):
    return {"status": "ok"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = depends_db):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    users = crud.create_user(db=db, user=user)
    return users


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, X_API_TOKEN: Optional[str] = Header(None), db: Session = depends_db):
    auth_user = auth.get_current_user_from_token(db, X_API_TOKEN)
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, X_API_TOKEN: Optional[str] = Header(None), db: Session = depends_db):
    auth_user = auth.get_current_user_from_token(db, X_API_TOKEN)
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, X_API_TOKEN: Optional[str] = Header(None), db: Session = depends_db
):
    auth_user = auth.get_current_user_from_token(db, X_API_TOKEN)
    items = crud.create_user_item(db=db, item=item, user_id=user_id)
    return items


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, X_API_TOKEN: Optional[str] = Header(None), db: Session = depends_db):
    auth_user = auth.get_current_user_from_token(db, X_API_TOKEN)
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/me/items", response_model=List[schemas.Item])
def read_own_items(skip: int = 0, limit: int = 100, X_API_TOKEN: Optional[str] = Header(None), db: Session = depends_db):
    """リクエストユーザーのitemを取得"""
    auth_user = auth.get_current_user_from_token(db, X_API_TOKEN)
    items = crud.get_items_by_user(db, user_id=auth_user.id, skip=skip, limit=limit)
    return items


@app.post("/token", response_model=schemas.Token)
def issue_token(user: schemas.UserLogin, db: Session = depends_db):
    """ユーザー認証を行いトークン発行（有効期限1時間）"""
    db_user = auth.authenticate(db, user.email, user.password)
    token = auth.create_tokens(db, db_user.id)
    return token


@app.get("/users/{user_id}/delete", response_model=schemas.User)
def delete_user(user_id: int, X_API_TOKEN: Optional[str] = Header(None), db: Session = depends_db):
    """ユーザーを削除"""
    auth_user = auth.get_current_user_from_token(db, X_API_TOKEN)
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = crud.delete_user(db, db_user=db_user)
    return db_user
