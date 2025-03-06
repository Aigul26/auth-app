from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, delete
from app.config.database import async_session_maker 
from app.models import User
from app.pyd import UserBase


router = APIRouter(prefix='/users', tags=['Auth app'])

@router.post("/create", summary="Создать нового пользователя")
async def create_user(user_create: UserBase):
    async with async_session_maker() as session:
        existing_user = await session.execute(
            select(User).where(User.phone == user_create.phone)
        )
        existing_user = existing_user.scalars().first()
        if existing_user:
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
    

@router.get("/get/{id}", summary="Получить данные пользователя")
async def get_user(id: int):
    async with async_session_maker() as session:
        query = select(User).where(User.id == id)
        result = await session.execute(query)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден")
        
        return user
    

@router.put("/update/{id}", summary="Изменить данные пользователя")
async def update_user(id: int, 
                   firstname: str | None = Query(default=None), 
                   lastname: str | None = Query(default=None)):
    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.id == id))
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
    

@router.delete("/delete/{id}", summary="Удалить пользователя")
async def delete_user(id: int):
    async with async_session_maker() as session:
        existing_user = await session.execute(
            select(User).where(User.id == id)
        )
        if not existing_user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не существует")
        
        query = delete(User).where(User.id == id)
        await session.execute(query)
        await session.commit()