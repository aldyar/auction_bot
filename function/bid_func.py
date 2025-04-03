from database.models import async_session
from database.models import User,Bid,ActiveBid
from sqlalchemy import select, update, delete, desc
from decimal import Decimal
from datetime import datetime

def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


@connection
async def get_bid(session):
    bid = await session.scalar(select(Bid))
    return bid


@connection
async def buy_bid(session, tg_id, bid_id):
    bid = await session.scalar(select(Bid).where(Bid.id == bid_id))

    if not bid:
        return


    bid.tg_id = tg_id
    bid.bot_taken = 'sold'
    
    await session.flush()  # Принудительно отправить изменения в БД
    await session.commit()



@connection
async def set_active_bid(session,bid_id,start,blitz):
    new_active_bid = ActiveBid(
        bid_id = bid_id,
        start_price = start,
        blitz_price=blitz,
        current_price = start
    )
    session.add(new_active_bid)
    await session.commit()


@connection
async def update_active_bid(session,bid_id,tg_id,current):
    active_bid = await session.scalar(select(ActiveBid).where(ActiveBid.bid_id == bid_id))
    if active_bid:
        active_bid.tg_id = tg_id
        active_bid.current_price += current
        active_bid.updated_at = datetime.now()
        await session.commit()

    
@connection
async def delete_active_bid(session,bid_id):
    active_bid = await session.scalar(select(ActiveBid).where(ActiveBid.bid_id == bid_id))
    if active_bid:
        await session.delete(active_bid)
        await session.commit()


@connection
async def get_active_bid(session,bid_id):
    bid = await session.scalar(select(ActiveBid).where(ActiveBid.bid_id == bid_id))
    if bid.tg_id:
        return bid.tg_id
    else:
        return False