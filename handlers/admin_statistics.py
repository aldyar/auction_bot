from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command,CommandStart
from aiogram.fsm.context import FSMContext
from config import ADMIN
from function.bid_func import BidFunction as Bid
from function.user_func import UserFunction as User
from function.admin_func import AdminFunction
import app.keyboards as kb
from handlers.user_group import timer
from aiogram import Bot

admin = Router()


class Admin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in ADMIN
    

@admin.message(Admin(),F.text == 'Статистика')
async def admin_stat_handler(message:Message):
    bids = await Bid.get_all_bids()
    users = await User.get_all_users()
    active_users = await AdminFunction.get_active_users()
    sold_bids = await AdminFunction.get_sold_bids()
    not_sold_bids = await AdminFunction.get_not_sold_bids()

    revenue = sum(bid.sold_price or 0 for bid in bids)
    average_price = revenue / len(sold_bids) if sold_bids else 0  # избегаем деления на 0
    bids_count = len(bids)
    not_sold_percent = 100*(len(sold_bids)/ bids_count)
    user_count = len(users.all())
    active_users_count = len(active_users)
    await message.answer(
        f"*📊 Статистика по заявкам*\n\n"
        f"🔹 *Общее количество заявок:* `{bids_count}`\n"
        f"🔸 *Проданные заявки:* `{len(sold_bids)}`\n"
        f"🔸 *Процент проданных заявок:* `{int(not_sold_percent)}%`\n\n"
        
        
        f"*📊 Статистика по пользователям*\n\n"
        f"🔹 *Общее количество пользователей:* `{user_count}`\n"
        f"🔸 *Активные пользователи:* `{active_users_count}`\n\n"
        
        f"*💰 Финансовая статистика*\n\n"
        f"🔹 *Общая выручка:* `{revenue} Р`\n"
        f"🔹 *Средняя цена за заявку:* `{average_price} Р` \n\n"
        
        f"📈 *Статистика актуальна на момент запроса*\n",
        parse_mode='Markdown', reply_markup=kb.inline_admin_stat
    )
    

@admin.callback_query(Admin(),F.data == 'day')
async def admin_stat_day_handler(callback:CallbackQuery):
    await callback.answer()
    bids = await AdminFunction.get_total_bids_by_period(1)
    sold_bids = await AdminFunction.get_sold_bids_by_period(1)
    users = await AdminFunction.get_users_by_registration_period(1)
    active_users = await AdminFunction.get_active_users_by_period(1)

    revenue = sum(bid.sold_price or 0 for bid in bids)
    average_price = revenue / len(sold_bids) if sold_bids else 0  # избегаем деления на 0
    not_sold_percent = 0 if not bids else 100 * (len(sold_bids) / len(bids))
    await callback.message.answer(
        f"*📊Статистика за 24 часа*\n\n"
        f"*📊 Статистика по заявкам*\n\n"
        f"🔹 *Общее количество заявок:* `{len(bids)}`\n"
        f"🔸 *Проданные заявки:* `{len(sold_bids)}`\n"
        f"🔸 *Процент проданных заявок:* `{int(not_sold_percent)}%`\n\n"

        f"*📊 Статистика по пользователям*\n\n"
        f"🔹 *Новых пользователей за 24 часа:* `{len(users)}`\n"
        f"🔸 *Активные пользователи за 24 часа:* `{len(active_users)}`\n\n"

        f"*💰 Финансовая статистика*\n\n"
        f"🔹 *Общая выручка:* `{revenue} Р`\n"
        f"🔹 *Средняя цена за заявку:* `{average_price} Р` \n\n",
        parse_mode='Markdown'
    )   

@admin.callback_query(Admin(),F.data == 'week')
async def admin_stat_day_handler(callback:CallbackQuery):
    await callback.answer()
    bids = await AdminFunction.get_total_bids_by_period(7)
    sold_bids = await AdminFunction.get_sold_bids_by_period(7)
    users = await AdminFunction.get_users_by_registration_period(7)
    active_users = await AdminFunction.get_active_users_by_period(7)

    revenue = sum(bid.sold_price or 0 for bid in bids)
    average_price = revenue / len(sold_bids) if sold_bids else 0  # избегаем деления на 0
    not_sold_percent = 0 if not bids else 100 * (len(sold_bids) / len(bids))
    await callback.message.answer(
        f"*📊Статистика за неделю*\n\n"
        f"*📊 Статистика по заявкам*\n\n"
        f"🔹 *Общее количество заявок:* `{len(bids)}`\n"
        f"🔸 *Проданные заявки:* `{len(sold_bids)}`\n"
        f"🔸 *Процент проданных заявок:* `{int(not_sold_percent)}%`\n\n"

        f"*📊 Статистика по пользователям*\n\n"
        f"🔹 *Новых пользователей за неделю:* `{len(users)}`\n"
        f"🔸 *Активные пользователи за неделю:* `{len(active_users)}`\n\n"

        f"*💰 Финансовая статистика*\n\n"
        f"🔹 *Общая выручка:* `{revenue} Р`\n"
        f"🔹 *Средняя цена за заявку:* `{average_price} Р` \n\n",
        parse_mode='Markdown'
    )   


@admin.callback_query(Admin(),F.data == 'month')
async def admin_stat_day_handler(callback:CallbackQuery):
    await callback.answer()
    bids = await AdminFunction.get_total_bids_by_period(30)
    sold_bids = await AdminFunction.get_sold_bids_by_period(30)
    users = await AdminFunction.get_users_by_registration_period(30)
    active_users = await AdminFunction.get_active_users_by_period(30)

    revenue = sum(bid.sold_price or 0 for bid in bids)
    average_price = revenue / len(sold_bids) if sold_bids else 0  # избегаем деления на 0
    not_sold_percent = 0 if not bids else 100 * (len(sold_bids) / len(bids))
    await callback.message.answer(
        f"*📊Статистика за месяц*\n\n"
        f"*📊 Статистика по заявкам*\n\n"
        f"🔹 *Общее количество заявок:* `{len(bids)}`\n"
        f"🔸 *Проданные заявки:* `{len(sold_bids)}`\n"
        f"🔸 *Процент проданных заявок:* `{int(not_sold_percent)}%`\n\n"

        f"*📊 Статистика по пользователям*\n\n"
        f"🔹 *Новых пользователей за месяц:* `{len(users)}`\n"
        f"🔸 *Активные пользователи за месяц:* `{len(active_users)}`\n\n"

        f"*💰 Финансовая статистика*\n\n"
        f"🔹 *Общая выручка:* `{revenue} Р`\n"
        f"🔹 *Средняя цена за заявку:* `{average_price} Р` \n\n",
        parse_mode='Markdown'
    )   

