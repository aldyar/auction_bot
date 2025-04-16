from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from app.states import InvalidBid
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from function.bid_func import BidFunction as Bid
from function.user_func import UserFunction as User
from function.order_func import OrderFunction as Order
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
    tg_id = callback.from_user.id
    orders = await Order.get_orders_by_userid(tg_id)
    await callback.answer()
    if not orders:
        await callback.message.answer("У вас нет пополнений.")
        return

    for order in orders:
        date = order.processed_at.strftime('%Y-%m-%d %H:%M') if order.processed_at else '—'

        text = (
            f"*🆔 Заявка №:* `{order.id}`\n"
            #f"*👤 ID Заявки:* `{order.telegram_payment_id}`\n"
            f"*💳 Сумма:* *{order.amount}*\n"
            f"*⏱ Дата:* _{date}_\n"
        )

        await callback.message.answer(text, parse_mode='Markdown')