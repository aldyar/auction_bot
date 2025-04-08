import asyncio
from aiogram import Dispatcher, Bot
from config import TOKEN
from handlers.admin import admin
from handlers.user import user
from handlers.user_history import user as user_history
from handlers.user_group import user as user_group
from handlers.admin_bid import admin as admin_bid
from handlers.admin_statistics import admin as admin_stat
from handlers.user_payment import user as user_payment

from database.models import async_main


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(admin, admin_bid, admin_stat,
                       user, user_group, user_history, user_payment)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

async def on_startup(dispatcher):
    await async_main()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass