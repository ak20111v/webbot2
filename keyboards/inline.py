from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import selector as select


async def device_kb(user_id: int):
    """returns inline keyboard with various options of cfg choosing"""
    kb = InlineKeyboardMarkup(
        row_width=2,
    )

    existing_devices = [
        item[0].split("_")[-1] for item in select.all_user_configs(user_id=user_id)
    ]

    if "PC" not in existing_devices:
        kb.insert(
            InlineKeyboardButton(text="💻 ПК", callback_data="pc_config_create_request")
        )
    if "PHONE" not in existing_devices:
        kb.insert(
            InlineKeyboardButton(
                text="📱 Смартфон", callback_data="phone_config_create_request"
            )
        )

    kb.add(
        InlineKeyboardButton(text="❌Отмена❌", callback_data="cancel_config_creation")
    )

    return kb


async def cancel_payment_kb():
    """returns inline keyboard with cancel payment button"""
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text="❌Отмена❌", callback_data="cancel_payment"))
    return kb


async def create_new_payment_kb(url: str, payment_id: str, free: bool, time: int = 0):
    """Button with link for payment"""

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text="💳Оплатить", url=url))
    kb.add(InlineKeyboardButton(text="👉Обновить статус платежа👈", callback_data=f"check_payment:{payment_id}:{0 if free is False else 1}:{time}"))

    return kb


if __name__ == "__main__":
    ...
