from database.models import async_session
from database.models import User,Bid,ActiveBid,BidInvalid
from sqlalchemy import select, update, delete, desc
from decimal import Decimal
from datetime import datetime

def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


class AdminFunction:

    @connection
    async def set_ban_user(session,tg_id,change):
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if change == 1:
            user.is_banned = True
        elif change == 0:
            user.is_banned = False
        
        await session.commit()