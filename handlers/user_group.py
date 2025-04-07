from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from function.bid_func import BidFunction as Bid
from function.user_func import UserFunction as User
from aiogram.enums import ChatAction
from aiogram import Bot
from config import GROUP_ID
import asyncio
import logging

timers = {}

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



# @user.message(Command("send_test"))
# async def timer(message: Message,bid_id,bot:Bot):
#     countdown_time = 30  # 5 минут = 300 секунд


#     sent_message = await bot.send_message(
#         GROUP_ID,
#         f"⏳ Обратный отсчёт: *{countdown_time // 60}:00* минут\n\n",
#         parse_mode='Markdown'
#     )
    
#     # Получаем заявку из базы данных через функцию get_bid
#     bid = await Bid.get_bid_by_id(bid_id)  # вызов твоей асинхронной функции для получения заявки
#     timers[bid_id] = 30
#     remaining_time = timers[bid_id]
#     while remaining_time > 0:
#         await asyncio.sleep(1)  # Пауза 1 секунда
#         remaining_time -= 1  # Уменьшаем оставшееся время
#         timers[bid_id] = remaining_time  # Обновляем оставшееся время в словаре
#     del timers[bid_id]
#     if bid is None:
#         await sent_message.edit_text("❌ Заявка не найдена!")
#         return
#     await Bid.set_active_bid(bid.id,bid.start_price,bid.blitz_price)

#     keyboard = await kb.inline_bids_keyboard(bid.id)
    
#     for i in range(countdown_time - 1, -1, -1):
#         if i % 2 == 0:  # Обновляем сообщение раз в 5 секунд
#             minutes = i // 60
#             sec = i % 60
#             active_bid = await Bid.get_active_bid(bid.id)
#             if not active_bid:
#                 await sent_message.delete()  # Удаляем сообщение
#                 return  # Прерываем выполнение функции (и цикла, если он в этой функции)
#             # Формируем текст с данными заявки
#             bid_info = (
#                 f"Тип заявки: {bid.request_type}\n"
#                 f"Вопрос: {bid.question}\n"
#                 f"Категория: {bid.category}\n"
#                 f"Стартовая цена: {bid.start_price}\n"
#                 f"Блиц-цена: {bid.blitz_price if bid.blitz_price else 'Не указана'}\n\n"
#                 f'Текущая цена:{active_bid.current_price}\n'
#                 f'Последний покупатель:{active_bid.tg_id if active_bid.tg_id else 'Ставок по лоту не было'}'
#             )
#             await sent_message.edit_text(
#                 f"⏳ Обратный отсчёт: *{minutes}:{sec:02d}*\n\n{bid_info}",
#                 parse_mode='Markdown',reply_markup=keyboard
#             )
            
        
#         await asyncio.sleep(1)
        
#     await sent_message.edit_text(f"✅ Время вышло!\n\n{bid_info}")
#     await Bid.delete_active_bid(bid.id)
#     if active_bid.tg_id is not None:
#         await Bid.buy_bid(message.from_user.id, bid.id,active_bid.current_price)
#         await bot.send_message(GROUP_ID,f'Пользователь {active_bid.tg_id} выкупил, Последняя цена : {active_bid.current_price}')
    # if active_bid:
    #     await buy_bid(message.from_user.id, bid.id)
    #     await message.answer(f'Пользователь {active_bid.tg_id} выкупил')
    #     await delete_active_bid(bid.id)
    # else:
    #     await message.answer("❌ Ставок не было. Запускаем заново...")
    #     await delete_active_bid(bid.id)
    #     await timer(message)  # 🔥 Перезапуск хендлера



@user.callback_query(F.data.startswith('50bids_'))
async def auction_50_handler(callback:CallbackQuery):
    bid_id = callback.data.split('_')[1]
    user_id = callback.from_user.id
    current = 50
    user = await User.get_user(user_id)
    active_bid = await Bid.get_active_bid(bid_id)
    price = active_bid.blitz_price
    if user.balance < price + 50:
        return await callback.answer('У вас не хватает средтсв',show_alert=True)
    await Bid.update_active_bid(bid_id,user_id,current)
    await callback.answer()


