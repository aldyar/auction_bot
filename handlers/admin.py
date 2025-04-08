from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command,CommandStart
from aiogram.fsm.context import FSMContext
from config import ADMIN
from function.bid_func import BidFunction as Bid
from function.user_func import UserFunction as User
import app.keyboards as kb
from aiogram import Bot
from app.states import Admin as AdminState
from function.admin_func import AdminFunction
admin = Router()


class Admin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in ADMIN
    

@admin.message(Admin(), CommandStart())
async def admin_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Добро пожаловать в панель администратора',reply_markup=kb.admin_menu)


@admin.message(Admin(),F.text == 'Управление пользователями')
async def user_manage_handler(message:Message):
    users = await User.get_all_users()
    user_count = len(users.all())
    await message.answer(f"🧾*Общее количество пользователей:* {user_count}\n\n"
                         "*Поиск пользователя происходит по его username без@*",reply_markup=kb.admin_search_user,parse_mode='Markdown')


@admin.callback_query(Admin(),F.data == 'SearchUser')
async def searc_user_handler(callback:CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('*Введите имя пользователя...*',parse_mode='Markdown')
    await state.set_state(AdminState.wait_username)


@admin.message(AdminState.wait_username)
async def process_username_hanler(message:Message,state:FSMContext):
    username = message.text
    user = await User.get_user_by_username(username)
    if not user:
        await state.clear()
        return await message.answer('Пользоветль не был найден')
    register_date = user.register_date.strftime("%d-%m-%Y %H:%M:%S") if user.register_date else 'Не указано'
    if user.is_banned:
        ban_status = "🚫 Заблокирован"
    else:
        ban_status = "✅ Не заблокирован"
    text = (
        f"👤 Имя: {user.name or 'Не указано'}\n"
        f"🆔 Telegram ID: {user.tg_id}\n"
        f"💰 Баланс: {user.balance:.2f} ₽\n"
        f"📅 Дата регистрации: {register_date}\n"
        f"{ban_status}\n"
    )
    keyboard = await kb.admin_block_unlock_user(user.tg_id)
    await message.answer(text,reply_markup=keyboard)
    await state.clear()


@admin.callback_query(F.data.startswith ('unlock_'))
async def unlock_handler(callback:CallbackQuery):
    user_id = callback.data.split("_")[1]
    user = await User.get_user(user_id)
    if user.is_banned == False:
        return await callback.answer("Пользователь не заблокирован")
    else:
        await AdminFunction.set_ban_user(user_id,0)
        await callback.message.delete()
        await callback.message.answer(f'✅*Пользователь* {user_id} * был разблокирован*',parse_mode='Markdown')


@admin.callback_query(F.data.startswith ('block'))
async def block_handler(callback:CallbackQuery):
    user_id = callback.data.split("_")[1]
    user = await User.get_user(user_id)
    if user.is_banned == True:
        return await callback.answer("Пользователь уже заблокирован")
    else:
        await AdminFunction.set_ban_user(user_id,1)
        await callback.message.delete()
        await callback.message.answer(f'✅*Пользователь* {user_id} * был заблокирован*',parse_mode='Markdown')