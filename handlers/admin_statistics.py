from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command,CommandStart
from aiogram.fsm.context import FSMContext
from config import ADMIN
from function.bid_func import BidFunction as Bid
import app.keyboards as kb
from handlers.user_group import timer
from aiogram import Bot

admin = Router()


class Admin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in ADMIN
    

@admin.message(Admin(),F.text == 'Статистика')
async def admin_stat_handler(message:Message):
    await message.answer('Заглушка')