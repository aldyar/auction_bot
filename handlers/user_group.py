from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.states import Chat, Image
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from database.requests import set_user,get_user
from function.bid_func import get_bid,set_active_bid, delete_active_bid,update_active_bid,get_active_bid,buy_bid
from aiogram.enums import ChatAction
from aiogram import Bot
from config import GROUP_ID
import asyncio
import logging


user = Router()
logging.basicConfig(level=logging.INFO)

"""@user.message(Command("send_test"))
async def timer (message: Message):
    countdown_time = 300  # 5 минут = 300 секунд
    sent_message = await message.answer(f"⏳ Обратный отсчёт: *{countdown_time // 60}:00* минут",parse_mode='Markdown')
    
    for i in range(countdown_time - 1, -1, -1):
        if i % 1 == 0:  # Обновлять сообщение раз в 5 секунд
            minutes = i // 60
            sec = i % 60
            await sent_message.edit_text(f"⏳ Обратный отсчёт: *{minutes}:{sec:02d}*",parse_mode='Markdown')
        
        await asyncio.sleep(1)
    
    await sent_message.edit_text("✅ Время вышло!")"""


@user.message(Command("get_chat_id"))
async def get_chat_id(message: Message):
    await message.answer(f"Chat ID: {message.chat.id}")

@user.message(F.text =='text')
async def test_handler(message:Message):
    bid = await get_bid()
    await message.answer(f'Id: {bid.id}')


@user.message(Command("send_test"))
async def timer(message: Message):
    countdown_time = 8  # 5 минут = 300 секунд
    sent_message = await message.answer(
        f"⏳ Обратный отсчёт: *{countdown_time // 60}:00* минут\n\n",
        parse_mode='Markdown'
    )
    
    # Получаем заявку из базы данных через функцию get_bid
    bid = await get_bid()  # вызов твоей асинхронной функции для получения заявки
    
    if bid is None:
        await sent_message.edit_text("❌ Заявка не найдена!")
        return

    # Формируем текст с данными заявки
    bid_info = (
        f"Тип заявки: {bid.request_type}\n"
        f"Вопрос: {bid.question}\n"
        f"Категория: {bid.category}\n"
        f"Стартовая цена: {bid.start_price}\n"
        f"Блиц-цена: {bid.blitz_price if bid.blitz_price else 'Не указана'}"
    )
    keyboard = await kb.inline_bids_keyboard(bid.id)
    await set_active_bid(bid.id,bid.start_price,bid.blitz_price)
    for i in range(countdown_time - 1, -1, -1):
        if i % 1 == 0:  # Обновляем сообщение раз в 5 секунд
            minutes = i // 60
            sec = i % 60
            await sent_message.edit_text(
                f"⏳ Обратный отсчёт: *{minutes}:{sec:02d}*\n\n{bid_info}",
                parse_mode='Markdown',reply_markup=keyboard
            )
            
        
        await asyncio.sleep(1)
    
    await sent_message.edit_text(f"✅ Время вышло!\n\n{bid_info}")
    active_bid = await get_active_bid(bid.id)
    if active_bid:
        await buy_bid(message.from_user.id, bid.id)
        await message.answer(f'Пользователь {active_bid} выкупил')
        await delete_active_bid(bid.id)
    else:
        await message.answer("❌ Ставок не было. Запускаем заново...")
        await delete_active_bid(bid.id)
        await timer(message)  # 🔥 Перезапуск хендлера


@user.callback_query(F.data.startswith('50bids_'))
async def auction_50_handler(callback:CallbackQuery):
    bid_id = callback.data.split('_')[1]
    user_id = callback.from_user.id
    current = 50
    await update_active_bid(bid_id,user_id,current)
    await callback.answer()


@user.callback_query(F.data.startswith('100bids_'))
async def auction_50_handler(callback:CallbackQuery):
    bid_id = callback.data.split('_')[1]
    user_id = callback.from_user.id
    current = 100
    await update_active_bid(bid_id,user_id,current)
    await callback.answer()