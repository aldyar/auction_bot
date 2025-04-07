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


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await User.set_user(message.from_user.id,message.from_user.username)
    await message.answer('🤖 Добро пожаловать!',reply_markup=kb.user_menu)


@user.message(F.text == '💵Баланс')
async def balance_handler(message:Message):
    user = await User.get_user(message.from_user.id)
    text = (
        f"👤 Имя: {user.name or 'Не указано'}\n"
        f"🆔 Telegram ID: {user.tg_id}\n"
        f"💰 Баланс: {user.balance:.2f} ₽"
    )
    await message.answer(text,reply_markup=kb.inline_history_topup)


@user.callback_query(F.data == 'history_topup')
async def user_history_popup(callback:CallbackQuery):
    await callback.answer(f'Ваш АЙДИ: {callback.from_user.id} я тута!!!')