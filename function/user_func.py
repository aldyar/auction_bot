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

class UserFunction:
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

    @connection
    async def get_user_bid_history(session,tg_id):
        bids = await session.scalars(select(Bid).where(Bid.tg_id == tg_id,Bid.valid == 1).order_by(desc(Bid.id)))
        return bids