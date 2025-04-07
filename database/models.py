from sqlalchemy import ForeignKey, String, BigInteger, DateTime, Boolean, Float, Integer, Text,text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime
from config import DB_LINK

#engine = create_async_engine(url='mysql+aiomysql://root:1234@localhost/auction_db', echo=True)  
engine = create_async_engine(DB_LINK, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    tg_id: Mapped[int] = mapped_column(BigInteger,primary_key=True)
    balance: Mapped[int] = mapped_column(Float, default=0)
    name : Mapped[str] = mapped_column(String(32),nullable=True)


class Bid(Base):
    __tablename__ = 'bids'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    request_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    request_type: Mapped[str] = mapped_column(String(50), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    start_price: Mapped[int] = mapped_column(Integer, nullable=False)
    blitz_price: Mapped[int] = mapped_column(Integer, nullable=True)
    valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    bot_taken: Mapped[str] = mapped_column(String(20), nullable=True)
    sold_price: Mapped[int] = mapped_column(Integer,nullable=True)  


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)  # ID счета Cryptomus
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Статус платежа
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)  # ID пользователя
    amount: Mapped[str] = mapped_column(String(15), nullable=False)  # Сумма платежа
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)  # Обработан ли платеж
    processed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class BidInvalid(Base):
    __tablename__ = 'bids_invalid'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    request_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    request_type: Mapped[str] = mapped_column(String(50), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    start_price: Mapped[int] = mapped_column(Integer, nullable=False)
    blitz_price: Mapped[int] = mapped_column(Integer, nullable=True)
    sold_price: Mapped[int] = mapped_column(Integer,nullable=True)  
    invalid_reason: Mapped[str] = mapped_column(Text)   

    
class ActiveBid(Base):
    __tablename__ = 'active_bid'

    bid_id: Mapped[int] = mapped_column(Integer,primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    current_price: Mapped[int] = mapped_column(Integer,nullable=True)
    start_price: Mapped[int] = mapped_column(Integer, nullable=False)  # Начальная цена
    blitz_price: Mapped[int] = mapped_column(Integer, nullable=True)  # Блиц-цена (если есть)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True )  # Дата последнего обновления


# class BidHistory(Base):
#     __tablename__ = 'bids_history'

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     tg_id: Mapped[int] = mapped_column(BigInteger)
#     price:Mapped[int] = mapped_column(Integer)
#     full_name: Mapped[str] = mapped_column(String(255), nullable=False)
#     phone: Mapped[str] = mapped_column(String(20), nullable=False)
#     request_type: Mapped[str] = mapped_column(String(50), nullable=False)
#     question: Mapped[str] = mapped_column(Text, nullable=False)
#     category: Mapped[str] = mapped_column(String(100), nullable=False)

    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)