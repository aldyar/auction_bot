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

user = Router()



@user.message(F.text == '🧾История заявок')
async def history_bid_handler(message: Message):
    bids = await Bid.get_user_bid_history(message.from_user.id)
    if not bids:
        return await message.answer('❌ У вас пока нет заявок.')

    for bid in bids:
        text = (
            f"📄 *Заявка №{bid.id}*\n"
            f"🧑 *ФИО:* *{bid.full_name}*\n"
            f"📞 *Телефон:* `{bid.phone}`\n"
            f"📌 *Тип запроса:* *{bid.request_type}*\n"
            f"📂 *Категория:* *{bid.category}*\n"
            f"❓ *Вопрос:* {bid.question}\n"
        )
        keyboard = await kb.inline_invalid_bid(bid.id)
        await message.answer(text, parse_mode="Markdown",reply_markup=keyboard)


@user.callback_query(F.data.startswith('InvalidBId_'))
async def invalid_bid_handler(callback:CallbackQuery,state: FSMContext):
    bid_id = callback.data.split("_")[1]
    await state.update_data(bid_id=int(bid_id))
    await callback.message.delete()
    await callback.message.answer('⏳*Напишите пожалуйста причину:*',parse_mode='Markdown')
    await state.set_state(InvalidBid.text)


@user.message(InvalidBid.text)
async def wait_text_handler(message:Message, state:FSMContext):
    print("📥 Получено сообщение от пользователя в состоянии InvalidBid")
    data = await state.get_data()
    print(f"🔍 Данные из FSM: {data}")
    bid_id = data.get("bid_id")  # достаем айди из FSM

    reason = message.text
    print(f"✏️ Причина: {reason}")
    await message.answer('⏳*Заявка отправлена на проверку*',parse_mode='Markdown')
    print(f"📤 Вызываем change_to_invalid_bid с bid_id={bid_id} и reason='{reason}'")

    await Bid.change_to_invalid_bid(bid_id, reason)
    await state.clear()