@user.callback_query(F.data.startswith('100bids_'))
async def auction_100_handler(callback:CallbackQuery):
    bid_id = callback.data.split('_')[1]
    user_id = callback.from_user.id
    current = 100
    user = await User.get_user(user_id)
    active_bid = await Bid.get_active_bid(bid_id)
    price = active_bid.blitz_price
    if user.balance < price + 100:
        return await callback.answer('У вас не хватает средтсв',show_alert=True)
    await Bid.update_active_bid(bid_id,user_id,current)
    await callback.answer()


@user.callback_query(F.data.startswith('blitz_'))
async def blitz_handler(callback:CallbackQuery):
    bid_id = callback.data.split('_')[1]
    user_id = callback.from_user.id
    user = await User.get_user(user_id)
    active_bid = await Bid.get_active_bid(bid_id)
    price = active_bid.blitz_price
    if user.balance < price:
        return await callback.answer('У вас не хватает средтсв',show_alert=True)
    await Bid.buy_bid(user_id,bid_id,price)
    await Bid.delete_active_bid(bid_id)
    await callback.message.answer(f'✅ Пользователь {user_id} выкупил заявку'
                                  f'По цене: {price}')



async def timer(message: Message,bid_id,bot:Bot):
    countdown_time = 300  # 5 минут = 300 секунд
    bid = await Bid.get_bid_by_id(bid_id)  # вызов твоей асинхронной функции для получения заявки
    keyboard = await kb.inline_bids_keyboard(bid.id)
    bid_info = (
                f"Тип заявки: {bid.request_type}\n"
                f"Вопрос: {bid.question}\n"
                f"Категория: {bid.category}\n"
                f"Стартовая цена: {bid.start_price}\n"
                f"Блиц-цена: {bid.blitz_price if bid.blitz_price else 'Не указана'}\n\n"

            )
    sent_message = await bot.send_message(
        GROUP_ID,
        bid_info,
        parse_mode='Markdown',reply_markup=keyboard
    )
    
    await Bid.set_active_bid(bid.id,bid.start_price,bid.blitz_price)
    timers[bid_id] = countdown_time
    
    for i in range(countdown_time - 1, -1, -1):
        # Пауза 1 секунда
        await asyncio.sleep(1)
        timers[bid_id] = i

        # Проверяем, не изменились ли данные заявки
        active_bid = await Bid.get_active_bid(bid.id)
        if not active_bid:
            await sent_message.delete()  # Удаляем сообщение
            del timers[bid_id]  # Удаляем таймер из словаря
            return  # Прерываем выполнение

    del timers[bid_id]
    await sent_message.delete()
    #await sent_message.edit_text(f"✅ Время вышло!\n\n{bid_info}")
    await Bid.delete_active_bid(bid.id)
    if active_bid.tg_id is not None:
        await Bid.buy_bid(active_bid.tg_id, bid.id,active_bid.current_price)
        await bot.send_message(GROUP_ID,f'Пользователь {active_bid.tg_id} выкупил , Последняя цена : {active_bid.current_price}')
    elif active_bid.tg_id is None:
        await Bid.mark_bid_not_sold(bid.id)
        await bot.send_message(GROUP_ID,f'Время вышло! Заявка по номером: {active_bid.bid_id} не была выкуплена ')


@user.callback_query(F.data.startswith ('info_'))
async def info_bid_handler(callback:CallbackQuery):
    bid_id = callback.data.split('_')[-1]

    # Получаем оставшееся время для конкретного bid_id
    remaining_time = timers.get(bid_id, 0)

    minutes = remaining_time // 60
    sec = remaining_time % 60
    active_bid = await Bid.get_active_bid(bid_id)
    price = active_bid.current_price
    await callback.answer(f"Осталось {minutes}:{sec:02d}\n"
                          f"Цена: {price}\n"
                          f"Покупатель:{active_bid.tg_id if active_bid.tg_id else 'Ставок по лоту не было'}")

