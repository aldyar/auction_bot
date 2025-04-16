from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from function.user_func import UserFunction

class BanCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = await UserFunction.get_user(event.from_user.id)

        if user and user.is_banned:
            await event.answer("🚫 Вы заблокированы и не можете использовать бота.")
            return  # Прекращаем обработку

        return await handler(event, data)
