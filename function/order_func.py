from database.models import async_session
from database.models import User,Bid,ActiveBid,BidInvalid,Order
from sqlalchemy import select, update, delete, desc,distinct
from decimal import Decimal
from datetime import datetime

def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner

class OrderFunction:
    

    @connection
    async def create_order(session, tg_id, tg_order_id, provider_id, amount):
        new_order = Order(
            tg_id = tg_id,
            telegram_payment_id = tg_order_id,
            provider_payment_id = provider_id,
            amount = amount,
            processed_at = datetime.now()
        )
        session.add(new_order)
        await session.commit()


    @connection
    async def add_balance(session,tg_id,amount):
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.balance += amount
            await session.commit()