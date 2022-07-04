from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import crud, models

import secrets
import datetime

def get_current_user_from_token(db: Session, access_token: str):
    """tokenからユーザーを取得"""
    now_at = datetime.datetime.now()
    db_token = crud.get_token(db, access_token)
    if db_token is None:
        raise HTTPException(status_code=401, detail='Unauthorized')
    elif db_token.expiration_at < now_at:
        raise HTTPException(status_code=401, detail=f'Unauthorized')
    db_user = crud.get_user(db, user_id=db_token.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def authenticate(db: Session, email: str, password: str):
    """パスワード認証し、userを返却"""
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if db_user.hashed_password != password + "notreallyhashed":
        raise HTTPException(status_code=401, detail='Unauthorized')
    return db_user


def create_tokens(db: Session, user_id: int):
    """パスワード認証を行い、トークンを生成"""
    access_token = secrets.token_hex()
    expiration_at = datetime.datetime.now() + datetime.timedelta(hours=1)
    db_token = crud.get_token_by_user(db, user_id=user_id)
    if db_token is None:
        """ tokenを作成 """
        db_token = models.Token(
            access_token=access_token,
            expiration_at=expiration_at,
            user_id=user_id
            )
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
    else:
        """ tokenを更新 """
        db_token.access_token = access_token
        db_token.expiration_at = expiration_at
        db.commit()
        db.refresh(db_token)
    return {'access_token': db_token.access_token,'expiration_at': str(db_token.expiration_at)}