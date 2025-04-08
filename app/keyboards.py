from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton


user_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = '💵Баланс'),
                                           KeyboardButton(text = '➕Пополнить баланс')],
                                           [KeyboardButton(text = '🧾История заявок')]],resize_keyboard=True)

async def inline_bids_keyboard(bid_id):
    inline_bids_keyboards = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = '+50 рублей', callback_data=f'50bids_{bid_id}'),
                                                        InlineKeyboardButton(text = '+100 рублей',callback_data=f'100bids_{bid_id}')],
                                                        [InlineKeyboardButton(text = 'Блиц выкуп',callback_data= f'blitz_{bid_id}')],
                                                        [InlineKeyboardButton(text= 'Информация',callback_data=f'info_{bid_id}')]])
    return inline_bids_keyboards


async def inline_invalid_bid(bid_id):
    inline_invalid_bid = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = '❌Заявка не валидная', callback_data= f'InvalidBId_{bid_id}')]]) 
    return inline_invalid_bid

inline_history_topup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = '🧾История пополнения',callback_data='history_topup')]])


admin_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Заявки'),
                                            KeyboardButton(text = 'Статистика')],
                                            [KeyboardButton(text = 'Управление пользователями')]],resize_keyboard=True)

inline_admin_bid = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'Новые заявки',callback_data='NewBids'),
                                                          InlineKeyboardButton(text = 'Активные заявки',callback_data= 'ActiveBids')]])
async def inline_accept_bid(bid_id):
    inline_accept_bid = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'Одобрить заявку', callback_data= f'AcceptBid_{bid_id}')],
                                                          [InlineKeyboardButton(text = 'Удалить заявку', callback_data= f'DeleteBid_{bid_id}')]])
    return inline_accept_bid

admin_search_user = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = '🔍Поиск пользователя',callback_data = 'SearchUser')]])

async def admin_block_unlock_user(user_id):
    admin_block_unlock_user = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'Разблокировать',callback_data=f'unlock_{user_id}'),
                                                                     InlineKeyboardButton(text = 'Заблокировать', callback_data= f'block_{user_id}')]])

    return admin_block_unlock_user

inline_admin_stat = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'за 24 часа',callback_data='day'),
                                                           InlineKeyboardButton(text='За неделю' ,callback_data='week')],
                                                           [InlineKeyboardButton(text = 'За месяц',callback_data='month')]])