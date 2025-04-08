from database.models import async_session
from database.models import User,Bid,ActiveBid,BidInvalid
from sqlalchemy import select, update, delete, desc,distinct
from decimal import Decimal
from datetime import datetime,timedelta

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

    @connection
    async def get_active_users(session):
        # Получаем уникальные tg_id из заявок, где заявка была куплена
        active_tg_ids_result = await session.execute(
            select(distinct(Bid.tg_id)).where(Bid.sold_price.isnot(None))
        )
        active_tg_ids = [row[0] for row in active_tg_ids_result.all() if row[0] is not None]

        if not active_tg_ids:
            return []

        # Теперь находим всех пользователей с этими tg_id
        users_result = await session.execute(
            select(User).where(User.tg_id.in_(active_tg_ids))
        )
        users = users_result.scalars().all()
        return users
    
    @connection
    async def get_sold_bids(session):
        bids = await session.scalars(select(Bid).where(Bid.bot_taken == 'sold'))
        return bids.all()
    
    @connection
    async def get_not_sold_bids(session):
        bids = await session.scalars(select(Bid).where(Bid.bot_taken !=  'sold'))
        return bids.all()

    @connection
    async def get_total_bids_by_period(session, days: int):
        # Рассчитываем дату начала периода
        start_date = datetime.now() - timedelta(days=days)
        
        # Запрос, который фильтрует заявки по дате
        bids = await session.scalars(
            select(Bid).where(Bid.request_date >= start_date)
        )
        return bids.all()
    
    @connection
    async def get_sold_bids_by_period(session, days: int):
        # Рассчитываем дату начала периода
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Запрос, который фильтрует проданные заявки по дате
        sold_bids = await session.scalars(
            select(Bid).where(Bid.bot_taken == 'sold', Bid.sold_date >= start_date)
        )
        return sold_bids.all()
    
    
    @connection
    async def get_users_by_registration_period(session, days: int):
        # Рассчитываем дату начала периода
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Запрос, который фильтрует пользователей по дате регистрации
        users_result = await session.execute(
            select(User).where(User.register_date >= start_date)
        )
        return users_result.scalars().all()


    @connection
    async def get_active_users_by_period(session, days: int):
        # Рассчитываем дату начала периода
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Получаем уникальные tg_id из заявок, где заявка была куплена и в указанном периоде
        active_tg_ids_result = await session.execute(
            select(distinct(Bid.tg_id)).where(Bid.sold_price.isnot(None), Bid.sold_date >= start_date)
        )
        active_tg_ids = [row[0] for row in active_tg_ids_result.all() if row[0] is not None]

        if not active_tg_ids:
            return []

        # Теперь находим всех пользователей с этими tg_id
        users_result = await session.execute(
            select(User).where(User.tg_id.in_(active_tg_ids))
        )
        return users_result.scalars().all()