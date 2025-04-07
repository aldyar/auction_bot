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

class BidFunction:
    @connection
    async def get_bid(session):
        bid = await session.scalar(select(Bid))
        return bid


    @connection
    async def buy_bid(session, tg_id, bid_id,current):
        bid = await session.scalar(select(Bid).where(Bid.id == bid_id))
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not bid:
            return


        bid.tg_id = tg_id
        bid.bot_taken = 'sold'
        user.balance -= current
        
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
        if bid:
            return bid
        else:
            return False
        

    @connection
    async def change_to_invalid_bid(session,bid_id,text):
        bid = await session.scalar(select(Bid).where(Bid.id == bid_id))
        print(f"⏳ Ищем заявку с ID {bid_id}")
        if bid:
            print("✅ Заявка найдена, создаём BidInvalid")
            bid.valid = False
            invalid_bid = BidInvalid(
                    tg_id=bid.tg_id,
                    request_date=bid.request_date,
                    full_name=bid.full_name,
                    phone=bid.phone,
                    request_type=bid.request_type,
                    question=bid.question,
                    category=bid.category,
                    start_price=bid.start_price,
                    blitz_price=bid.blitz_price,
                    sold_price=bid.sold_price,
                    invalid_reason=text  # Добавляем причину из параметра
                )

                # Добавляем объект в сессию и коммитим изменения
            session.add(invalid_bid)
            print("💾 Коммитим изменения...")
            await session.commit()
            print("✅ Готово")


    @connection
    async def get_new_bids(session):
        bid = await session.scalars(select(Bid).where(Bid.bot_taken == 'new'))
        return bid
    
    @connection
    async def get_all_active_bids(session):
        bid = await session.scalars(select(Bid).where(Bid.id == ActiveBid.bid_id))
        return bid.all() 
    
    @connection
    async def get_bid_by_id(session,bid_id):
        bid = await session.scalar(select(Bid).where(Bid.id == bid_id))
        return bid
    
    @connection
    async def bid_taken(session,bid_id):
        bid = await session.scalar(select(Bid).where(Bid.id == bid_id))
        if bid:
            bid.bot_taken = 'taken'
            await session.commet()

    @connection
    async def mark_bid_not_sold(session,bid_id):
        bid = await session.scalar(select(Bid).where(Bid.id == bid_id))
        if bid:
            bid.bot_taken = 'not sold'
            await session.commit()