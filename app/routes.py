from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, delete
from app.config.database import async_session_maker 
from app.models import User
from app.pyd import UserBase


router = APIRouter(prefix='/users', tags=['Auth app'])

@router.post("/create", summary="Создать нового пользователя")
async def create_user(user_create: UserBase):
    async with async_session_maker() as session:
        user = await session.execute(
            select(User).where(User.phone == user_create.phone)
        )
        user = user.scalars().first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким номером телефона уже существует"
                )
        new_user = User(
            phone=user_create.phone,
            firstname=user_create.firstname,
            lastname=user_create.lastname
            )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)  # Обновление объекта после коммита
        
        return new_user
    

@router.get("/get/{phone}", summary="Получить данные пользователя")
async def get_user(phone: str):
    async with async_session_maker() as session:
        query = select(User).where(User.phone == phone)
        result = await session.execute(query)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден")
        
        return user
    

@router.put("/update/{phone}", summary="Изменить данные пользователя")
async def get_user(phone: str, 
                   firstname: str | None = Query(default=None), 
                   lastname: str | None = Query(default=None)):
    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.phone == phone))
        user = user.scalars().first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден")
        
        if firstname is not None:
            user.firstname = firstname
        if lastname is not None:
            user.lastname = lastname

        await session.commit()
        await session.refresh(user)

        return user
    

@router.delete("/delete/{phone}", summary="Удалить пользователя")
async def delete_user(phone: str):
    async with async_session_maker() as session:
        user = await session.execute(
            select(User).where(User.phone == phone)
        )
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не существует")
        
        query = delete(User).where(User.phone == phone)
        await session.execute(query)
        await session.commit()