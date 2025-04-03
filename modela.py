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