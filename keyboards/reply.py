from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.selector import is_user_have_config, all_user_configs


async def payed_user_kb():#меню основное 
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.insert(KeyboardButton("🔌Подключиться"))
    keyboard.insert(KeyboardButton("💵 Продлить VPN"))
    keyboard.insert(KeyboardButton("🤳Как настроить VPN"))
    keyboard.insert(KeyboardButton("🔑Мои ключи"))
    keyboard.insert(KeyboardButton("🕑 Моя подписка"))
    keyboard.insert(KeyboardButton("😎 Спонсоры"))
    keyboard.insert(KeyboardButton("😍 Пожертвовать"))
    keyboard.insert(KeyboardButton("📝 Помощь"))
    keyboard.insert( KeyboardButton("💵 Тарифы VPN",))
    
    return keyboard
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# async def payed_user_kb():
#     # Создаем инлайн-клавиатуру
#     keyboard = InlineKeyboardMarkup(row_width=2)
    
#     # Добавляем инлайн-кнопки с callback_data
#     buttons = [
#         InlineKeyboardButton("🔌 Подключиться", callback_data='connect'),
#         InlineKeyboardButton("🤳 Как настроить VPN", callback_data='setup_vpn'),
#         InlineKeyboardButton("🔑 Мои ключи", callback_data='my_keys'),
#         InlineKeyboardButton("🕑 Моя подписка", callback_data='my_subscription'),
#         InlineKeyboardButton("😎 Спонсоры", callback_data='sponsors'),
#         InlineKeyboardButton("😍 Пожертвовать", callback_data='donate'),
#         InlineKeyboardButton("📝 Помощь", callback_data='help')
#     ]
    
#     # Добавляем кнопки в клавиатуру
#     for button in buttons:
#         keyboard.add(button)
    
#     return keyboard

async def update_user_kb(user_id: int): #меню который выдвется после окончание срока подписки 
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.insert(KeyboardButton("🔌Подключиться"))
    keyboard.insert(KeyboardButton("💵 Продлить VPN"))
    keyboard.insert(KeyboardButton("🤳Как настроить VPN"))
    keyboard.insert(KeyboardButton("🔑Мои ключи"))
    keyboard.insert(KeyboardButton("🕑 Моя подписка"))
    keyboard.insert(KeyboardButton("😎 Спонсоры"))
    keyboard.insert(KeyboardButton("😍 Пожертвовать"))
    keyboard.insert(KeyboardButton("📝 Помощь"))
    keyboard.insert( KeyboardButton("💵 Тарифы VPN",))


    if is_user_have_config(user_id=user_id):
        keyboard.insert(KeyboardButton("🔑Мои ключи"))
    return keyboard


async def free_user_kb(user_id: int):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.insert(KeyboardButton("🔌Подключиться"))
    keyboard.insert(KeyboardButton("💵 Продлить VPN"))
    keyboard.insert(KeyboardButton("🤳Как настроить VPN"))
    keyboard.insert(KeyboardButton("🔑Мои ключи"))
    keyboard.insert(KeyboardButton("🕑 Моя подписка"))
    keyboard.insert(KeyboardButton("😎 Спонсоры"))
    keyboard.insert(KeyboardButton("😍 Пожертвовать"))
    keyboard.insert(KeyboardButton("📝 Помощь"))
    keyboard.insert( KeyboardButton("💵 Тарифы VPN",))
    

    if is_user_have_config(user_id=user_id):
        keyboard.insert(KeyboardButton("🔑Мои ключи"))
        
    return keyboard


async def configs_kb(user_id: int):
    configs_kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    configs = all_user_configs(user_id=user_id)

    if configs:
        for config in configs:
            configs_kb.insert(
                KeyboardButton(
                    f"🔐 {'ПК' if config[0].split('_')[-1] == 'PC' else 'Смартфон'}"
                )
            )

    if not configs or len(configs) < 2:
        configs_kb.insert(KeyboardButton("🆕 Создать конфиг"))

    configs_kb.insert(KeyboardButton("🔙 Назад"))

    return configs_kb


async def subscription_management_kb():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.insert(KeyboardButton("📅 Дата отключения"))
    keyboard.insert(KeyboardButton("💵 Продлить VPN"))
    keyboard.insert(KeyboardButton("🔙 Назад"))
    return keyboard


async def get_coffee_list():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.insert(KeyboardButton("😍 Булочку 35р")) 
    keyboard.insert(KeyboardButton("☕️ Айс кофе 250₽"))
    keyboard.insert(KeyboardButton("🍰 Тортик 350р"))
    keyboard.insert(KeyboardButton("🔙 Назад"))

    return keyboard


async def get_pay_buttons():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.insert(KeyboardButton("✅1 месяц 100р"))
    keyboard.insert(KeyboardButton("✅3 месяц 300р"))
    keyboard.insert(KeyboardButton("✅6 месяц 600р"))
    keyboard.insert(KeyboardButton("✅12 месяц 1200р"))
    keyboard.insert(KeyboardButton("🔙 Назад"))


    return keyboard
