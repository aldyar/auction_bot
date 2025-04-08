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
    

@admin.message(Admin(), CommandStart())
async def admin_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Добро пожаловать в панель администратора',reply_markup=kb.admin_menu)


@admin.message(Admin(),F.text == 'Заявки')
async def bid_handler(message:Message):
    await message.answer(
    "*🔹 Активные заявки* — это те, которые уже запущены и участвуют в аукционе в группе.\n"
    "*🕓 Новые заявки* — ожидают вашего одобрения перед запуском.\n\n"
    "Выберите действие ниже ⤵️",
    reply_markup=kb.inline_admin_bid,
    parse_mode="Markdown"
)


@admin.callback_query(Admin(),F.data == 'NewBids')
async def new_bids_handler(callback:CallbackQuery):
    bids = await Bid.get_new_bids()
    await callback.answer()
    for bid in bids:
        text = (
            f"*📌 Новая заявка №{bid.id}*\n\n"
            f"*👤 Имя:* {bid.full_name}\n"
            f"*📞 Телефон:* {bid.phone}\n"
            f"*📅 Дата заявки:* {bid.request_date.strftime('%d.%m.%Y %H:%M')}\n"
            f"*📂 Категория:* {bid.category}\n"
            f"*❓ Вопрос:* {bid.question}\n"
            f"*💼 Тип запроса:* {bid.request_type}\n"
            f"*💰 Стартовая цена:* {bid.start_price}₸\n"
            f"*⚡ Блиц-цена:* {bid.blitz_price if bid.blitz_price else '—'}\n\n"
            "Выберите действие для этой заявки ⤵️"
        )
        keyboard = await kb.inline_accept_bid(bid.id)
        await callback.message.answer(text, parse_mode="Markdown",reply_markup=keyboard)

@admin.callback_query(Admin(),F.data.startswith('AcceptBid_'))
async def accept_bid_handler(callback:CallbackQuery,bot:Bot):
    bid_id = callback.data.split("_")[1]
    await Bid.mark_bid_taken(bid_id)
    await callback.answer()
    await timer(callback.message, bid_id,bot)
    

@admin.callback_query(Admin(), F.data == 'ActiveBids')
async def active_bids_handler(callback:CallbackQuery):   
    bids = await Bid.get_all_active_bids()
    await callback.answer()
    if not bids:
        return await callback.message.answer('*На данный момент активных заявок нет*',parse_mode='Markdown')
    for bid in bids:
        text = (
            f"*📌 Новая заявка №{bid.id}*\n\n"
            f"*👤 Имя:* {bid.full_name}\n"
            f"*📞 Телефон:* {bid.phone}\n"
            f"*📅 Дата заявки:* {bid.request_date.strftime('%d.%m.%Y %H:%M')}\n"
            f"*📂 Категория:* {bid.category}\n"
            f"*❓ Вопрос:* {bid.question}\n"
            f"*💼 Тип запроса:* {bid.request_type}\n"
            f"*💰 Стартовая цена:* {bid.start_price}₸\n"
            f"*⚡ Блиц-цена:* {bid.blitz_price if bid.blitz_price else '—'}\n\n"
            "Выберите действие для этой заявки ⤵️"
        )
        await callback.message.answer(text, parse_mode="Markdown")
