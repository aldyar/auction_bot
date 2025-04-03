from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton


user_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = '💵Баланс'),
                                           KeyboardButton(text = '➕Пополнить баланс')],
                                           [KeyboardButton(text = '🧾История заявок')]],resize_keyboard=True)

async def inline_bids_keyboard(bid_id):
    inline_bids_keyboards = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = '+50 рублей', callback_data=f'50bids_{bid_id}'),
                                                        InlineKeyboardButton(text = '+100 рублей',callback_data=f'100bids_{bid_id}')],
                                                        [InlineKeyboardButton(text = 'Блиц выкуп',callback_data= f'blitz_{bid_id}')]])
    return inline_bids_keyboards
