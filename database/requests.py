from database.models import async_session
from database.models import User
from sqlalchemy import select, update, delete, desc
from decimal import Decimal
from datetime import datetime

def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


@connection
async def set_user(session, tg_id,name):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(
            tg_id=tg_id,
            name = name))
        await session.commit()

@connection
async def get_user(session,tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    return user

#get_all users

