from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from app.states import InvalidBid
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from function.bid_func import BidFunction as Bid
from function.user_func import UserFunction as User
from aiogram.enums import ChatAction
from aiogram import Bot

user = Router()


@user.message(F.text == '➕Пополнить баланс')
async def add_funds_handler(message:Message):
    await message.answer('Заглушка')