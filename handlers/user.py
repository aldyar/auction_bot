from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from app.states import Chat, Image
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from database.requests import set_user,get_user
from aiogram.enums import ChatAction
from aiogram import Bot

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await set_user(message.from_user.id,message.from_user.username)
    await message.answer('🤖 Добро пожаловать!',reply_markup=kb.user_menu)


@user.message(F.text == 'test')
async def test(message:Message):
    user = await get_user(message.from_user.id)
    await message.answer(f'Balance: {user.balance} , ID: {user.tg_id}')


"""@user.message(F.text == 'Баланс')
async def ()"""