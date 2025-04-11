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
from function.order_func import OrderFunction as Order
import json
from app.states import User as UserState

from aiogram.types import LabeledPrice
from aiogram.types import PreCheckoutQuery
from config import PROVIDER_TOKEN

user = Router()


@user.message(F.text == '➕Пополнить баланс')
async def add_funds_handler(message:Message):
    text = (
        "*💳 Пополнение баланса*\n\n"
        "*Вы можете пополнить свой баланс через ЮKassa. Выберите одну из предложенных сумм ниже или введите свою сумму вручную.*\n\n"
        "🔹* Для ввода своей суммы выберите соответсвующую кнопку.*\n\n"
        "*Мы позаботимся о безопасной и быстрой транзакции.*"
    )
    await message.answer(text,parse_mode='Markdown',reply_markup=kb.inline_add_funds)


@user.callback_query(F.data.startswith ('topup_'))
async def send_invoice(callback: CallbackQuery,bot:Bot):
    user_amount = int(callback.data.split('_')[-1])
    prices = [LabeledPrice(label="Тестовый товар", amount=user_amount*100)]  # 10000 копеек = 100.00 руб
    await callback.message.delete()
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="Тестовая покупка",
        description="Это тестовый платёж через ЮKassa в Telegram",
        payload="test_payload",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="test-payment",
    )


@user.callback_query(F.data == 'MySum')
async def wait_user_sum(callback:CallbackQuery,state:FSMContext):
    await callback.message.delete()
    await callback.message.answer('*Введите сумму которую хотите пополнить*',parse_mode='Markdown')
    await state.set_state(UserState.wait_add_sum)


@user.message(UserState.wait_add_sum)
async def user_sum_handler(message:Message,state:FSMContext,bot:Bot):
    user_amount = int(message.text)
    prices = [LabeledPrice(label="Тестовый товар", amount=user_amount*100)]  # 10000 копеек = 100.00 руб
    await state.clear()

    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Тестовая покупка",
        description="Это тестовый платёж через ЮKassa в Telegram",
        payload="test_payload",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="test-payment",
    )


# ✅ Подтверждение перед оплатой
@user.pre_checkout_query()
async def pre_checkout_query_handler(query: PreCheckoutQuery,bot:Bot):
    await bot.answer_pre_checkout_query(query.id, ok=True)

# 💰 Уведомление об успешной оплате
@user.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    tg_id = message.from_user.id 
    tg_order_id = message.successful_payment.telegram_payment_charge_id
    provider_id = message.successful_payment.provider_payment_charge_id  
    amount = message.successful_payment.total_amount / 100  

    await Order.create_order( tg_id, tg_order_id, provider_id, amount)
    await Order.add_balance( tg_id, amount)
    await message.answer("✅Оплата прошла успешно!")