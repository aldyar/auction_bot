1 User
    tg_id Bigint
    balance
    name 

2 Bid
    id
    create_date
    is_active
    end_date
    full_name
    phone
    type_of_request
    description
    valid: true or false 
3 Order
class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # ID счета Cryptomus
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Статус платежа
    tg_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), nullable=False)  # ID пользователя
    amount: Mapped[str] = mapped_column(String(15), nullable=False)  # Сумма платежа
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)  # Обработан ли платеж
    processed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)



routers
1) register
    я отправляю name,tg_id
2)get_user
    tg_id
3)update_user
    tg_id ,value,field      
vale = 'balance'
field = '14'



from aiogram import Bot, types
from aiogram.types import CallbackQuery
import asyncio

# Словарь для хранения оставшегося времени для каждого таймера
timers = {}

# Функция для старта таймера
async def run_timer(bid_id, callback: CallbackQuery, bot: Bot):
    # Инициализация времени для конкретного таймера
    timers[bid_id] = 30  # Таймер 30 секунд (можно менять)
    remaining_time = timers[bid_id]

    # Пример, как получить информацию о заявке
    bid = await Bid.get_bid_by_id(bid_id)

    if not bid:
        await callback.answer("❌ Заявка не найдена!")
        return

    # Статичное сообщение, которое не изменяется
    initial_text = f"⏳ Обратный отсчёт начался! Время: {remaining_time // 60}:{remaining_time % 60:02d}"

    # Отправляем сообщение с информацией о заявке (это статичный текст)
    sent_message = await callback.message.edit_text(initial_text, parse_mode='Markdown')

    # Таймер в фоновом режиме
    while remaining_time > 0:
        await asyncio.sleep(1)  # Пауза 1 секунда
        remaining_time -= 1  # Уменьшаем оставшееся время
        timers[bid_id] = remaining_time  # Обновляем оставшееся время в словаре

    # Когда время вышло, выводим финальное сообщение
    await sent_message.edit_text(f"✅ Время вышло!\n\n{initial_text}", parse_mode='Markdown')

    # Удаляем таймер из словаря по окончанию
    del timers[bid_id]

# Обработчик для нажатия на кнопку (время обновляется)
@user.callback_query(F.data == 'info_timer')
async def send_remaining_time(callback: CallbackQuery):
    # Получаем id заявки из callback_data
    bid_id = callback.data.split('_')[-1]

    # Получаем оставшееся время для конкретного bid_id
    remaining_time = timers.get(bid_id, 0)

    minutes = remaining_time // 60
    sec = remaining_time % 60
    await callback.answer(f"Осталось {minutes}:{sec:02d}")

# Обработчик команды для старта таймера
@user.callback_query(F.data == 'start_timer')
async def start_timer(callback: CallbackQuery, bot: Bot):
    bid_id = callback.data.split('_')[-1]  # Получаем ID заявки из callback_data

    # Запускаем таймер в фоновом потоке
    await run_timer(bid_id, callback, bot)
