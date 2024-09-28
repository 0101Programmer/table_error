from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import *
from app.models import User
from app.schemas import CreateUser, UpdateUser, CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    usr = db.scalars(select(User).where(User.id == user_id))
    if usr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такого пользователя не найдено'
        )
    else:
        return usr


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_us: CreateUser):
    db.execute(insert(User).values(username=create_us.username,
                                   firstname=create_us.firstname,
                                   lastname=create_us.lastname,
                                   age=create_us.age,
                                   slug=slugify(create_us.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_us: UpdateUser):
    usr = db.scalar(select(User).where(User.id == user_id))
    if create_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такого пользователя не найдено'
        )
    db.execute(update(User).where(User.id == user_id).values(
        username=update_us.username,
        firstname=update_us.firstname,
        lastname=update_us.lastname,
        age=update_us.age)
    )


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    usr = db.scalar(select(User).where(User.id == user_id))
    if create_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такого пользователя не найдено'
        )

